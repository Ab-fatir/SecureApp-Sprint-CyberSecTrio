from app.security import safe_ping

def test_safe_ping_valid_ip():
    res = safe_ping("127.0.0.1")
    assert res.get("error") == "" or "timed out" in res.get("error", "")

def test_safe_ping_valid_hostname():
    res = safe_ping("localhost")
    assert res.get("error") == "" or "timed out" in res.get("error", "")

def test_safe_ping_rejects_semicolon_chaining():
    res = safe_ping("127.0.0.1; whoami")
    assert not res["success"]
    assert "Invalid" in res["error"]

def test_safe_ping_rejects_pipe_injection():
    res = safe_ping("127.0.0.1 | dir")
    assert not res["success"]
    assert "Invalid" in res["error"]

def test_safe_ping_rejects_ampersand_chaining():
    res = safe_ping("127.0.0.1 && id")
    assert not res["success"]
    assert "Invalid" in res["error"]

def test_safe_ping_rejects_subshell_expansion():
    res = safe_ping("127.0.0.1 $(whoami)")
    assert not res["success"]
    assert "Invalid" in res["error"]

def test_safe_ping_rejects_backticks():
    res = safe_ping("127.0.0.1 `ls`")
    assert not res["success"]
    assert "Invalid" in res["error"]
