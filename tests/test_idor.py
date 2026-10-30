from tests.conftest import login_client

def test_vulnerable_mode_allows_idor(vuln_client):
    login_client(vuln_client, "alice", "Alice1234!")
    response = vuln_client.get("/documents/2")
    assert response.status_code == 200

def test_secure_mode_blocks_idor(secure_client):
    login_client(secure_client, "alice", "Alice1234!")
    response = secure_client.get("/documents/2")
    assert response.status_code == 403

def test_secure_mode_allows_owner(secure_client):
    login_client(secure_client, "alice", "Alice1234!")
    response = secure_client.get("/documents/1")
    assert response.status_code == 200

def test_secure_mode_allows_admin_override(secure_client):
    login_client(secure_client, "admin", "Admin1234!")
    response = secure_client.get("/documents/2")
    assert response.status_code == 200
