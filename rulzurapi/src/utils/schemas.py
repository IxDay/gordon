"""Schemas for dumping and loading datas of RulzUrAPI"""
import collections

import marshmallow as m

import db.helpers
import utils.exceptions as exc

FULLFIL_HELP = ('More info about fulfilling this entity here: '
                'http://link/to/the/doc')

identity = lambda x: x

###############################################################################
#                                                                             #
#                                   Helpers                                   #
#                                                                             #
###############################################################################

class DefaultMixin(m.Schema):
    """Default configuration for a Schema

    Has an id field required and a skip missing option
    (avoid setting a missing attribute to None)
    """

    id = m.fields.Integer()

    __envelope__ = {
        'single': None,
        'many': None
    }

    def get_envelope_key(self, many):
        """Helper to get the envelope key."""
        key = (self.__envelope__['many']
               if many else self.__envelope__['single'])
        return key

    @m.post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        """Add envelope around data, when dumping

        This method provide a different envelope based on
        the presence of multiple entries or not.
        """
        key = self.get_envelope_key(many)
        return data if key is None else {key: data}


    def handle_error(self, errors, data):
        """Flatten errors in order to remove "_schema" entry"""

        errors = errors.args[0]
        schema_errors = errors.pop('_schema', None)

        for key in errors:
            if not errors[key]:
                errors[key] = schema_errors.pop()


    class Meta(object):
        """Force error indexation"""
        index_errors = True


class PostMixin(m.Schema):
    """Default configuration for post arguments

    Exclude the id field, and require all the other fields
    """

    def __init__(self, *args, **kwargs):
        super(PostMixin, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True

    class Meta(object):
        """Options for the PostSchema"""
        exclude = ('id',)


class PutMixin(m.Schema):
    """Mixin for handling put entities

    Basically, it checks for the presence of an 'id' when providing
    a bulk update.
    """

    __update__ = identity

    # pylint: disable=protected-access
    @m.validates_schema(pass_original=True)
    def put_id_validator(self, data, original):
        """Ensure that an 'id' field is present when parsing many data"""
        if m.utils.is_collection(original):
            if data.get('id'):
                try:
                    data.update(self.__update__(data)._data)
                except exc.APIException:
                    raise m.ValidationError(db.helpers.CORRESPONDING, 'id')
            else:
                raise m.ValidationError(
                    m.fields.Field.default_error_messages['required'], 'id'
                )


class NestedMixin(m.Schema):
    """Mixin for handling nested entities in recipe"""
    __nested__ = identity
    __get_or_insert__ = identity

    def wrap_with_envelope(self, data, _):
        """Overrides the parent envelope method

        As we are using a transparent entity, it does not
        need any enveloping.
        """
        return data

    @m.post_load(pass_many=True)
    def get_insert_or_raise(self, data, many):
        """Runs a get or insert validation

        This will try to retrieve or insert data into the database,
        if an error occurs it is propagated.
        """
        if many:
            elts, errors = self.__get_or_insert__([
                {'id': d['id']} if 'id' in d else {'name': d['name']}
                for d in data
            ])
            if errors:
                raise m.ValidationError(errors)
            else:
                for d, elt in zip(data, elts):
                    d.update(elt)
        return data

    def handle_error(self, errors, data):
        """Reorganise error"""
        errors = collections.defaultdict(dict, errors.messages)
        ignore = []

        for key, value in errors.items():
            _schema = value.pop('_schema', [{}])[0]

            field_not_present = [
                field not in value for
                field in self.__nested__.fields.keys()
            ]
            field_not_present.append('id' not in value)
            if all(field_not_present):
                value.update(_schema)
            if 'id' in value or 'name' in value:
                ignore.append(key)

        data = [d for i, d in enumerate(data) if i not in ignore]
        _, errs = self.__get_or_insert__(data)

        cpt = 0
        for i in range(max(len(errs), len(errors))):
            if i + cpt in ignore:
                cpt += 1
            if i in errs:
                errors[i + cpt].update(errs[i])

        raise m.ValidationError(errors)


    @m.validates_schema
    def validate_schema(self, data):
        """Try to infer if it is a get or an insert method

        if it is a get only: 'id' will be retrieve and no other checking is
        required.
        Otherwise, it is an insert and data must be validated according to
        a POST method.

        If nothing is validated, it adds a custom error field to indicates
        the documentation.
        """

        errors = self.__nested__.validate(data) if 'id' not in data else None

        if errors:
            errors['_'] = FULLFIL_HELP
            raise m.ValidationError(errors)


###############################################################################
#                                                                             #
#                             Schemas definition                              #
#                                                                             #
###############################################################################


class Utensil(DefaultMixin):
    """Utensil schema (for put method, ie: the 'id' field is required)"""

    __envelope__ = {
        'single': 'utensil',
        'many': 'utensils'
    }

    name = m.fields.String()


class UtensilPut(PutMixin, Utensil):
    """Utensil PUT method schema"""

    __update__ = db.helpers.update_utensil

utensil_post = type('UtensilPost', (PostMixin, Utensil), {})()


class RecipeUtensils(NestedMixin, Utensil):
    """Base schema for RecipeUtensils table

    As it is a many to many transitional table, this entity as
    not a real existence in term of data, this is a bridge
    between a recipe and its utensils
    """

    __nested__ = utensil_post
    __get_or_insert__ = db.helpers.get_or_insert_utensils

    @m.pre_dump
    def retrieve_internal(self, data):
        """Flatten the data in order to avoid transitional entity

        As the data must be provided as flatten as possible, this
        function remove the transitional entity.
        Here is the database output:

        {
            recipe: {
                ...,
                utensils: [
                    {
                        utensil: {
                            id: ...,
                            name: ...
                        }
                    }
                ]
            }
        }

        ingredient must be merged in its parent entity,
        this is why this function exists, here is the output it generates:

        {
            recipe: {
                ...,
                utensils: [
                    {
                        id: ...,
                        name: ...
                    }
                ]
            }
        }
        """
        try:
            return data.utensil
        except AttributeError:
            return data


class Ingredient(DefaultMixin):
    """Base schema schema for ingredient (used to dump)"""

    __envelope__ = {
        'single': 'ingredient',
        'many': 'ingredients'
    }

    name = m.fields.String()

class IngredientPut(PutMixin, Ingredient):
    """Ingredient PUT method schema"""
    __update__ = db.helpers.update_ingredient


ingredient_post = type('IngredientPost', (PostMixin, Ingredient), {})()

class RecipeIngredients(NestedMixin, Ingredient):
    """Base schema for RecipeIngredients table

    As it is a many to many transitional table, this entity as
    not a real existence in term of data, this is a bridge
    between a recipe and its ingredients
    """

    __nested__ = ingredient_post
    __get_or_insert__ = db.helpers.get_or_insert_ingrs

    quantity = m.fields.Integer(
        validate=m.validate.Range(0), required=True
    )
    measurement = m.fields.Str(
        validate=m.validate.OneOf(['L', 'g', 'oz', 'spoon']),
        required=True
    )

    # pylint: disable=protected-access
    @m.pre_dump
    def retrieve_internal(self, data):
        """Flatten the data in order to avoid transitional entity

        As the data must be provided as flatten as possible, this
        function remove the transitional entity.
        Here is the database output:

        {
            recipe: {
                ...,
                ingredients: [
                    {
                        quantity:...,
                        measurement:...,
                        ingredient: {
                            id: ...,
                            name: ...
                        }
                    }
                ]
            }
        }

        ingredient must be merged in its parent entity,
        this is why this function exists, here is the output it generates:

        {
            recipe: {
                ...,
                ingredients: [
                    {
                        quantity:...,
                        measurement:...,
                        id: ...,
                        name: ...
                    }
                ]
            }
        }
        """
        try:
            return dict(
                list(data.ingredient._data.items()) + list(data._data.items())
            )
        except AttributeError:
            return data


class Direction(DefaultMixin):
    """Base schema for direction (used for dump)"""
    title = m.fields.String()
    text = m.fields.String()

    @m.post_load
    def to_tuple(self, data):
        """Transform data from dict to tuple

        In order to push data to the database, they must be provided
        as a tuple. This is the internal representation of a direction
        """
        return data['title'], data['text']

    @m.pre_dump
    def from_tuple(self, data):
        """Transform data from tuple to dict

        Data which are outputed from the database are tuples
        in order to provide something consistent and understandable
        this must be transformed to a regular dictionnary
        """
        return dict(zip(['title', 'text'], data))

    def handle_error(self, errors, data):
        """Remove the field if errors are caught"""
        raise m.ValidationError(errors.messages)


class Recipe(DefaultMixin):
    """Base schema for recipe (used for dump)"""

    __envelope__ = {
        'single': 'recipe',
        'many': 'recipes'
    }

    name = m.fields.String()
    people = m.fields.Integer(
        validate=m.validate.Range(1, 12)
    )
    difficulty = m.fields.Integer(
        validate=m.validate.Range(1, 5)
    )
    duration = m.fields.Str(
        validate=m.validate.OneOf([
            '0/5', '5/10', '10/15', '15/20', '20/25', '25/30', '30/45',
            '45/60', '60/75', '75/90', '90/120', '120/150'
        ])
    )
    category = m.fields.Str(
        validate=m.validate.OneOf(['starter', 'main', 'dessert'])
    )

    directions = m.fields.Nested(Direction, many=True, default=[])
    utensils = m.fields.Nested(RecipeUtensils, many=True, default=[])
    ingredients = m.fields.Nested(RecipeIngredients, many=True, default=[])


class RecipePost(PostMixin, Recipe):
    """Schema for loading recipe from a POST method"""
    utensils = m.fields.Nested(RecipeUtensils, many=True, missing=[])
    ingredients = m.fields.Nested(RecipeIngredients, many=True, missing=[])
    directions = m.fields.Nested(
        type('DirectionPost', (PostMixin, Direction), {}), many=True,
        missing=[]
    )

class RecipePut(PutMixin, Recipe):
    """Schema for loading recipe from a PUT method"""
    __update__ = db.helpers.update_recipe

    utensils = m.fields.Nested(RecipeUtensils, many=True)
    ingredients = m.fields.Nested(RecipeIngredients, many=True)
    directions = m.fields.Nested(
        type('DirectionPost', (PostMixin, Direction), {}), many=True,
    )

###############################################################################
#                                                                             #
#                            Schemas instantiation                            #
#                                                                             #
###############################################################################

Schema = collections.namedtuple('Schema', ['dump', 'put', 'post'])

ingredient = Schema(Ingredient().dump, IngredientPut(), ingredient_post)
utensil = Schema(Utensil().dump, UtensilPut(), utensil_post)

recipe = Schema(
    Recipe().dump,
    RecipePut(),
    RecipePost()
)
