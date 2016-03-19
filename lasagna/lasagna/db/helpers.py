"""Helps managing the get or insert mecanism"""
import collections
import functools

import peewee

import lasagna.db.models as models

import lasagna.utils.helpers as helpers
import lasagna.utils.exceptions as exc

MULTIPLE = 'Multiple entries for the same element.'
CORRESPONDING = 'No corresponding id in database.'


def _multiple_entries_error(errors, elts, msg):
    """Convenient method for adding error message in elt error list

    This function is commented for keeping track of the algorithm
    """
    for elt in elts:
        # retrieve the elt and its index
        i, elt = elt['index'], elt['elt']
        # append the error message in the correct field according on
        # element attributes
        errors[i]['id' if 'id' in elt else 'name'].append(msg)


def _get(model, elts):
    """Retrieve elts from database

    Filters elts, try to retrieve those existing in the database
    (according to name or id).
    If name does not exist, it will be created in the _insert method
    If id does not exist, an error is reported

    This function ensure that we keep track of the element index in
    success and errors
    """
    dd = collections.defaultdict
    dm = helpers.dict_merge

    ids, names, errors = dd(list), dd(list), dd(lambda: dd(list))

    for i, elt in enumerate(elts):
        key, struct = (elt['id'], ids) if 'id' in elt else (elt['name'], names)
        struct[key].append({'index': i, 'elt': elt})

    id_keys, name_keys = list(ids.keys()), list(names.keys())

    if id_keys and name_keys:
        where_clause = (model.id << id_keys) | (model.name << name_keys)
    elif names:
        where_clause = (model.name << name_keys)
    elif ids:
        where_clause = (model.id << id_keys)

    for obj in model.select().where(where_clause):

        if obj.id in ids and obj.name in names:
            err_msg = {'msg': MULTIPLE, 'id': obj.id, 'name': obj.name}
            for elt in ids.pop(obj.id):
                errors[elt['index']]['id'].append(err_msg)
            for elt in names.pop(obj.name):
                errors[elt['index']]['name'].append(err_msg)

            continue

        elt = ids.pop(obj.id, []) or names.pop(obj.name, [])

        if len(elt) > 1:
            _multiple_entries_error(errors, elt, MULTIPLE)
            continue

        elt = elt.pop()
        elts[elt['index']] = dm(obj._data, elt['elt'])

    for v in ids.values():
        if len(v) > 1:
            _multiple_entries_error(errors, v, MULTIPLE)
        _multiple_entries_error(errors, v, CORRESPONDING)

    for k, v in names.items():
        if len(v) > 1:
            _multiple_entries_error(errors, v, MULTIPLE)
        else:
            names[k] = v[0]

    return names, errors


def _insert(model, elts, names):
    """Insert names into the database and add them to elts"""
    req = (model
           .insert_many([elt['elt'] for elt in names.values()])
           .returning())

    for obj in req.execute():
        elts[names[obj.name]['index']] = obj._data


def get_or_insert(model, elts):
    """Get the elements from a model or create them if they not exist"""
    names, errors = {}, {}

    if elts:
        names, errors = _get(model, elts)

    if names and not errors:
        _insert(model, elts, names)

    return elts, errors


def get(model, pk):
    """Get a specific elt or raise 404 if it does not exists"""
    try:
        return model.get(model.id == pk)
    except peewee.DoesNotExist:
        raise exc.APIException('%s not found' % model._meta.name, 404)


def update(model, value):
    """Update an elt and return it"""
    try:
        return (model
                .update(**value)
                .where(model.id == value.pop('id'))
                .returning()
                .execute()
                .next())
    except StopIteration:
        raise exc.APIException('%s not found' % model._meta.name, 404)


get_or_insert_utensils = functools.partial(get_or_insert, models.Utensil)
get_or_insert_ingrs = functools.partial(get_or_insert, models.Ingredient)

update_utensil = functools.partial(update, models.Utensil)
update_ingredient = functools.partial(update, models.Ingredient)


def select_recipes(where_clause=None):
    """Select recipes according to where_clause if provided"""

    recipes = (
        models.Recipe
        .select(models.Recipe, models.RecipeIngredients, models.Ingredient,
                models.RecipeUtensils, models.Utensil)
        .join(models.RecipeIngredients, peewee.JOIN.LEFT_OUTER)
        .join(models.Ingredient, peewee.JOIN.LEFT_OUTER)
        .switch(models.Recipe)
        .join(models.RecipeUtensils, peewee.JOIN.LEFT_OUTER)
        .join(models.Utensil, peewee.JOIN.LEFT_OUTER)
        .switch(models.Recipe)
    )
    if where_clause:
        recipes = recipes.where(where_clause)

    return recipes.aggregate_rows().execute()


def select_utensils(recipe_id):
    """Retrieve recipe utensils from database"""
    return list(
        models.Utensil
        .select()
        .join(models.RecipeUtensils)
        .where(models.RecipeUtensils.recipe == recipe_id)
        .dicts()
    )


def select_ingredients(recipe_id):
    """Retrieve recipe ingredients from database"""
    return list(
        models.RecipeIngredients
        .select(
            models.RecipeIngredients.quantity,
            models.RecipeIngredients.measurement,
            models.Ingredient
        )
        .join(models.Ingredient)
        .where(models.RecipeIngredients.recipe == recipe_id)
        .dicts()
    )


def recipe_insert_utensils(recipe_id, utensils):
    """Insert the utensils of a recipe into its intermediary table"""
    recipe_utensils = [
        {'recipe': recipe_id, 'utensil': utensil['id']} for utensil in utensils
    ]
    if recipe_utensils:
        models.RecipeUtensils.insert_many(recipe_utensils).execute()


def recipe_insert_ingredients(recipe_id, ingredients):
    """Insert the ingredients of a recipe into its intermediary table"""
    def ingr_builder(ingr):
        return {
            'recipe': recipe_id, 'ingredient': ingr['id'],
            'quantity': ingr['quantity'], 'measurement': ingr['measurement']
        }

    recipe_ingredients = [ingr_builder(ingr) for ingr in ingredients]
    if recipe_ingredients:
        models.RecipeIngredients.insert_many(recipe_ingredients).execute()


def _update_recipe(recipe):
    """Update a recipe"""

    def delete_old_entries(model, recipe_id):
        """Delete entries on model given a specific recipe id"""
        model.delete().where(model.recipe == recipe_id).execute()

    ingredients = recipe.pop('ingredients', None)
    utensils = recipe.pop('utensils', None)

    recipe = update(models.Recipe, recipe)

    if utensils is None:
        utensils = select_utensils(recipe.id)
    else:
        delete_old_entries(models.RecipeUtensils, recipe.id)
        recipe_insert_utensils(recipe.id, utensils)

    if ingredients is None:
        ingredients = select_ingredients(recipe.id)
    else:
        delete_old_entries(models.RecipeIngredients, recipe.id)
        recipe_insert_ingredients(recipe.id, ingredients)

    recipe._data.update({'ingredients': ingredients, 'utensils': utensils})
    return recipe

update_recipe = functools.partial(_update_recipe)
