# app/tests/integration/test_auth.py

import pytest
from flask import Flask
from api.auth.auth import login_required

@pytest.fixture
def app():
    app = Flask(__name__)

    @route('/protected')
    @login_required
    def protected_route():
        return 'Protected route'

    return app

def test_protected_route(client):
    response = client.get('/protected')
    assert response.status_code == 401
    assert response.json == {'message': 'Authorization required'}
