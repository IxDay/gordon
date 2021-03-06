"""Database models

Models from the database adapted to python through peewee ORM
"""
import peewee

import lasagna.db as db
import lasagna.db.orm as db_orm


class BaseModel(peewee.Model):
    """Define the common model configuration"""

    @classmethod
    def create_table(cls, *args, **kwargs):
        for field in cls._meta.fields.values():
            try:
                field.pre_field_create(cls)
            except AttributeError:
                pass

        cls._meta.database.create_table(cls, *args, **kwargs)

        for field in cls._meta.fields.values():
            try:
                field.post_field_create(cls)
            except AttributeError:
                pass

    class Meta(object):
        """Define the common database configuration for the models

        All the configuration is loaded from db.connector,
        this is just a linking to have this in a dedicated file and share it to
        the models
        """
        database = db.database
        schema = db.schema


class Ingredient(BaseModel):
    """database's ingredient table"""
    id = peewee.PrimaryKeyField(sequence='ingredient_id_seq')
    name = peewee.CharField()


class Utensil(BaseModel):
    """database's utensil table"""
    id = peewee.PrimaryKeyField(sequence='utensil_id_seq')
    name = peewee.CharField()


class Recipe(BaseModel):
    """database's recipe table"""
    id = peewee.PrimaryKeyField(sequence='recipe_id_seq')
    name = peewee.CharField()
    description = peewee.TextField()
    directions = db_orm.ArrayField(db_orm.DirectionField)
    difficulty = peewee.IntegerField()
    duration = db_orm.EnumField(choices=[
        '0/5', '5/10', '10/15', '15/20', '20/25', '25/30', '30/45', '45/60',
        '60/75', '75/90', '90/120', '120/150'])
    people = peewee.IntegerField()
    category = db_orm.EnumField(choices=['starter', 'main', 'dessert'])


class RecipeIngredients(BaseModel):
    """database's recipe_ingredients table"""
    recipe = peewee.ForeignKeyField(
        Recipe,
        related_name='ingredients',
        db_column='fk_recipe'
    )
    ingredient = peewee.ForeignKeyField(
        Ingredient,
        related_name='recipes',
        db_column='fk_ingredient'
    )
    quantity = peewee.IntegerField()
    measurement = db_orm.EnumField(choices=['L', 'g', 'oz', 'spoon'])

    class Meta(object):
        """ManyToMany relationship for recipe_ingredients

        primary_key need to be specified here

        peewee does not handle the tables creation, so we have to make the name
        linking by hand (db_tables)
        """
        primary_key = peewee.CompositeKey('recipe', 'ingredient')
        db_table = 'recipe_ingredients'


class RecipeUtensils(BaseModel):
    """database's recipe_utensils table"""
    recipe = peewee.ForeignKeyField(
        Recipe,
        related_name='utensils',
        db_column='fk_recipe'
    )
    utensil = peewee.ForeignKeyField(
        Utensil,
        related_name='recipes',
        db_column='fk_utensil'
    )

    class Meta(object):
        """ManyToMany relationship for recipe_utensils

        primary_key need to be specified here

        peewee does not handle the tables creation, so we have to make the name
        linking by hand (db_tables)
        """
        primary_key = peewee.CompositeKey('recipe', 'utensil')
        db_table = 'recipe_utensils'
