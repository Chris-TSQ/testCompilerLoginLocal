import sys
import os
import pytest
import importlib.util
import tempfile

print(">>> LOADED TEST_APP.PY <<<")

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(__file__, "../../../../.."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "backend")

sys.path.insert(0, BACKEND_DIR)

# ------------------------------------------------------------------
# Load backend/app.py dynamically
# ------------------------------------------------------------------
app_path = os.path.join(BACKEND_DIR, "app.py")

spec = importlib.util.spec_from_file_location("backend_app", app_path)
backend_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend_app)

import database

# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------
@pytest.fixture
def client(monkeypatch):
    # Create temp DB file (Windows-safe)
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    monkeypatch.setattr(database, "DATABASE", db_path)
    database.init_db()

    app = backend_app.app
    client = app.test_client()

    yield client

    # SQLite may still hold a lock; safe to leave temp files

# ------------------------------------------------------------------
# Signup tests
# ------------------------------------------------------------------
def test_signup_success(client):
    r = client.post("/api/signup", json={
        "username": "test",
        "email": "test@test.com",
        "password": "123"
    })
    assert r.status_code == 201

def test_signup_missing_fields(client):
    r = client.post("/api/signup", json={
        "username": "",
        "email": "",
        "password": ""
    })
    assert r.status_code == 400

def test_signup_duplicate_user(client):
    client.post("/api/signup", json={
        "username": "test",
        "email": "test@test.com",
        "password": "123"
    })

    r = client.post("/api/signup", json={
        "username": "test",
        "email": "test@test.com",
        "password": "123"
    })
    assert r.status_code == 409

# ------------------------------------------------------------------
# Login tests
# ------------------------------------------------------------------
def test_login_success(client):
    client.post("/api/signup", json={
        "username": "test",
        "email": "test@test.com",
        "password": "123"
    })

    r = client.post("/api/login", json={
        "username": "test",
        "password": "123"
    })
    assert r.status_code == 200
    assert "token" in r.json

def test_login_invalid_password(client):
    client.post("/api/signup", json={
        "username": "test",
        "email": "test@test.com",
        "password": "123"
    })

    r = client.post("/api/login", json={
        "username": "test",
        "password": "wrong"
    })
    assert r.status_code == 401

# ------------------------------------------------------------------
# Auth lifecycle tests
# ------------------------------------------------------------------
def test_verify_and_logout(client):
    client.post("/api/signup", json={
        "username": "test",
        "email": "test@test.com",
        "password": "123"
    })

    login = client.post("/api/login", json={
        "username": "test",
        "password": "123"
    })

    token = login.json["token"]

    verify = client.get("/api/verify", headers={
        "Authorization": f"Bearer {token}"
    })
    assert verify.status_code == 200

    logout = client.post("/api/logout", headers={
        "Authorization": f"Bearer {token}"
    })
    assert logout.status_code == 200

    verify_again = client.get("/api/verify", headers={
        "Authorization": f"Bearer {token}"
    })
    assert verify_again.status_code == 401
