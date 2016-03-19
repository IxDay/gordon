"""Utils for dealing with the db and peewee library"""

import functools

import peewee

import lasagna.db as db


# pylint: disable=protected-access
def parse_entity(*path):
    """Parse the db entity and return the correct string"""
    entity = peewee.Entity(*path)
    return db.database.compiler()._parse_entity(entity, None, None)[0]

# pylint: disable=protected-access
def model_entity(model):
    """Get the entity of a model (basically 'schema'.'table_name')"""
    return parse_entity(model._meta.schema, model._meta.db_table)

def lock(*models):
    """Lock table to avoid race conditions"""

    lock_string = 'LOCK TABLE %s IN SHARE ROW EXCLUSIVE MODE'
    models = ', '.join([model_entity(model) for model in models])

    def decorator(func):
        """simple decorator function"""

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrap a function in order to lock tables during its execution"""
            with db.database.atomic():
                db.database.execute_sql(lock_string % models)
                return func(*args, **kwargs)

        return wrapper

    return decorator
