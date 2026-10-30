# CloudVault DevSecOps Sprint Backlog (Jira Traceability)

**Project:** SecureApp-Sprint-CyberSecTrio (CloudVault)  
**Live Jira Sprint Board:** [https://securebank-test123.atlassian.net/jira/software/projects/CV/boards/2](https://securebank-test123.atlassian.net/jira/software/projects/CV/boards/2)  
**Mirror GitHub Issues Board:** [https://github.com/Ab-fatir/SecureApp-Sprint-CyberSecTrio/issues](https://github.com/Ab-fatir/SecureApp-Sprint-CyberSecTrio/issues)  
**Team Members:**  
* **Muhammad Tallat** (FA23-BCT-029)  
* **Sadat Ali** (FA23-BCT-034)  
* **Hassaan Shakoor** (FA23-BCT-054)  

---

## 1. Sprint Epics

* **EPIC-1: Foundation, Protection Needs (PNE) & Repository Setup**
* **EPIC-2: Threat Modeling, STRIDE & CVSS Risk Analysis**
* **EPIC-3: Vulnerability Remediation & Secure Implementation (5 Vulnerability Classes)**
* **EPIC-4: DevSecOps CI/CD Pipeline & Automated Security Gates (SAST & DAST)**
* **EPIC-5: Security Verification, Documentation & Final IEEE Report**

---

## 2. Complete Traceability Matrix (PNE -> Threat -> Jira -> Fix -> Test)

| Issue Key | Type | Summary | Assignee | Status | PNE Ref | Threat (STRIDE) | Code / Fix | Verification Test |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---|:---|
| **CV-10** | Story | Setup User Authentication & Password Hashing | Muhammad Tallat | Done | PN-01 | T-06 (Information Disclosure) | `app/auth.py` (Argon2 / Werkzeug hash) | `tests/test_auth.py` |
| **CV-11** | Task | Setup SQLite Models and Database Migration | Muhammad Tallat | Done | PN-01 | T-06 (Information Disclosure) | `app/models.py` | `tests/test_auth.py` |
| **CV-12** | Story | Fix IDOR on Document Retrieval Endpoint | Muhammad Tallat | Done | PN-02 | T-03 (Information Disclosure - IDOR) | `app/vault.py` (`check_document_access`) | `tests/test_idor.py` |
| **CV-13** | Task | Add Ownership Check in Document Details View | Muhammad Tallat | Done | PN-02 | T-03 (IDOR) | `app/vault.py` (Line 80) | `tests/test_idor.py` |
| **CV-14** | Story | Fix CSRF on Document Ownership Transfer | Muhammad Tallat | Done | PN-03 | T-04 (Tampering / Spoofing - CSRF) | `app/security.py` (`generate_csrf_token`) | `tests/test_csrf.py` |
| **CV-15** | Task | Add Synchronizer Token to Transfer Form | Muhammad Tallat | Done | PN-03 | T-04 (CSRF) | `app/templates/document_detail.html` | `tests/test_csrf.py` |
| **CV-16** | Story | Fix OS Command Injection in Ping Diagnostics | Hassaan Shakoor | Done | PN-04 | T-02 (Elevation of Privilege - Command Injection) | `app/security.py` (`safe_ping`) | `tests/test_command_injection.py` |
| **CV-17** | Task | Implement Regex Host Whitelist and shell=False | Hassaan Shakoor | Done | PN-04 | T-02 (Command Injection) | `app/security.py` (HOST_PATTERN) | `tests/test_command_injection.py` |
| **CV-18** | Story | Fix Buffer Overflow in Native C Metadata Parser | Sadat Ali | Done | PN-05 | T-01 (Tampering / Memory Corruption) | `native_parser/metadata_parser_secure.c` | `tests/test_buffer_overflow.py` |
| **CV-19** | Task | Add Compiler Mitigations (-fstack-protector, ASAN) | Sadat Ali | Done | PN-05 | T-01 (Buffer Overflow) | `native_parser/Makefile` | WSL GCC build & ASAN |
| **CV-20** | Story | Fix Clickjacking on Admin Management Console | Sadat Ali | Done | PN-06 | T-05 (Tampering / UI Redressing) | `app/security.py` (`set_security_headers`) | `tests/test_clickjacking.py` |
| **CV-21** | Task | Add X-Frame-Options DENY and CSP frame-ancestors | Sadat Ali | Done | PN-06 | T-05 (Clickjacking) | `app/security.py` (Middleware) | `tests/test_clickjacking.py` |
| **CV-22** | Story | Implement Security Audit Logging | Muhammad Tallat | Done | PN-07 | T-07 (Repudiation) | `app/models.py` (`AuditLog`) | `app/vault.py` audit logs |
| **CV-24** | Story | Configure Bandit SAST Security Gate | Hassaan Shakoor | Done | PN-09 | T-02 (Command Injection) | `scripts/run_sast.py` | Bandit scan output |
| **CV-25** | Story | Configure DAST Dynamic Baseline Scan | Hassaan Shakoor | Done | PN-09 | T-03, T-04, T-05 | `scripts/run_dast.py` | DAST before/after reports |
| **CV-26** | Story | Build GitHub Actions CI/CD Pipeline | Hassaan Shakoor | Done | PN-09 | Pipeline integrity | `.github/workflows/ci-cd.yml` | GitHub Actions workflow |
| **CV-28** | Story | Dockerize Application with Non-Root User | Hassaan Shakoor | Done | PN-08 | Container security | `Dockerfile`, `docker-compose.yml` | Docker build |
| **CV-30** | Story | Write Comprehensive IEEE Final Project Report | All Members | Done | Documentation | Full project audit | `FINAL_REPORT.md` / `FINAL_REPORT.pdf` | Team submission |

---

## 3. How to Import into Jira

1. Open your Jira workspace (or GitHub Projects).
2. Go to **Project Settings -> Import Data -> CSV**.
3. Select the file `jira_backlog_export.csv` located in this project root.
4. Map the columns:
   * `Issue Key` -> Issue Key
   * `Type` -> Issue Type
   * `Summary` -> Summary
   * `Assignee` -> Assignee
   * `Status` -> Status
5. Click **Run Import**. Your board will immediately show the entire sprint with Done, In Progress, and To Do cards!
