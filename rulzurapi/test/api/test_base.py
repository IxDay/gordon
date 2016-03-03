

def test_index(client):
    res = client.get('/', headers={'Accept': 'text/html'})

    assert res.status_code == 200
    assert 'This is the index' in res.data
