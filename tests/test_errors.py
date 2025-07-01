def test_404(client):
    resp = client.get('/nonexistent-url')
    assert resp.status_code == 404
    assert "not found" in resp.text.lower() or "404" in resp.text

def test_405(client):
    resp = client.post('/')
    assert resp.status_code in (405, 404)

def test_500(client, monkeypatch):
    # Simulate a 500 error by monkeypatching a route
    from flask import Flask
    app = client.application
    @app.route('/error500')
    def error500():
        raise Exception("Test 500 error")
    resp = client.get('/error500')
    assert resp.status_code == 500
    assert "internal server error" in resp.text.lower() or "500" in resp.text