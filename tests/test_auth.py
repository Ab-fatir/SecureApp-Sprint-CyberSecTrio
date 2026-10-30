from app.models import User
from tests.conftest import login_client

def test_password_hashing(secure_app):
    with secure_app.app_context():
        user = User(username="testuser", role="user")
        user.set_password("MySecretPass123!")
        assert user.password_hash != "MySecretPass123!"
        assert user.verify_password("MySecretPass123!")
        assert not user.verify_password("WrongPass!")

def test_registration_validation(secure_client):
    response = secure_client.post(
        "/register",
        data={"username": "newuser", "password": "123"},
        follow_redirects=True
    )
    assert b"chars" in response.data

def test_login_flow(secure_client):
    response = login_client(secure_client, "alice", "Alice1234!")
    assert response.status_code == 200

def test_unauthenticated_dashboard_redirect(secure_client):
    response = secure_client.get("/dashboard")
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")
