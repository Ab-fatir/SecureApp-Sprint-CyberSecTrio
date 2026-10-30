import os
from flask import Flask
from app.models import db, User, Document
from app.security import set_security_headers, generate_csrf_token

def create_app(mode="secure", test_config=None):
    app = Flask(__name__)
    app.config["SECURITY_MODE"] = mode
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-123")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cloudvault.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if mode == "secure":
        app.config["SESSION_COOKIE_HTTPONLY"] = True
        app.config["SESSION_COOKIE_SAMESITE"] = "Strict"

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    @app.context_processor
    def inject_security_context():
        return {
            "csrf_token": generate_csrf_token if mode == "secure" else (lambda: ""),
            "security_mode": app.config.get("SECURITY_MODE", "secure")
        }

    @app.after_request
    def process_response(response):
        if app.config.get("SECURITY_MODE") == "secure":
            return set_security_headers(response)
        response.headers.pop("X-Frame-Options", None)
        response.headers.pop("Content-Security-Policy", None)
        return response

    from app.auth import auth_bp
    from app.vault import vault_bp
    from app.diagnostics import diagnostics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(vault_bp)
    app.register_blueprint(diagnostics_bp)

    with app.app_context():
        db.create_all()
        init_demo_users()

    return app

def init_demo_users():
    if User.query.count() == 0:
        admin = User(username="admin", role="admin")
        admin.set_password("Admin1234!")

        alice = User(username="alice", role="user")
        alice.set_password("Alice1234!")

        bob = User(username="bob", role="user")
        bob.set_password("Bob12345!")

        db.session.add_all([admin, alice, bob])
        db.session.commit()

        d1 = Document(
            title="Alice Confidential Notes",
            author="alice",
            content="Confidential project details belonging to Alice.",
            owner_id=alice.id
        )
        d2 = Document(
            title="Bob Private Report",
            author="bob",
            content="Private audit notes belonging to Bob.",
            owner_id=bob.id
        )
        db.session.add_all([d1, d2])
        db.session.commit()
