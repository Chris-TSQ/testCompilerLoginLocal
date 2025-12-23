const path = require("path");
const TestGenerator = require("./TestGenerator");

class PyTestGenerator extends TestGenerator {
  supports(filePath) {
    return filePath.endsWith(".py");
  }

  generate(filePath) {
    const name = path.basename(filePath, ".py");

    const testCode = `
import pytest
from backend import app as backend_app
import backend.database as database

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
`;

    this.writeFile(
      `backend/tests/test_${name}.py`,
      testCode
    );
  }
}

module.exports = PyTestGenerator;
