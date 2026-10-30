# Security Test Report: SAST, DAST & CI/CD Pipeline Verification
**Project:** CloudVault — Enterprise Secure Document & DevOps Artifact Collaboration Hub  
**Course:** CYC386 — Secure Software Design and Development (Fall 2026)  
**Instructor:** Engr. Muhammad Ahmad Nawaz  
**Sprint:** 1-Week DevSecOps Security Engineering Sprint  
**Team Members:**  
1. **Muhammad Tallat** (FA23-BCT-029) — Lead Architect & Secure Core Engineer  
2. **Sadat Ali** (FA23-BCT-034) — Threat Modeling & AppSec Engineer  
3. **Hassaan Shakoor** (FA23-BCT-054) — DevSecOps & QA Automation Engineer  

---

## 1. Executive Testing Summary
This report presents the objective verification results obtained across the CloudVault DevSecOps security sprint. Testing incorporates **Static Application Security Testing (SAST)** via Bandit, **Dynamic Application Security Testing (DAST)** via automated HTTP baseline scanning (OWASP ZAP equivalent), **Unit and Security Regression Testing** via `pytest`, and **CI/CD Security Gate Enforcement** within GitHub Actions.

All tests validate our **Fail-on-Critical / Fail-on-High** gate policy, providing verifiable before-and-after evidence.

---

## 2. Static Application Security Testing (SAST) Results

### 2.1 Tooling & Configuration
* **Tool:** Bandit v1.9.4 (Security linter for Python)
* **Configuration:** Scans all application code (`app/`), evaluates severity thresholds (Low, Medium, High), outputs JSON and text audit logs.
* **Gate Policy:** Non-zero exit code on any High severity finding.

### 2.2 SAST Scan Findings: Before vs. After Remediation

| Metric | Before Remediation (Vulnerable State) | After Remediation (Secured Production State) |
|:---|:---:|:---:|
| **Total Lines Scanned** | 482 | 510 |
| **High Severity Issues** | **1** (`B605:start_process_with_a_shell`) | **0** |
| **Medium Severity Issues** | 0 | 0 |
| **Low Severity Issues** | 3 (Import checks) | 2 (Subprocess call verified) |
| **Security Gate Status** | :x: **FAILED (Exit Code 1)** | :white_check_mark: **PASSED (Exit Code 0)** |

### 2.3 Detailed Bandit SAST Finding & Remediation Proof

#### Finding 1: Command Injection in Diagnostics (Pre-Remediation)
```text
>> Issue: [B605:start_process_with_a_shell] Starting a process with a shell, possible injection detected.
   Severity: High   Confidence: High
   CWE: CWE-78 (https://cwe.mitre.org/data/definitions/78.html)
   Location: app/diagnostics.py:33:29
   32   # Deliberate vulnerability for educational demonstration
   33   raw_output = os.popen(cmd_str).read()
```
* **Remediation Status:** Remediated by replacing `os.popen()` with `subprocess.run(shell=False)` with argument isolation in `app/security.py` and strict regex whitelist validation.
* **Verification:** Re-running `bandit -r app/ -ll` (Medium and High severity filter) returns **0 High findings**, allowing the security gate to pass cleanly.

---

## 3. Dynamic Application Security Testing (DAST) Results

### 3.1 Tooling & Configuration
* **Engine:** CloudVault Automated DAST Baseline Scanner (`scripts/run_dast.py`), simulating OWASP ZAP core rulesets.
* **Target Scope:** All authentication endpoints, document retrieval routes, ownership transfer handlers, and administrative consoles.
* **Reports Stored:** `reports/dast_vulnerable_report.json` and `reports/dast_secure_report.json`.

### 3.2 DAST Scan Findings: Before vs. After Remediation

| Finding ID | Vulnerability Description | CWE | Target URL | Before Remediation | After Remediation |
|:---:|:---|:---:|:---|:---:|:---:|
| **DAST-01** | Insecure Direct Object Reference (IDOR) | CWE-639 | `/documents/2` | :red_circle: **CRITICAL (HTTP 200)** | :green_circle: **REMEDIATED (HTTP 403)** |
| **DAST-02** | Cross-Site Request Forgery (CSRF) | CWE-352 | `/documents/1/transfer` | :orange_circle: **HIGH (State Changed)** | :green_circle: **REMEDIATED (HTTP 403)** |
| **DAST-03** | Missing Anti-Framing (Clickjacking) | CWE-1021 | `/admin/console` | :orange_circle: **HIGH (Framable)** | :green_circle: **REMEDIATED (DENY)** |
| **DAST-04** | Missing MIME Sniffing Defense | CWE-693 | `/login` | :yellow_circle: **LOW (Header Absent)** | :green_circle: **REMEDIATED (nosniff)** |

### 3.3 DAST Execution Console Output

#### Vulnerable Mode Execution (Security Gate Fail Demonstration):
```text
[*] Starting DAST Security Scan against CloudVault in [VULNERABLE] mode...
============================================================
DAST SCAN COMPLETED [VULNERABLE]:
  Critical Findings: 1
  High Findings:     2
  Low Findings:      1
  Full report saved: reports/dast_vulnerable_report.json
============================================================
[HIGH] Improper Restriction of Rendered UI Layers (Clickjacking) at /admin/console (CWE-1021)
[HIGH] Cross-Site Request Forgery (CSRF) on Sensitive Transfer at /documents/1/transfer (CWE-352)
[CRITICAL] Insecure Direct Object Reference (IDOR) - Horizontal Privilege Escalation at /documents/2 (CWE-639)
[LOW] Missing X-Content-Type-Options Header at /login (CWE-693)

[!] DAST SECURITY GATE FAILED: Critical/High vulnerabilities detected! (Exit Code: 1)
```

#### Remediated Secure Mode Execution (Security Gate Pass Demonstration):
```text
[*] Starting DAST Security Scan against CloudVault in [SECURE] mode...
============================================================
DAST SCAN COMPLETED [SECURE]:
  Critical Findings: 0
  High Findings:     0
  Low Findings:      0
  Full report saved: reports/dast_secure_report.json
============================================================

[+] DAST SECURITY GATE PASSED: Zero Critical/High vulnerabilities found. (Exit Code: 0)
```

---

## 4. Automated Unit & Security Regression Testing (`pytest`)

A comprehensive suite of 27 automated tests was executed across the codebase:

```text
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.2.0, pluggy-1.7.0
rootdir: D:\Uni\7th sem\SSDD\lab mid
collected 27 items

tests\test_auth.py ....                                                  [ 14%]
tests\test_buffer_overflow.py ....                                       [ 29%]
tests\test_clickjacking.py ....                                          [ 44%]
tests\test_command_injection.py .......                                  [ 70%]
tests\test_csrf.py ....                                                  [ 85%]
tests\test_idor.py ....                                                  [100%]

====================== 27 passed, 0 failures in 10.25s =======================
```

### Coverage by Vulnerability Class:
1. **Authentication & Identity (`test_auth.py`):** 4 tests validating password hashing (Argon2/PBKDF2), complexity requirements, login flows, and unauthorized redirects.
2. **Buffer Overflow (`test_buffer_overflow.py`):** 4 tests validating magic byte checks, bounds checking, string clamping, and rejection of tampered lengths.
3. **Command Injection (`test_command_injection.py`):** 7 tests verifying regex whitelisting, parameterization, and explicit rejection of shell operators (`;`, `|`, `&`, `&&`, `$()`, backticks).
4. **IDOR Access Control (`test_idor.py`):** 4 tests verifying that cross-tenant document requests fail with HTTP 403 Forbidden, while legitimate owners and administrators retain authorized access.
5. **CSRF Synchronizer Tokens (`test_csrf.py`):** 4 tests verifying rejection of missing or tampered tokens with HTTP 403 Forbidden, and success with valid tokens.
6. **Clickjacking Defense (`test_clickjacking.py`):** 4 tests verifying `X-Frame-Options: DENY`, `frame-ancestors 'none'`, and `X-Content-Type-Options: nosniff`.

---

## 5. CI/CD Security Gate & Fail-on-Critical Enforcement

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) implements three sequential security gates:

1. **Gate 1: Build & Unit Test Verification:** Validates that native C code compiles with `-fstack-protector-strong` and all 27 unit tests pass.
2. **Gate 2: SAST Security Gate (Bandit):** Executes static analysis and terminates the pipeline if any High or Critical flaw is present.
3. **Gate 3: DAST Baseline Gate:** Runs dynamic HTTP requests against the application. Fails the build if any Critical or High vulnerability is flagged.
4. **Gate 4: Container Security Gate (Trivy):** Scans the Docker image for unpatched OS and library vulnerabilities before release.

All test reports, JUnit XML summaries, and Bandit JSON logs are retained as committed artifacts in `reports/`.
