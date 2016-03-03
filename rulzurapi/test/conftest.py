"""Global py.test configuration"""
# pylint: disable=unused-argument, protected-access, redefined-outer-name
import os
import collections
import json

import pytest

import app as app_builder

import db
import db.models as models
import db.utils

import utils.helpers


@pytest.fixture
def app():
    """Base fixture, retrieve the app and pass custom testing configuration

    This will start the database connection, and set the application
    configuration.

    Read the settings files in order to see available options.
    """
    if not 'RULZURAPI_SETTINGS' in os.environ:
        os.environ['RULZURAPI_SETTINGS'] = 'test.settings'
    return app_builder.create_app()


@pytest.fixture
@db.database.atomic()
def clean_db(app):
    """Clean database entries before test

    This fixture goes through model tables and removes
    all entries.

    It also reinitialise the sequences (for ids), in order to have
    consistent ids accross tests.
    """
    # delete table content
    tables = [models.RecipeIngredients, models.RecipeUtensils,
              models.Ingredient, models.Utensil, models.Recipe]
    for table in tables:
        table.delete().execute()

    # reset id sequences
    sequences = [models.Ingredient.id.sequence, models.Utensil.id.sequence,
                 models.Recipe.id.sequence]
    for sequence in sequences:
        entity = db.utils.parse_entity(db.schema, sequence)
        db.database.execute_sql('ALTER SEQUENCE %s RESTART WITH 1' % (entity,))


@pytest.fixture
def client(app, clean_db):
    """Retrieves a test client from flask and the rulzurapi application

    Also add a parser around the client, in order to easily parse the
    response in tests
    """
    attrs = ['status_code', 'data', 'headers']
    Response = collections.namedtuple('Response', attrs)

    headers = {'Content-Type': 'application/json'}

    def client_open_decorator(func):
        """simple decorator around client 'open' method"""

        def wrapper(*args, **kwargs):
            """Convenient wrapper for API calls

            This function infers if the data passed is a dict and
            dump it as a json if so, adding the proper headers.

            It then pass the data to the client 'open' method

            If the response is a json (according to response headers),
            it is loaded as a python dict.
            """
            data = kwargs.get('data')
            if utils.helpers.is_iterable(data):
                kwargs['data'] = json.dumps(data)

            headers.update(kwargs.get('headers', {}))
            kwargs['headers'] = headers
            response = func(*args, **kwargs)

            response_data = response.data.decode('utf8')
            if response.mimetype == 'application/json':
                response_data = json.loads(response_data or '{}')

            return Response(response.status_code, response_data,
                            response.headers)

        return wrapper

    client = app.test_client()
    client.open = client_open_decorator(client.open)

    return client


@pytest.yield_fixture
def gen_table(app):
    """Generates tables for a given test

    Pass a table definition and the fixture will create it against the
    correct schema and database (the test one).
    It also keeps tracks on it and remove it at the end of the test
    """
    tables = []
    def make_table(table):
        """Factory for creating and registering the given table"""
        table = type(table.__name__, (models.BaseModel, table,), {})
        table.create_table()
        tables.append(table)

        return table

    db.database.execute_sql('SET search_path TO %s,public' % db.schema)
    yield make_table

    for table in tables:
        table.drop_table()

@pytest.fixture
def next_id(app):
    """Fixture which retrieves the last value of a sequence"""

    def wrapper(model):
        """Factory which accept a model and gives its next id entry"""
        entity = db.utils.parse_entity(model._meta.schema, model.id.sequence)

        return lambda: db.database.execute_sql(
            'SELECT last_value FROM %s' % (entity,)
        ).fetchone()[0]

    return wrapper
