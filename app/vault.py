from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort, current_app
from app.models import db, User, Document, AuditLog
from app.auth import login_required, admin_required
from app.security import check_document_access, validate_csrf_token
from native_parser.parser_wrapper import MetadataParserWrapper

vault_bp = Blueprint("vault", __name__)

@vault_bp.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("vault.dashboard"))
    return redirect(url_for("auth.login"))

@vault_bp.route("/dashboard")
@login_required
def dashboard():
    user = db.session.get(User, session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    if user.role == "admin":
        docs = Document.query.order_by(Document.id.desc()).all()
    else:
        docs = Document.query.filter_by(owner_id=user.id).order_by(Document.id.desc()).all()

    return render_template("dashboard.html", user=user, documents=docs)

@vault_bp.route("/documents/upload", methods=["POST"])
@login_required
def upload_document():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    author = session.get("username", "Unknown")
    mode = current_app.config.get("SECURITY_MODE", "secure")

    header_file = request.files.get("header_file")
    if header_file and header_file.filename:
        raw_header = header_file.read()
        parser = MetadataParserWrapper(mode=mode)
        res = parser.parse_header(raw_header)
        if not res.get("success"):
            flash(f"Header error: {res.get('error')}", "danger")
            return redirect(url_for("vault.dashboard"))
        title = res.get("title", title)
        author = res.get("author", author)

    if not title or not content:
        flash("Title and content are required.", "warning")
        return redirect(url_for("vault.dashboard"))

    doc = Document(
        title=title,
        author=author,
        content=content,
        owner_id=session["user_id"]
    )
    db.session.add(doc)
    db.session.commit()

    flash("Document saved.", "success")
    return redirect(url_for("vault.dashboard"))

@vault_bp.route("/documents/<int:doc_id>")
@login_required
def view_document(doc_id):
    doc = db.session.get(Document, doc_id)
    if not doc:
        abort(404)

    current_user = db.session.get(User, session["user_id"])
    mode = current_app.config.get("SECURITY_MODE", "secure")

    if mode == "secure":
        if not check_document_access(doc, current_user):
            log = AuditLog(
                user_id=current_user.id,
                action="DENIED_DOCUMENT_ACCESS",
                details=f"Unauthorized access to document {doc_id}",
                ip_address=request.remote_addr
            )
            db.session.add(log)
            db.session.commit()
            abort(403)

    return render_template("document_detail.html", doc=doc, current_user=current_user)

@vault_bp.route("/documents/<int:doc_id>/transfer", methods=["POST"])
@login_required
def transfer_ownership(doc_id):
    doc = db.session.get(Document, doc_id)
    if not doc:
        abort(404)

    current_user = db.session.get(User, session["user_id"])
    mode = current_app.config.get("SECURITY_MODE", "secure")

    if mode == "secure":
        if not check_document_access(doc, current_user):
            abort(403)
        token = request.form.get("csrf_token")
        if not validate_csrf_token(token):
            abort(403)

    target_name = request.form.get("new_owner", "").strip()
    target_user = User.query.filter_by(username=target_name).first()
    if not target_user:
        flash("Target user not found.", "danger")
        return redirect(url_for("vault.view_document", doc_id=doc_id))

    doc.owner_id = target_user.id
    db.session.commit()

    flash(f"Ownership transferred to {target_name}.", "success")
    return redirect(url_for("vault.dashboard"))

@vault_bp.route("/admin/console")
@admin_required
def admin_console():
    users = User.query.all()
    logs = AuditLog.query.order_by(AuditLog.id.desc()).limit(20).all()
    return render_template("admin.html", users=users, logs=logs)

@vault_bp.route("/admin/clickjack-demo")
@admin_required
def clickjack_demo():
    return render_template("clickjack_demo.html")
