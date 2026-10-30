from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import db, User, AuditLog

auth_bp = Blueprint("auth", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session or session.get("user_role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("vault.dashboard"))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if len(username) < 3 or len(password) < 8:
            flash("Username must be 3+ chars and password 8+ chars.", "danger")
            return render_template("register.html")

        if User.query.filter_by(username=username).first():
            flash("Username already exists.", "warning")
            return render_template("register.html")

        role = "admin" if User.query.count() == 0 else "user"
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        log = AuditLog(
            user_id=user.id,
            action="REGISTER",
            details=f"User {username} created",
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()

        flash("Registered successfully. Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.username
            session["user_role"] = user.role

            log = AuditLog(
                user_id=user.id,
                action="LOGIN",
                details=f"User {username} logged in",
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()

            return redirect(request.args.get("next") or url_for("vault.dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
