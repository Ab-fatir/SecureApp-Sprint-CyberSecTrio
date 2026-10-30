import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from app import create_app
from tests.conftest import login_client

def run_dast(mode="secure", report_path="reports/dast_report.json"):
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    app = create_app(mode=mode, test_config={"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    client = app.test_client()

    findings = []

    login_client(client, "admin", "Admin1234!")
    resp = client.get("/admin/console")
    if "X-Frame-Options" not in resp.headers:
        findings.append({
            "name": "Clickjacking",
            "severity": "High",
            "url": "/admin/console"
        })

    login_client(client, "alice", "Alice1234!")
    csrf_resp = client.post("/documents/1/transfer", data={"new_owner": "bob"})
    if csrf_resp.status_code == 200:
        findings.append({
            "name": "CSRF on Transfer",
            "severity": "High",
            "url": "/documents/1/transfer"
        })

    idor_resp = client.get("/documents/2")
    if idor_resp.status_code == 200 and b"Bob Private Report" in idor_resp.data:
        findings.append({
            "name": "IDOR on Document View",
            "severity": "Critical",
            "url": "/documents/2"
        })

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(findings, f, indent=2)

    high_count = sum(1 for f in findings if f["severity"] in ["Critical", "High"])
    print(f"DAST mode={mode} Critical/High findings: {high_count}")
    return 1 if high_count > 0 else 0

if __name__ == "__main__":
    mode_arg = sys.argv[1] if len(sys.argv) > 1 else "secure"
    out_arg = sys.argv[2] if len(sys.argv) > 2 else f"reports/dast_{mode_arg}_report.json"
    sys.exit(run_dast(mode=mode_arg, report_path=out_arg))
