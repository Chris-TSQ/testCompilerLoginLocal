import sys
import os
import pytest

BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../backend'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import app        
import database  

import pytest


@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    monkeypatch.setattr(database, 'DATABASE', ':memory:')
    database.init_db()
    yield

def test_signup_and_login():
    app = backend_app.app
    with app.test_client() as client:
        r = client.post('/api/signup', json={
            "username": "test",
            "email": "test@test.com",
            "password": "123"
        })
        assert r.status_code == 201

        r = client.post('/api/login', json={
            "username": "test",
            "password": "123"
        })
        assert r.status_code == 200
