
def test_events_api(client):
    resp = client.get('/api/events')
    assert resp.status_code == 200
    assert resp.is_json or resp.mimetype == 'application/json'
    data = resp.get_json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0] or 'name' in data[0]

def test_events_api_not_found(client):
    resp = client.get('/api/events/999999')
    assert resp.status_code in (404, 400)

def test_players_api(client):
    resp = client.get('/api/players')
    assert resp.status_code == 200
    assert resp.is_json or resp.mimetype == 'application/json'
    data = resp.get_json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0] or 'name' in data[0]

def test_players_api_not_found(client):
    resp = client.get('/api/players/999999')
    assert resp.status_code in (404, 400)