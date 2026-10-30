# CloudVault — DevSecOps Secure Engineering Sprint
### CYC386: Secure Software Design and Development (Fall 2026)
**Department of Computer Science, COMSATS University Islamabad**  
**Instructor:** Engr. Muhammad Ahmad Nawaz  

---

## Team Information
* **Muhammad Tallat** (`FA23-BCT-029`) — Lead Architect & Core Security Engineer
* **Sadat Ali** (`FA23-BCT-034`) — Threat Modeling & Native AppSec Engineer
* **Hassaan Shakoor** (`FA23-BCT-054`) — DevSecOps & QA Automation Engineer

---

## 1. Project Overview
CloudVault is an enterprise document repository and DevOps platform developed during a 1-week DevSecOps security sprint. The application demonstrates the identification, lab reproduction, and production hardening of five mandatory vulnerability classes:
1. **Buffer Overflow (CWE-120):** In native C binary metadata parser.
2. **OS Command Injection (CWE-78):** In DevOps network diagnostic ping utility.
3. **Insecure Direct Object Reference - IDOR (CWE-639):** In document retrieval routes.
4. **Cross-Site Request Forgery - CSRF (CWE-352):** In document ownership transfer.
5. **Clickjacking (CWE-1021):** In administrative management console.

---

## 2. Quick Start Guide

### Step 1: Install Dependencies
Ensure Python 3.10+ is installed on your machine.
```bash
pip install -r requirements.txt
```

### Step 2: Compile Native C Parser (WSL / Linux)
```bash
cd native_parser
make clean
make
cd ..
```
*Compiled artifacts include `parser_vulnerable`, `parser_secure`, and `libparser_secure.so`.*

### Step 3: Run Application
CloudVault supports two runtime modes:

#### Hardened Production Mode (Secure Defenses Active):
```bash
python run.py --mode secure --port 5000
```
*Enforces object-level authorization, anti-CSRF synchronizer tokens, parameterization, and anti-framing headers (`X-Frame-Options: DENY`).*

#### Lab Demonstration Mode (Vulnerabilities Enabled):
```bash
python run.py --mode vulnerable --port 5000
```
*Allows observing and testing the vulnerabilities in a safe, controlled local environment.*

Open your browser at `http://127.0.0.1:5000`.

---

## 3. Pre-seeded Demo Accounts

| Username | Password | Role | Description |
|:---|:---|:---:|:---|
| `admin` | `Admin1234!` | admin | System Administrator with management console access |
| `alice` | `Alice1234!` | user | Standard tenant; owns Document #1 (Confidential Notes) |
| `bob` | `Bob12345!` | user | Standard tenant; owns Document #2 (Private Report) |

---

## 4. Running Automated Tests & Security Scans

### Run Complete Pytest Suite (27 Test Cases):
```bash
python -m pytest tests/ -v
```

### Run Static Application Security Testing (SAST - Bandit):
```bash
python scripts/run_sast.py
```

### Run Dynamic Application Security Testing (DAST):
```bash
# Test in vulnerable mode (shows 2 High findings and fails gate):
python scripts/run_dast.py vulnerable reports/dast_vulnerable_report.json

# Test in secure mode (shows 0 High findings and passes gate):
python scripts/run_dast.py secure reports/dast_secure_report.json
```

### Compile PDF Reports:
```bash
python scripts/generate_pdf_reports.py
```

---

## 5. Docker Deployment

Build and run CloudVault inside a hardened, unprivileged container:
```bash
docker compose up --build
```
Access the application at `http://localhost:5000`.

---

## 6. Deliverables & Documentation Index

| Deliverable | Description | Location |
|:---|:---|:---|
| **PNE Report** | Asset inventory, elicited protection needs, and explicit CIA triad mapping | [`PNE_Report.md`](file:///d:/Uni/7th%20sem/SSDD/lab%20mid/PNE_Report.md) / `PNE_Report.pdf` |
| **Threat Model** | DFD Level-0/1, STRIDE analysis, Attack Trees, and CVSS v3.1 scoring | [`THREAT_MODEL.md`](file:///d:/Uni/7th%20sem/SSDD/lab%20mid/THREAT_MODEL.md) / `THREAT_MODEL.pdf` |
| **Security Implementation** | Before/after code, root-cause analysis, compiler flags, and fixes | [`SECURITY_IMPLEMENTATION.md`](file:///d:/Uni/7th%20sem/SSDD/lab%20mid/SECURITY_IMPLEMENTATION.md) |
| **Security Test Report** | SAST, DAST, and CI/CD security gate fail-on-critical evidence | [`SECURITY_TEST_REPORT.md`](file:///d:/Uni/7th%20sem/SSDD/lab%20mid/SECURITY_TEST_REPORT.md) |
| **Final IEEE Report** | 18–30 page structured comprehensive DevSecOps report | [`FINAL_REPORT.md`](file:///d:/Uni/7th%20sem/SSDD/lab%20mid/FINAL_REPORT.md) / `FINAL_REPORT.pdf` |
| **Live Sprint Board (GitHub)** | 18 traceable sprint items (Approved Equivalent per Section 6.1) | [GitHub Issues Board](https://github.com/Ab-fatir/SecureApp-Sprint-CyberSecTrio/issues?q=is%3Aissue) |
| **Jira Sprint Backlog** | Full traceability (PNE -> Threat -> Fix -> Test) | [`JIRA_SPRINT_BACKLOG.md`](file:///d:/Uni/7th%20sem/SSDD/lab%20mid/JIRA_SPRINT_BACKLOG.md) / `jira_backlog_export.csv` |
| **Demo Video Script** | Timed 6–10 minute step-by-step recording guide | [`DEMO_VIDEO_SCRIPT.md`](file:///d:/Uni/7th%20sem/SSDD/lab%20mid/DEMO_VIDEO_SCRIPT.md) |
| **CI/CD Pipeline** | GitHub Actions multi-stage workflow with automated gates | [`.github/workflows/ci-cd.yml`](file:///d:/Uni/7th%20sem/SSDD/lab%20mid/.github/workflows/ci-cd.yml) |
