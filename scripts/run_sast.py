import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import subprocess

def run_bandit():
    os.makedirs("reports", exist_ok=True)
    report_file = "reports/sast_report.json"
    cmd = [
        sys.executable, "-m", "bandit",
        "-r", "app/",
        "-f", "json",
        "-o", report_file,
        "-s", "B605"
    ]
    
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if not os.path.exists(report_file):
        return 1

    with open(report_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    metrics = data.get("metrics", {}).get("_totals", {})
    high_count = metrics.get("SEVERITY.HIGH", 0)

    print(f"Bandit High Issues: {high_count}")
    return 2 if high_count > 0 else 0

if __name__ == "__main__":
    sys.exit(run_bandit())
