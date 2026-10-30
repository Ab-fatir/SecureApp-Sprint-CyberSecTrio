import os
from flask import Blueprint, render_template, request, flash, current_app
from app.auth import login_required
from app.security import safe_ping

diagnostics_bp = Blueprint("diagnostics", __name__)

@diagnostics_bp.route("/diagnostics", methods=["GET", "POST"])
@login_required
def network_diagnostics():
    result = None
    target_host = ""
    mode = current_app.config.get("SECURITY_MODE", "secure")

    if request.method == "POST":
        target_host = request.form.get("host", "").strip()

        if mode == "vulnerable":
            is_windows = os.name == "nt"
            cmd_str = f"ping -n 1 {target_host}" if is_windows else f"ping -c 1 {target_host}"
            try:
                raw_output = os.popen(cmd_str).read()
                result = {
                    "success": True,
                    "command": cmd_str,
                    "output": raw_output
                }
            except Exception as e:
                result = {"success": False, "error": str(e), "output": ""}
        else:
            result = safe_ping(target_host)
            if not result.get("success"):
                flash(result.get("error", "Ping failed"), "warning")

    return render_template("diagnostics.html", result=result, target_host=target_host, mode=mode)
