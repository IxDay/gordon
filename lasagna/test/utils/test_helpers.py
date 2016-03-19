# pylint: disable=missing-docstring

import lasagna.utils.helpers as helpers


def test_unpack():
    data = {'foo': 'bar'}

    assert helpers.unpack((data, 201, data)) == (data, 201, data)
    assert helpers.unpack((data, 201)) == (data, 201, {})
    assert helpers.unpack(data) == (data, 200, {})
    assert helpers.unpack(('foo', 'bar', 'baz', 'quuz')) == (
        ('foo', 'bar', 'baz', 'quuz'), 200, {}
    )

def test_dict_merge():
    a = {'jim': 123, 'a': {'b': {'c': {'d': 'bob'}}}, 'rob': 34}
    b = {'tot': {'a': {'b': 'string'}, 'c': [1, 2]}}
    c = {'tot': {'c': [3, 4]}}

    assert helpers.dict_merge(a, b, c) == {
        'a': {'b': {'c': {'d': 'bob'}}},
        'jim': 123,
        'rob': 34,
        'tot': {'a': {'b': 'string'}, 'c': [1, 2, 3, 4]}
    }
