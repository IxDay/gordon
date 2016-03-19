"""API utensils entrypoints"""
import flask
import peewee

import lasagna.db as db
import lasagna.db.models as models
import lasagna.db.helpers as db_helpers

import lasagna.utils.helpers as helpers
import lasagna.utils.schemas as schemas
import lasagna.utils.exceptions as exc

blueprint = flask.Blueprint('utensils', __name__, template_folder='templates')


@blueprint.route('')
@helpers.template({'text/html': 'utensils.html'})
def utensils_get():
    """List all utensils"""
    utensils = models.Utensil.select().dicts()
    return schemas.utensil.dump(utensils, many=True).data


@blueprint.route('', methods=['POST'])
@db.database.atomic()
def utensils_post():
    """Create an utensil"""
    utensil = helpers.raise_or_return(schemas.utensil.post)
    try:
        utensil = models.Utensil.create(**utensil)
    except peewee.IntegrityError:
        raise exc.APIException('utensil already exists', 409)

    return schemas.utensil.dump(utensil).data, 201


@blueprint.route('', methods=['PUT'])
@db.database.atomic()
def utensils_put():
    """Update multiple utensils"""
    utensils = helpers.raise_or_return(schemas.utensil.put, True)
    return schemas.utensil.dump(utensils, many=True).data


@blueprint.route('/<int:utensil_id>')
def utensil_get(utensil_id):
    """Provide the utensil for utensil_id"""
    utensil = db_helpers.get(models.Utensil, utensil_id)
    return schemas.utensil.dump(utensil).data


@blueprint.route('/<int:utensil_id>', methods=['PUT'])
@db.database.atomic()
def utensil_put(utensil_id):
    """Update the utensil for utensil_id"""
    utensil = helpers.raise_or_return(schemas.utensil.put)
    if not utensil:
        raise exc.APIException('no data provided for update')

    utensil['id'] = utensil_id
    utensil = db_helpers.update(models.Utensil, utensil)
    return schemas.utensil.dump(utensil).data


@blueprint.route('/<int:utensil_id>/recipes')
def recipes_get(utensil_id):
    """List all the recipes for utensil_id"""

    # This ensure that the utensil exists
    db_helpers.get(models.Utensil, utensil_id)

    recipe_ids = (models.Recipe
                  .select(models.Recipe.id)
                  .join(models.RecipeUtensils)
                  .where(models.RecipeUtensils.utensil == utensil_id))

    recipes = list(db.helpers.select_recipes(models.Recipe.id << recipe_ids))

    return schemas.recipe.dump(recipes, many=True).data
