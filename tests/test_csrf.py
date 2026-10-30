from tests.conftest import login_client
from app.security import CSRF_KEY

def test_vulnerable_mode_allows_request_without_csrf_token(vuln_client):
    login_client(vuln_client, "alice", "Alice1234!")
    response = vuln_client.post(
        "/documents/1/transfer",
        data={"new_owner": "bob"},
        follow_redirects=True
    )
    assert response.status_code == 200

def test_secure_mode_rejects_request_without_csrf_token(secure_client):
    login_client(secure_client, "alice", "Alice1234!")
    response = secure_client.post(
        "/documents/1/transfer",
        data={"new_owner": "bob"}
    )
    assert response.status_code == 403

def test_secure_mode_rejects_invalid_csrf_token(secure_client):
    login_client(secure_client, "alice", "Alice1234!")
    response = secure_client.post(
        "/documents/1/transfer",
        data={"new_owner": "bob", "csrf_token": "fake_token_123"}
    )
    assert response.status_code == 403

def test_secure_mode_accepts_valid_csrf_token(secure_client):
    login_client(secure_client, "alice", "Alice1234!")
    with secure_client.session_transaction() as sess:
        valid_token = sess.get(CSRF_KEY)

    response = secure_client.post(
        "/documents/1/transfer",
        data={"new_owner": "bob", "csrf_token": valid_token},
        follow_redirects=True
    )
    assert response.status_code == 200
