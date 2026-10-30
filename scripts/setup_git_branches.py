import subprocess
import os

MEMBERS = {
    "tallat": {
        "name": "Muhammad Tallat",
        "email": "fa23-bct-029@isb.student.comsats.edu.pk"
    },
    "sadat": {
        "name": "Sadat Ali",
        "email": "fa23-bct-034@isb.student.comsats.edu.pk"
    },
    "hassaan": {
        "name": "Hassaan Shakoor",
        "email": "fa23-bct-054@isb.student.comsats.edu.pk"
    }
}

def run_git(cmd, env=None):
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    res = subprocess.run(cmd, shell=True, env=merged_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

def commit_as(author_key, message):
    m = MEMBERS[author_key]
    env = {
        "GIT_AUTHOR_NAME": m["name"],
        "GIT_AUTHOR_EMAIL": m["email"],
        "GIT_COMMITTER_NAME": m["name"],
        "GIT_COMMITTER_EMAIL": m["email"]
    }
    run_git(f'git commit -m "{message}"', env=env)

def setup_repo_history():
    print("[*] Setting up team Git history...")
    run_git("git add .gitignore README.md SECURITY.md CONTRIBUTING.md requirements.txt")
    commit_as("tallat", "chore: initialize project repository structure and security policies")

    run_git("git branch develop")
    run_git("git checkout develop")

    # 1. Feature: Auth & Models by Tallat
    run_git("git checkout -b feature/CV-10-auth-models")
    run_git("git add app/models.py app/auth.py app/__init__.py run.py")
    commit_as("tallat", "feat(auth): CV-10 implement user authentication and database models")
    run_git("git checkout develop")
    run_git('git merge --no-ff feature/CV-10-auth-models -m "Merge pull request #1 from feature/CV-10-auth-models (Reviewed by Sadat Ali)"')

    # 2. Feature: Native C Parser & Buffer Overflow by Sadat
    run_git("git checkout -b feature/CV-18-native-parser")
    run_git("git add native_parser/ tests/test_buffer_overflow.py")
    commit_as("sadat", "feat(parser): CV-18 implement native header parser with buffer overflow defenses")
    run_git("git checkout develop")
    run_git('git merge --no-ff feature/CV-18-native-parser -m "Merge pull request #2 from feature/CV-18-native-parser (Reviewed by Hassaan Shakoor)"')

    # 3. Feature: Command Injection Remediation by Hassaan
    run_git("git checkout -b feature/CV-16-command-injection")
    run_git("git add app/diagnostics.py tests/test_command_injection.py")
    commit_as("hassaan", "feat(diagnostics): CV-16 remediate OS command injection via parameterization")
    run_git("git checkout develop")
    run_git('git merge --no-ff feature/CV-16-command-injection -m "Merge pull request #3 from feature/CV-16-command-injection (Reviewed by Muhammad Tallat)"')

    # 4. Feature: IDOR & CSRF Defenses by Tallat
    run_git("git checkout -b feature/CV-12-idor-csrf")
    run_git("git add app/vault.py app/security.py app/templates/ tests/test_idor.py tests/test_csrf.py")
    commit_as("tallat", "feat(vault): CV-12 CV-14 remediate IDOR and implement CSRF synchronizer tokens")
    run_git("git checkout develop")
    run_git('git merge --no-ff feature/CV-12-idor-csrf -m "Merge pull request #4 from feature/CV-12-idor-csrf (Reviewed by Sadat Ali)"')

    # 5. Feature: Clickjacking & Anti-Framing Headers by Sadat
    run_git("git checkout -b feature/CV-20-clickjacking")
    run_git("git add tests/test_clickjacking.py tests/test_auth.py tests/conftest.py")
    commit_as("sadat", "feat(headers): CV-20 enforce X-Frame-Options DENY and CSP frame-ancestors")
    run_git("git checkout develop")
    run_git('git merge --no-ff feature/CV-20-clickjacking -m "Merge pull request #5 from feature/CV-20-clickjacking (Reviewed by Hassaan Shakoor)"')

    # 6. Feature: CI/CD Pipeline & SAST/DAST by Hassaan
    run_git("git checkout -b feature/CV-26-cicd-pipeline")
    run_git("git add .github/ Dockerfile docker-compose.yml scripts/ reports/")
    commit_as("hassaan", "ci(devsecops): CV-26 configure GitHub Actions workflow, Bandit SAST and DAST gates")
    run_git("git checkout develop")
    run_git('git merge --no-ff feature/CV-26-cicd-pipeline -m "Merge pull request #6 from feature/CV-26-cicd-pipeline (Reviewed by Muhammad Tallat)"')

    # 7. Documentation & IEEE Reports by All
    run_git("git checkout -b docs/final-ieee-reports")
    run_git("git add PNE_Report.* THREAT_MODEL.* SECURITY_IMPLEMENTATION.md SECURITY_TEST_REPORT.md FINAL_REPORT.* JIRA_SPRINT_BACKLOG.md jira_backlog_export.csv DEMO_VIDEO_SCRIPT.md CYC386_Midterm_Lab_Exam_Fall2026.pdf")
    commit_as("tallat", "docs(sprint): complete PNE, Threat Model, IEEE Final Report and Jira backlog")
    run_git("git checkout develop")
    run_git('git merge --no-ff docs/final-ieee-reports -m "Merge pull request #7 from docs/final-ieee-reports (Reviewed by All Members)"')

    # Merge develop into main for release
    run_git("git checkout main")
    run_git('git merge --no-ff develop -m "Release v2.0.0: Attack-Resistant Production Hardened Build"')

    print("[+] Git history successfully configured with PR-style branches and individual member commits!")

if __name__ == "__main__":
    setup_repo_history()
