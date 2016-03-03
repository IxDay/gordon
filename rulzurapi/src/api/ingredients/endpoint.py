"""API ingredients entrypoints"""
import flask
import peewee

import db
import db.models as models
import db.helpers
import db.utils

import utils.exceptions as exc
import utils.helpers
import utils.schemas as schemas


blueprint = flask.Blueprint('ingredients', __name__)

@blueprint.route('')
def ingredients_get():
    """List all ingredients"""
    ingredients = models.Ingredient.select().dicts()
    return schemas.ingredient.dump(ingredients, many=True).data


@blueprint.route('', methods=['POST'])
@db.database.atomic()
def ingredients_post():
    """Create an ingredient"""
    ingredient = utils.helpers.raise_or_return(schemas.ingredient.post)
    try:
        ingredient = models.Ingredient.create(**ingredient)
    except peewee.IntegrityError:
        raise exc.APIException('ingredient already exists', 409)

    return schemas.ingredient.dump(ingredient).data, 201


@blueprint.route('', methods=['PUT'])
@db.database.atomic()
def ingredients_put():
    """Update multiple ingredients"""
    ingredients = utils.helpers.raise_or_return(schemas.ingredient.put, True)
    return schemas.ingredient.dump(ingredients, many=True).data


@blueprint.route('/<int:ingredient_id>')
def ingredient_get(ingredient_id):
    """Provide the ingredient for ingredient_id"""
    ingredient = db.helpers.get(db.models.Ingredient, ingredient_id)
    return schemas.ingredient.dump(ingredient).data


@blueprint.route('/<int:ingredient_id>', methods=['PUT'])
@db.database.atomic()
def ingredient_put(ingredient_id):
    """Update the ingredient for ingredient_id"""
    ingredient = utils.helpers.raise_or_return(schemas.ingredient.put)
    if not ingredient:
        raise exc.APIException('no data provided for update')

    ingredient['id'] = ingredient_id
    ingredient = db.helpers.update(models.Ingredient, ingredient)
    return schemas.ingredient.dump(ingredient).data


@blueprint.route('/<int:ingredient_id>/recipes')
def recipe_get(ingredient_id):
    """List all the recipes for ingredient_id"""

    # This ensure that the ingredient exists
    db.helpers.get(models.Ingredient, ingredient_id)

    recipe_ids = (models.Recipe
                  .select(models.Recipe.id)
                  .join(models.RecipeIngredients)
                  .where(models.RecipeIngredients.ingredient == ingredient_id))

    recipes = list(db.helpers.select_recipes(models.Recipe.id << recipe_ids))

    return schemas.recipe.dump(recipes, many=True).data
