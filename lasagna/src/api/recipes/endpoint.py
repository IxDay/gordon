"""API recipes entrypoints"""
import flask
import peewee

import db
import db.models as models
import db.utils
import db.helpers as db_helpers

import utils.helpers as helpers
import utils.schemas as schemas
import utils.exceptions as exc

blueprint = flask.Blueprint('recipes', __name__, template_folder='templates')



@blueprint.route('')
@helpers.template({'text/html': 'recipes.html'})
def recipes_get():
    """List all recipes"""
    recipes = db_helpers.select_recipes()
    return schemas.recipe.dump(recipes, many=True).data


@blueprint.route('', methods=['POST'])
@db.utils.lock(models.Utensil, models.Ingredient)
def recipes_post():
    """Create a recipe"""
    recipe = helpers.raise_or_return(schemas.recipe.post)


    utensils = recipe.pop('utensils')
    ingredients = recipe.pop('ingredients')
    try:
        recipe = models.Recipe.create(**recipe)
    except peewee.IntegrityError:
        raise exc.APIException('recipe already exists', 409)

    db_helpers.recipe_insert_utensils(recipe.id, utensils)
    db_helpers.recipe_insert_ingredients(recipe.id, ingredients)

    recipe.utensils = utensils
    recipe.ingredients = ingredients

    return schemas.recipe.dump(recipe).data, 201


@blueprint.route('', methods=['PUT'])
@db.utils.lock(models.Utensil, models.Ingredient)
def recipes_put():
    """Update multiple recipes"""
    recipes = helpers.raise_or_return(schemas.recipe.put, True)

    return schemas.recipe.dump(recipes, many=True).data


@blueprint.route('/<int:recipe_id>')
@helpers.template({'text/html': 'recipe.html'})
def recipe_get(recipe_id):
    """Provide the recipe for recipe_id"""
    try:
        recipe = next(db.helpers.select_recipes(models.Recipe.id == recipe_id))
    except StopIteration:
        raise exc.APIException('recipe not found', 404)

    return schemas.recipe.dump(recipe).data


@blueprint.route('/<int:recipe_id>', methods=['PUT'])
@db.utils.lock(models.Utensil, models.Ingredient)
def recipe_put(recipe_id):
    """Update a specified recipe"""
    recipe = helpers.raise_or_return(schemas.recipe.put)
    if not recipe:
        raise exc.APIException('no data provided for update')
    recipe['id'] = recipe_id
    recipe = db_helpers.update_recipe(recipe)
    return schemas.recipe.dump(recipe).data


@blueprint.route('/<int:recipe_id>/utensils')
def recipe_utensils_get(recipe_id):
    """List all the utensils for recipe_id"""
    db_helpers.get(models.Recipe, recipe_id)
    return {'utensils': db_helpers.select_utensils(recipe_id)}


@blueprint.route('/<int:recipe_id>/ingredients')
def recipe_ingredients_get(recipe_id):
    """List all the ingredients for recipe_id"""
    db_helpers.get(models.Recipe, recipe_id)
    return {'ingredients': db_helpers.select_ingredients(recipe_id)}
