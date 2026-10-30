import os
import re
import secrets
import subprocess
from functools import wraps
from flask import session, request, abort

CSRF_KEY = "_csrf_token"
HOST_PATTERN = re.compile(r"^[a-zA-Z0-9.\-]+$")

def generate_csrf_token():
    if CSRF_KEY not in session:
        session[CSRF_KEY] = secrets.token_hex(32)
    return session[CSRF_KEY]

def validate_csrf_token(token):
    saved_token = session.get(CSRF_KEY)
    if not saved_token or not token:
        return False
    return secrets.compare_digest(saved_token, token)

def csrf_protected(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ["POST", "PUT", "DELETE"]:
            token = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token")
            if not token or not validate_csrf_token(token):
                abort(403)
        return f(*args, **kwargs)
    return decorated_function

def check_document_access(document, user):
    if not user:
        return False
    if user.role == "admin":
        return True
    return document.owner_id == user.id

def safe_ping(target):
    target = target.strip()
    if not target or not HOST_PATTERN.match(target):
        return {
            "success": False,
            "error": "Invalid host format",
            "output": ""
        }

    is_windows = os.name == "nt"
    cmd = ["ping", "-n" if is_windows else "-c", "1", target]

    try:
        proc = subprocess.run(
            cmd,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5
        )
        return {
            "success": proc.returncode == 0,
            "output": proc.stdout if proc.returncode == 0 else proc.stderr,
            "error": "" if proc.returncode == 0 else proc.stderr,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {"success": False, "error": str(e), "output": ""}

def set_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self' https:; script-src 'self' 'unsafe-inline' https:; style-src 'self' 'unsafe-inline' https:; frame-ancestors 'none';"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
