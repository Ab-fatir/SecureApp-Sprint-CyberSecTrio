import os
import zipfile

def create_clean_submission_zip():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    zip_filename = os.path.join(base_dir, "CYC386_Midterm_Sprint_FA23-BCT-029_FA23-BCT-034_FA23-BCT-054.zip")
    
    # Exact required files at root level
    root_files = [
        "FINAL_REPORT.pdf",
        "FINAL_REPORT.md",
        "PNE_Report.pdf",
        "PNE_Report.md",
        "THREAT_MODEL.pdf",
        "THREAT_MODEL.md",
        "SECURITY_IMPLEMENTATION.md",
        "SECURITY_TEST_REPORT.md",
        "JIRA_SPRINT_REPORT.pdf",
        "JIRA_SPRINT_REPORT.md",
        "JIRA_SPRINT_BACKLOG.md",
        "jira_backlog_export.csv",
        "DEMO_VIDEO_SCRIPT.md",
        "demo_video.mp4",
        "SUBMISSION_INFO.txt",
        "README.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt",
        "run.py"
    ]
    
    # Exact directories to include
    include_directories = [
        ("app", True),
        ("native_parser", True),
        ("tests", True),
        ("reports", True),
        (".github/workflows", True)
    ]
    
    # Scripts to include (only officially required runners)
    scripts_to_include = [
        "scripts/run_sast.py",
        "scripts/run_dast.py",
        "scripts/generate_pdf_reports.py",
        "scripts/generate_demo_video.py"
    ]

    print(f"[*] Packaging CLEAN final submission archive: {os.path.basename(zip_filename)}...")
    
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 1. Add root files
        for f in root_files:
            p = os.path.join(base_dir, f)
            if os.path.exists(p):
                zipf.write(p, f)
                print(f"  + Added: {f}")
            else:
                print(f"  ! Warning: {f} not found!")

        # 2. Add directories
        for rel_dir, _ in include_directories:
            full_dir = os.path.join(base_dir, rel_dir)
            if not os.path.exists(full_dir):
                continue
            for root, dirs, files in os.walk(full_dir):
                dirs[:] = [d for d in dirs if d not in {"__pycache__", ".pytest_cache"}]
                for file in files:
                    if file.endswith((".pyc", ".pyo")):
                        continue
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, base_dir)
                    zipf.write(full_p, rel_p)
                    print(f"  + Added: {rel_p}")

        # 3. Add scripts
        for s in scripts_to_include:
            p = os.path.join(base_dir, s)
            if os.path.exists(p):
                zipf.write(p, s)
                print(f"  + Added: {s}")

    size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
    print(f"\n[+] Final clean archive created: {os.path.basename(zip_filename)} ({size_mb:.2f} MB)")
    
    # Create the alias copy
    alias_zip = os.path.join(base_dir, "SecureApp-Sprint-CyberSecTrio.zip")
    import shutil
    shutil.copyfile(zip_filename, alias_zip)
    print(f"[+] Created mirror copy: {os.path.basename(alias_zip)}")

if __name__ == "__main__":
    create_clean_submission_zip()
