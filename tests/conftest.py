import pytest
from app import create_app

@pytest.fixture
def secure_app():
    app = create_app(
        mode="secure",
        test_config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-key-1",
            "WTF_CSRF_ENABLED": True
        }
    )
    with app.app_context():
        yield app

@pytest.fixture
def vuln_app():
    app = create_app(
        mode="vulnerable",
        test_config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-key-2",
            "WTF_CSRF_ENABLED": False
        }
    )
    with app.app_context():
        yield app

@pytest.fixture
def secure_client(secure_app):
    return secure_app.test_client()

@pytest.fixture
def vuln_client(vuln_app):
    return vuln_app.test_client()

def login_client(client, username, password):
    return client.post("/login", data={"username": username, "password": password}, follow_redirects=True)
