import subprocess

ISSUES = [
    {
        "key": "CV-11",
        "type": "Task",
        "title": "Setup SQLite Database Models & Schema",
        "assignee": "Muhammad Tallat (FA23-BCT-029)",
        "pne": "PN-01",
        "threat": "T-06 (Information Disclosure)",
        "fix": "app/models.py (User, Document, AuditLog tables)",
        "test": "tests/test_auth.py"
    },
    {
        "key": "CV-12",
        "type": "Story",
        "title": "Fix Insecure Direct Object Reference (IDOR) on Document Retrieval",
        "assignee": "Muhammad Tallat (FA23-BCT-029)",
        "pne": "PN-02",
        "threat": "T-03 (Information Disclosure - CWE-639)",
        "fix": "app/vault.py (check_document_access tenancy filter)",
        "test": "tests/test_idor.py (Assert 403 Forbidden)"
    },
    {
        "key": "CV-13",
        "type": "Task",
        "title": "Add Ownership Verification Check in Document View Route",
        "assignee": "Muhammad Tallat (FA23-BCT-029)",
        "pne": "PN-02",
        "threat": "T-03 (IDOR)",
        "fix": "app/vault.py (Line 80)",
        "test": "tests/test_idor.py"
    },
    {
        "key": "CV-14",
        "type": "Story",
        "title": "Fix Cross-Site Request Forgery (CSRF) on Ownership Transfer",
        "assignee": "Muhammad Tallat (FA23-BCT-029)",
        "pne": "PN-03",
        "threat": "T-04 (Tampering / Spoofing - CWE-352)",
        "fix": "app/security.py (generate_csrf_token & secrets.compare_digest)",
        "test": "tests/test_csrf.py (Assert Token Verification)"
    },
    {
        "key": "CV-15",
        "type": "Task",
        "title": "Add Synchronizer CSRF Token in Transfer Form",
        "assignee": "Muhammad Tallat (FA23-BCT-029)",
        "pne": "PN-03",
        "threat": "T-04 (CSRF)",
        "fix": "app/templates/document_detail.html",
        "test": "tests/test_csrf.py"
    },
    {
        "key": "CV-16",
        "type": "Story",
        "title": "Fix OS Command Injection in Diagnostic Ping Utility",
        "assignee": "Hassaan Shakoor (FA23-BCT-054)",
        "pne": "PN-04",
        "threat": "T-02 (Elevation of Privilege - CWE-78)",
        "fix": "app/security.py (safe_ping with regex allowlist & shell=False)",
        "test": "tests/test_command_injection.py"
    },
    {
        "key": "CV-17",
        "type": "Task",
        "title": "Implement Regex Whitelist and shell=False Parameterization",
        "assignee": "Hassaan Shakoor (FA23-BCT-054)",
        "pne": "PN-04",
        "threat": "T-02 (Command Injection)",
        "fix": "app/security.py (HOST_PATTERN)",
        "test": "tests/test_command_injection.py"
    },
    {
        "key": "CV-18",
        "type": "Story",
        "title": "Fix Stack Buffer Overflow in Native C Metadata Parser",
        "assignee": "Sadat Ali (FA23-BCT-034)",
        "pne": "PN-05",
        "threat": "T-01 (Tampering / Memory Corruption - CWE-120)",
        "fix": "native_parser/metadata_parser_secure.c (bounded memcpy & magic bytes)",
        "test": "tests/test_buffer_overflow.py & ASAN build"
    },
    {
        "key": "CV-19",
        "type": "Task",
        "title": "Add Stack Canaries, FORTIFY_SOURCE, and ASAN Compiler Flags",
        "assignee": "Sadat Ali (FA23-BCT-034)",
        "pne": "PN-05",
        "threat": "T-01 (Buffer Overflow)",
        "fix": "native_parser/Makefile (-fstack-protector-strong, -D_FORTIFY_SOURCE=2)",
        "test": "native_parser/Makefile (make parser_asan)"
    },
    {
        "key": "CV-20",
        "type": "Story",
        "title": "Fix Clickjacking on Administrative Management Console",
        "assignee": "Sadat Ali (FA23-BCT-034)",
        "pne": "PN-06",
        "threat": "T-05 (Tampering / UI Redressing - CWE-1021)",
        "fix": "app/security.py (set_security_headers middleware)",
        "test": "tests/test_clickjacking.py (Assert X-Frame-Options: DENY)"
    },
    {
        "key": "CV-21",
        "type": "Task",
        "title": "Add X-Frame-Options DENY and CSP frame-ancestors 'none'",
        "assignee": "Sadat Ali (FA23-BCT-034)",
        "pne": "PN-06",
        "threat": "T-05 (Clickjacking)",
        "fix": "app/security.py",
        "test": "tests/test_clickjacking.py"
    },
    {
        "key": "CV-22",
        "type": "Story",
        "title": "Implement Security Audit Logging Engine",
        "assignee": "Muhammad Tallat (FA23-BCT-029)",
        "pne": "PN-07",
        "threat": "T-07 (Repudiation)",
        "fix": "app/models.py (AuditLog table & vault route logging)",
        "test": "app/vault.py audit entries"
    },
    {
        "key": "CV-24",
        "type": "Story",
        "title": "Configure Bandit SAST Security Gate in CI/CD Pipeline",
        "assignee": "Hassaan Shakoor (FA23-BCT-054)",
        "pne": "PN-09",
        "threat": "T-02 (Command Injection)",
        "fix": "scripts/run_sast.py (Fail on High severity finding)",
        "test": "CI Run #41044238995 (Failed) vs #41045169191 (Passed)"
    },
    {
        "key": "CV-25",
        "type": "Story",
        "title": "Configure Dynamic Application Security Testing (DAST Baseline Scan)",
        "assignee": "Hassaan Shakoor (FA23-BCT-054)",
        "pne": "PN-09",
        "threat": "T-03, T-04, T-05 (IDOR, CSRF, Clickjacking)",
        "fix": "scripts/run_dast.py (OWASP ZAP baseline equivalent)",
        "test": "reports/dast_vulnerable_report.json vs reports/dast_secure_report.json"
    },
    {
        "key": "CV-26",
        "type": "Story",
        "title": "Build GitHub Actions Multi-Stage Workflow with Fail-on-Critical",
        "assignee": "Hassaan Shakoor (FA23-BCT-054)",
        "pne": "PN-09",
        "threat": "Pipeline Integrity",
        "fix": ".github/workflows/ci-cd.yml",
        "test": "GitHub Actions live runs on main and develop"
    },
    {
        "key": "CV-28",
        "type": "Story",
        "title": "Dockerize Application with Non-Root User Execution",
        "assignee": "Hassaan Shakoor (FA23-BCT-054)",
        "pne": "PN-08",
        "threat": "Container Privilege Escalation",
        "fix": "Dockerfile & docker-compose.yml (cloudvault user UID 10001)",
        "test": "docker compose up --build"
    },
    {
        "key": "CV-30",
        "type": "Story",
        "title": "Compile IEEE-Style Final Project Report & Demo Video Script",
        "assignee": "All Members",
        "pne": "Documentation",
        "threat": "Sprint Compliance",
        "fix": "FINAL_REPORT.pdf, DEMO_VIDEO_SCRIPT.md, demo_video.mp4",
        "test": "scripts/generate_pdf_reports.py"
    }
]

def main():
    repo = "Ab-fatir/SecureApp-Sprint-CyberSecTrio"
    print(f"[*] Populating GitHub Issues board on {repo}...")
    
    for item in ISSUES:
        title = f"[{item['key']}][{item['type']}] {item['title']}"
        body = (
            f"**Issue Key:** `{item['key']}`\n\n"
            f"**Type:** `{item['type']}`\n\n"
            f"**Assignee:** {item['assignee']}\n\n"
            f"**Protection Need (PNE):** `{item['pne']}`\n\n"
            f"**STRIDE Threat Ref:** `{item['threat']}`\n\n"
            f"**Implementation / Fix:** `{item['fix']}`\n\n"
            f"**Verification Test:** `{item['test']}`\n\n"
            f"**Status:** `Done` (Resolved in sprint)"
        )
        
        cmd_create = [
            "gh", "issue", "create",
            "-R", repo,
            "--title", title,
            "--body", body
        ]
        res = subprocess.run(cmd_create, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        issue_url = res.stdout.strip()
        print(f"[+] Created {item['key']}: {issue_url}")
        
        issue_num = issue_url.split("/")[-1]
        cmd_close = [
            "gh", "issue", "close", issue_num,
            "-R", repo,
            "--comment", f"Completed and verified in sprint feature branch by {item['assignee']}"
        ]
        subprocess.run(cmd_close, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("[*] All sprint issues created and marked as Done!")

if __name__ == "__main__":
    main()
