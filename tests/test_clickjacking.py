from tests.conftest import login_client

def test_vulnerable_mode_omits_framing_headers(vuln_client):
    login_client(vuln_client, "admin", "Admin1234!")
    response = vuln_client.get("/admin/console")
    assert response.status_code == 200
    assert "X-Frame-Options" not in response.headers

def test_secure_mode_enforces_x_frame_options_deny(secure_client):
    login_client(secure_client, "admin", "Admin1234!")
    response = secure_client.get("/admin/console")
    assert response.status_code == 200
    assert response.headers.get("X-Frame-Options") == "DENY"

def test_secure_mode_enforces_csp_frame_ancestors_none(secure_client):
    login_client(secure_client, "admin", "Admin1234!")
    response = secure_client.get("/admin/console")
    csp = response.headers.get("Content-Security-Policy", "")
    assert "frame-ancestors 'none'" in csp

def test_secure_mode_includes_nosniff_header(secure_client):
    response = secure_client.get("/login")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
