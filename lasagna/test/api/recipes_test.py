import pytest

import lasagna.db.models as models
import test.api.utils as utils


@pytest.fixture
def next_utensil_id(next_id):
    return next_id(models.Utensil)


@pytest.fixture
def next_recipe_id(next_id):
    return next_id(models.Recipe)


@pytest.fixture
def recipe_tmp_1():
    return {
        'name': 'recipe_1', 'difficulty': 1, 'people': 2, 'duration': '0/5',
        'category': 'starter'
    }, {
        'id': 1, 'name': 'recipe_1', 'difficulty': 1, 'people': 2,
        'duration': '0/5', 'category': 'starter', 'directions': [],
        'utensils': [], 'ingredients': []
    }


@pytest.fixture
def recipe_tmp_2(utensils):
    return {
        'name': 'recipe_2', 'difficulty': 1, 'people': 2, 'duration': '0/5',
        'category': 'starter',
        'directions': [], 'ingredients': [],
        'utensils': [
            {'id': utensils[0]['id']},
            {'id': utensils[1]['id']}
        ]
    }, {
        'id': 2, 'name': 'recipe_2', 'difficulty': 1, 'people': 2,
        'duration': '0/5', 'category': 'starter', 'directions': [],
        'ingredients': [],
        'utensils': [
            {'name': 'utensil_1'},
            {'name': 'utensil_2'}
        ]
    }


@pytest.fixture
def recipe_tmp_3(utensils):
    return {
        'name': 'recipe_3', 'difficulty': 1, 'people': 2, 'duration': '0/5',
        'category': 'starter',
        'directions': [], 'ingredients': [],
        'utensils': [
            {'name': utensils[0]['name']},
            {'name': utensils[1]['name']}
        ]
    }, {
        'id': 3, 'name': 'recipe_3', 'difficulty': 1, 'people': 2,
        'duration': '0/5', 'category': 'starter', 'directions': [],
        'ingredients': [],
        'utensils': [
            {'name': 'utensil_1'},
            {'name': 'utensil_2'}
        ]
    }


@pytest.fixture
def recipe_tmp_4(utensils, ingredients):
    return {
        'name': 'recipe_4',
        'difficulty': 1,
        'people': 2,
        'duration': '0/5',
        'category': 'starter',
        'directions': [
            {'title': 'step_1', 'text': 'instruction recipe 1 step 1'},
            {'title': 'step_2', 'text': 'instruction recipe 1 step 2'}
        ],
        'utensils': [
            {'id': utensils[0]['id']},
            {'name': utensils[1]['name']},
            {'name': 'utensil_3'},
            {'name': 'utensil_4'}
        ],
        'ingredients': [
            {'id': ingredients[0]['id'], 'measurement': 'L', 'quantity': 1},
            {
                'name': ingredients[1]['name'], 'measurement': 'g',
                'quantity': 2
            },
            {'name': 'ingredient_3', 'measurement': 'oz', 'quantity': 3},
            {'name': 'ingredient_4', 'measurement': 'spoon', 'quantity': 4}
        ]
    }, {
        'id': 4,
        'name': 'recipe_4',
        'difficulty': 1,
        'people': 2,
        'duration': '0/5',
        'category': 'starter',
        'directions': [
            {'title': 'step_1', 'text': 'instruction recipe 1 step 1'},
            {'title': 'step_2', 'text': 'instruction recipe 1 step 2'}
        ],
        'utensils': [
            {'name': 'utensil_1'},
            {'name': 'utensil_2'},
            {'name': 'utensil_3'},
            {'name': 'utensil_4'}
        ],
        'ingredients': [
            {
                'name': 'ingredient_1',
                'measurement': 'L',
                'quantity': 1
            }, {
                'measurement': 'g',
                'name': 'ingredient_2',
                'quantity': 2
            }, {
                'measurement': 'oz',
                'name': 'ingredient_3',
                'quantity': 3
            }, {
                'measurement': 'spoon',
                'name': 'ingredient_4',
                'quantity': 4
            }
        ]
    }


@pytest.fixture
def recipes_valid(recipe_tmp_1, recipe_tmp_2, recipe_tmp_3, recipe_tmp_4):
    return [recipe_tmp_1, recipe_tmp_2, recipe_tmp_3, recipe_tmp_4]


@pytest.fixture
def recipe_invalid(utensils, ingredients):
    return {
        'name': int(),
        'difficulty': str(),
        'people': int(),
        'duration': 'foo',
        'category': 'bar',
        'directions': [
            {},
            {'title': int(), 'text': int()}
        ],
        'utensils': [
            {'id': utensils[0]['id']},
            {'id': utensils[0]['id']},
            {'name': utensils[0]['name']},
            {'name': utensils[1]['name']},
            {'name': utensils[1]['name']},
            {'id': 3},
            {'id': 3},
            {'name': 'utensil_3'},
            {'name': 'utensil_3'},
            {},
            {'id': str()},
            {'name': int()}
        ],
        'ingredients': [
            {},
            {'id': ingredients[0]['id']},
            {'id': ingredients[0]['id'], 'measurement': 'L', 'quantity': 1},
            {
                'name': ingredients[0]['name'], 'measurement': 'L',
                'quantity': 1
            },
            {
                'name': ingredients[1]['name'], 'measurement': 'L',
                'quantity': 1
            },
            {
                'name': ingredients[1]['name'], 'measurement': 'L',
                'quantity': 1
            },
            {'id': 3, 'measurement': 'L', 'quantity': 1},
            {'id': 3, 'measurement': 'L', 'quantity': 1},
            {'name': 'ingredient_3', 'measurement': 'L', 'quantity': 1},
            {'name': 'ingredient_3', 'measurement': 'L', 'quantity': 1},
            {'id': str(), 'measurement': int(), 'quantity': str()},
            {'name': int(), 'measurement': 'foo', 'quantity': -1}
        ]
    }, {
        'name': [utils.STRING],
        'difficulty': [utils.INTEGER],
        'people': ['Must be between 1 and 12.'],
        'category': [utils.CHOICE],
        'duration': [utils.CHOICE],
        'directions': {
            '0': {'text': [utils.MISSING], 'title': [utils.MISSING]},
            '1': {'text': [utils.STRING], 'title': [utils.STRING]}
        },
        'utensils': {
            '0': {
                'id': [{'msg': utils.MULTIPLE, 'id': 1, 'name': 'utensil_1'}]
            },
            '1': {
                'id': [{'msg': utils.MULTIPLE, 'id': 1, 'name': 'utensil_1'}]
            },
            '2': {
                'name': [{'msg': utils.MULTIPLE, 'id': 1, 'name': 'utensil_1'}]
            },
            '3': {'name': [utils.MULTIPLE]},
            '4': {'name': [utils.MULTIPLE]},
            '5': {'id': [utils.MULTIPLE, utils.CORRESPONDING]},
            '6': {'id': [utils.MULTIPLE, utils.CORRESPONDING]},
            '7': {'name': [utils.MULTIPLE]},
            '8': {'name': [utils.MULTIPLE]},
            '9': {'_': utils.FULLFIL, 'name': [utils.MISSING]},
            '10': {'id': [utils.INTEGER]},
            '11': {'name': [utils.STRING]}
        },
        'ingredients': {
            '0': {
                '_': utils.FULLFIL,
                'name': [utils.MISSING],
                'measurement': [utils.MISSING],
                'quantity': [utils.MISSING]
            },
            '1': {
                'id': [
                    {'msg': utils.MULTIPLE, 'id': 1, 'name': 'ingredient_1'}
                ],
                'measurement': [utils.MISSING],
                'quantity': [utils.MISSING]
            },
            '2': {
                'id': [
                    {'msg': utils.MULTIPLE, 'id': 1, 'name': 'ingredient_1'}
                ]
            },
            '3': {
                'name': [
                    {'msg': utils.MULTIPLE, 'id': 1, 'name': 'ingredient_1'}
                ]
            },
            '4': {'name': [utils.MULTIPLE]},
            '5': {'name': [utils.MULTIPLE]},
            '6': {'id': [utils.MULTIPLE, utils.CORRESPONDING]},
            '7': {'id': [utils.MULTIPLE, utils.CORRESPONDING]},
            '8': {'name': [utils.MULTIPLE]},
            '9': {'name': [utils.MULTIPLE]},
            '10': {
                'id': [utils.INTEGER],
                'measurement': [utils.STRING],
                'quantity': [utils.INTEGER]
            },
            '11': {
                'name': [utils.STRING],
                'measurement': [utils.CHOICE],
                'quantity': ['Must be at least 0.']
            }
        }
    }


@pytest.fixture
def recipe_invalids(recipe_invalid, next_utensil_id):
    recipe_invalid_2 = {
        'name': 'foo',
        'difficulty': 15,
        'people': str(),
        'duration': int(),
        'category': int(),
        'utensils': [{'id': next_utensil_id() + 1}],
    }, {
        'difficulty': ['Must be between 1 and 5.'],
        'people': [utils.INTEGER],
        'duration': [utils.STRING],
        'category': [utils.STRING],
        'utensils': {'0': {'id': [utils.CORRESPONDING]}}
    }
    return [recipe_invalid, recipe_invalid_2]


class TestRecipes(utils.TestEndpoint):
    endpoint = 'recipes'
    E_404 = 'recipe not found'
    E_409 = 'recipe already exists'

    def test_list(self, client, recipes):
        def unorder(rcps): return [utils.unorder_recipe(rcp) for rcp in rcps]

        super(TestRecipes, self).test_list(
            client, {'recipes': unorder(recipes)},
            lambda d: unorder(d['recipes'])
        )

    def test_post(self, client, recipes_valid):
        def edit_data(data): return utils.sanitize_recipe(data['recipe'])

        for recipe, expected in recipes_valid:
            super(TestRecipes, self).test_post(
                client, recipe, {'recipe': expected}, edit_data
            )

    def test_post_invalid(self, client, recipe_invalids):
        for recipe, errors in recipe_invalids:
            super(TestRecipes, self).test_post_invalid(client, recipe, errors)

    def test_post_409(self, client, recipe):
        super(TestRecipes, self).test_post_409(client, recipe)

    def test_put_list(self, client, recipes):
        recipe_1, recipe_2 = recipes

        recipe_1['name'] = 'foo'
        recipe_1['utensils'] = []
        recipe_1['directions'].append(
            {'title': 'step_3', 'text': 'instruction recipe 1 step 3'}
        )

        ingrs = recipe_1.pop('ingredients')
        recipe_2['ingredients'] = ingrs

        recipe_1_expected = utils.dict_merge(recipe_1, {'ingredients': ingrs})
        expected = {'recipes': [recipe_1_expected, recipe_2]}
        super(TestRecipes, self).test_put_list(client, recipes, expected)

    def test_get(self, client, recipe):
        super(TestRecipes, self).test_get(
            client, recipe['id'], {'recipe': utils.unorder_recipe(recipe)},
            lambda d: utils.unorder_recipe(d['recipe'])
        )

    def test_get_404(self, client, next_recipe_id):
        super(TestRecipes, self).test_get_404(client, next_recipe_id())

    def test_put(self, client, recipe):
        recipe['name'] = 'recipe_foo'
        expected = utils.dict_merge(recipe)

        recipe.pop('utensils')
        recipe.pop('ingredients')
        recipe.pop('directions')
        super(TestRecipes, self).test_put(client, recipe, {'recipe': expected})

        expected['utensils'].pop()
        expected['ingredients'].pop()
        recipe['utensils'] = expected['utensils']
        recipe['ingredients'] = expected['ingredients']

        super(TestRecipes, self).test_put(client, recipe, {'recipe': expected})

    def test_put_invalid(self, client, recipe_invalid, recipe):
        data, errs = recipe_invalid
        data['id'] = recipe['id']
        super(TestRecipes, self).test_put_invalid(client, [data], {'0': errs})

    def test_put_404(self, client, next_recipe_id):
        recipe = {'id': next_recipe_id()}
        super(TestRecipes, self).test_put_404(client, recipe)

    def test_get_ingredients_404(self, client, next_recipe_id):
        res = client.get(
            utils.urlize(self.endpoint, next_recipe_id(), 'ingredients')
        )

        assert res.status_code == 404
        assert res.data == {'status_code': 404, 'message': self.E_404}

    def test_get_ingredients(self, client, recipe):
        r_id = recipe['id']
        res = client.get(utils.urlize(self.endpoint, r_id, 'ingredients'))

        assert res.status_code == 200
        assert res.data == {'ingredients': recipe['ingredients']}

    def test_get_utensils_404(self, client, next_recipe_id):
        res = client.get(
            utils.urlize(self.endpoint, next_recipe_id(), 'utensils')
        )

        assert res.status_code == 404
        assert res.data == {'status_code': 404, 'message': self.E_404}

    def test_get_utensils(self, client, recipe):
        r_id = recipe['id']
        res = client.get(utils.urlize(self.endpoint, r_id, 'utensils'))

        assert res.status_code == 200
        assert res.data == {'utensils': recipe['utensils']}
