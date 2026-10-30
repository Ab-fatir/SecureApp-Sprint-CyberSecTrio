# CloudVault: Design and Implementation of an Attack-Resistant Enterprise Collaboration Platform
### CYC386 — Secure Software Design and Development | Midterm DevSecOps Sprint Report
**Department of Computer Science, COMSATS University Islamabad**  
**Instructor:** Engr. Muhammad Ahmad Nawaz  
**Semester:** Fall 2026  

---

### Authors & Team Information
* **Muhammad Tallat** — Registration No: `FA23-BCT-029`  
  *Role:* Lead Architect & Secure Core Engineer (Authentication, IDOR & Access Control)
* **Sadat Ali** — Registration No: `FA23-BCT-034`  
  *Role:* Threat Modeling & AppSec Engineer (Native C Memory Safety, CSRF & Clickjacking)
* **Hassaan Shakoor** — Registration No: `FA23-BCT-054`  
  *Role:* DevSecOps & QA Automation Engineer (CI/CD Pipeline, SAST/DAST Gates & Command Injection)

---

## Abstract
This report documents the design, threat modeling, vulnerability remediation, and automated security verification of **CloudVault**, an enterprise-grade secure document repository and DevOps artifact management system. Developed within a time-boxed 7-day DevSecOps security sprint for CYC386, this project demonstrates end-to-end security engineering. We conducted Protection Needs Elicitation (PNE) mapping all assets to the CIA triad, generated Level-0 and Level-1 Data Flow Diagrams (DFDs), applied systematic STRIDE threat modeling, constructed Attack Trees, and scored risks quantitatively using CVSS v3.1. We then identified, safely demonstrated in a controlled lab environment, and fully remediated five mandatory vulnerability classes: Stack Buffer Overflow (CWE-120), OS Command Injection (CWE-78), Insecure Direct Object Reference (CWE-639), Cross-Site Request Forgery (CWE-352), and Clickjacking (CWE-1021). Our solution integrates compiler defenses (`-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, ASLR, NX), an automated GitHub Actions CI/CD pipeline with fail-on-critical security gates (Bandit SAST, DAST baseline scanning), and containerized deployment. Full traceability is maintained across Jira, code commits, pull requests, and automated verification test suites.

---

## 1. Introduction and Objectives

Modern software engineering increasingly demands that security be integrated continuously into every phase of the software development lifecycle—a methodology known as DevSecOps. In fast-paced software environments, applications frequently suffer from common design and implementation flaws, including memory corruption, broken access controls, and unsafe operating system invocations.

The objective of this CYC386 Midterm Lab Exam is to undertake an industry-style security engineering sprint to transform an unhardened application into an attack-resistant, production-grade system. Specifically, the sprint achieves:
1. **Protection Needs Elicitation (PNE):** Systematically categorizing data, process, and system assets, and linking each protection need to the Confidentiality, Integrity, and Availability (CIA) triad (CDF Unit 2).
2. **Threat Modeling & Risk Assessment:** Creating DFDs with clear trust boundaries, applying STRIDE, modeling multi-stage attack scenarios via Attack Trees, and calculating CVSS v3.1 scores (CDF Unit 3).
3. **Core Defensive Engineering:** Remediating five mandatory vulnerability classes (Buffer Overflow, Command Injection, IDOR, CSRF, Clickjacking) using safe APIs, input validation, and architectural controls (CDF Unit 5).
4. **DevSecOps Pipeline Automation:** Constructing a CI/CD pipeline using GitHub Actions that enforces static analysis (SAST) and dynamic scanning (DAST) with a strict fail-on-critical build policy.
5. **Traceability and Hygiene:** Maintaining end-to-end traceability across Jira issues (`CV-XX`), Git feature branches, pull requests, peer reviews, and automated test cases.

---

## 2. System Architecture and Design

CloudVault is structured around a modular client-server architecture with an isolated native parsing helper.

### 2.1 Core Architectural Components
1. **Web Presentation & REST Layer:** Developed in Python using the Flask framework. Handles user authentication, session state, document management, and DevOps health monitoring.
2. **Native C Binary Metadata Parser (`libparser_secure.so`):** A high-performance native component written in C (C11 standard) that parses custom `.cvlt` binary file headers. It executes with bounded memory copies and compiler mitigations.
3. **Centralized Security Layer (`app/security.py`):** Centralizes all authorization checks, CSRF token validation, input sanitization regex filters, and HTTP response security headers.
4. **Relational Persistence Layer:** Uses SQLAlchemy with an SQLite database (configured for clean transition to PostgreSQL in containerized environments).
5. **DevSecOps Testing & CI/CD Framework:** Combines `pytest` (27 unit and integration tests), Bandit for SAST, automated HTTP scripts for DAST, and Docker for deployment.

### 2.2 Trust Boundaries and Component Isolation
The system enforces three primary trust boundaries:
* **Trust Boundary 1 (Untrusted Client Boundary):** Separates untrusted web browsers and network adversaries from the web application entry points.
* **Trust Boundary 2 (Application Layer Boundary):** Encloses the Flask WSGI process and session manager. All inputs crossing this boundary undergo strict schema validation and sanitization.
* **Trust Boundary 3 (Host OS & Persistence Boundary):** Isolates the application runtime from the host kernel and database storage. The application executes under an unprivileged user account (`cloudvault`, UID 10001), preventing privilege escalation to root.

---

## 3. Protection Needs Elicitation (PNE) & CIA Triad Mapping

In accordance with CDF Unit 2, protection needs were elicited across all stakeholders and assets.

### 3.1 Comprehensive Asset Inventory
* **Data Assets:**
  * `DA-01`: User credentials, password hashes, and session cookies.
  * `DA-02`: Confidential documents and proprietary project files.
  * `DA-03`: Document metadata (author names, titles, timestamps).
  * `DA-04`: Security audit logs (login attempts, ownership transfers, access denials).
* **Process Assets:**
  * `PA-01`: Authentication and password verification engine.
  * `PA-02`: Native C binary header parser (`CVLT`).
  * `PA-03`: DevOps network health diagnostic utility.
  * `PA-04`: Object-level document access controller.
  * `PA-05`: State-changing ownership transfer routine.
* **System Assets:**
  * `CA-01`: Flask WSGI web application runtime.
  * `CA-02`: Persistent database store.
  * `CA-03`: Native shared library (`libparser_secure.so`).
  * `CA-04`: Host operating system shell and filesystem.

### 3.2 Explicit CIA Mapping Table

| Need ID | Asset Ref | Protection Need Description | CIA Triad Mapping | Measurable Security Requirement | Jira Issue |
|:---:|:---:|:---|:---:|:---|:---:|
| **PN-01** | DA-01 | User passwords must be stored using strong one-way salted hashes to prevent cracking if the database is exposed. | **Confidentiality** | **SR-01:** Passwords hashed with PBKDF2/Argon2. Cookies set with `HttpOnly` and `SameSite=Strict`. | `CV-10` |
| **PN-02** | DA-02 | Documents must be viewable only by their creator or an administrator. | **Confidentiality** | **SR-02:** Every document view route must verify `doc.owner_id == user.id`. Unauthorized access returns HTTP 403. | `CV-12` |
| **PN-03** | PA-05 | Ownership transfers must execute only when deliberately initiated by the authenticated user. | **Integrity** | **SR-03:** State-changing POST requests must require a valid anti-CSRF synchronizer token. | `CV-14` |
| **PN-04** | CA-04 | User inputs to diagnostics must never execute shell commands on the host server. | **Integrity & Availability** | **SR-04:** Use `subprocess.run(shell=False)` with argument arrays and strict regex whitelist `^[a-zA-Z0-9.-]+$`. | `CV-16` |
| **PN-05** | PA-02, CA-03 | Native binary parsing must never overflow memory buffers or hijack control flow. | **Integrity & Availability** | **SR-05:** Validate `CVLT` magic bytes, check lengths, use bounded `memcpy`/`snprintf`, compile with `-fstack-protector-strong`. | `CV-18` |
| **PN-06** | CA-01 | Sensitive admin panels must not be framed in malicious third-party websites. | **Integrity & Confidentiality** | **SR-06:** Inject `X-Frame-Options: DENY` and CSP `frame-ancestors 'none'` on all responses. | `CV-20` |
| **PN-07** | DA-04 | Audit logs must record all security events to ensure accountability. | **Integrity & Repudiation** | **SR-07:** Store timestamp, user ID, event type, and IP address for all sensitive actions. | `CV-22` |
| **PN-08** | CA-01 | Large payloads or slow diagnostics must not exhaust server memory or CPU. | **Availability** | **SR-08:** Binary payloads capped at 4096 bytes; diagnostic processes enforce a 5-second timeout. | `CV-24` |
| **PN-09** | CA-01 | High and critical vulnerabilities must block deployment to production. | **Integrity & Availability** | **SR-09:** CI/CD pipeline runs SAST and DAST, failing with a non-zero exit code on critical findings. | `CV-26` |

---

## 4. Threat Modeling, STRIDE & Quantitative Risk Assessment

In accordance with CDF Unit 3, threat modeling was conducted systematically across all elements of the Level-1 Data Flow Diagram.

### 4.1 STRIDE Threat Analysis Matrix

| Threat ID | Element | STRIDE Category | Threat Description | CIA Impact | Unmitigated CVSS v3.1 | Jira Key |
|:---:|:---|:---|:---|:---:|:---:|:---:|
| **T-01** | Process 4.0 (Native Parser) | **Tampering / Elevation of Privilege** | An attacker uploads a binary header exceeding 32 bytes, causing a stack buffer overflow in `strcpy` that overwrites the saved return address. | Integrity, Availability | **8.8 (High)** | `CV-18` |
| **T-02** | Process 3.0 (Diagnostics) | **Elevation of Privilege** | User submits `127.0.0.1; whoami` to the ping diagnostic, executing arbitrary shell commands via `os.popen(shell=True)`. | Confidentiality, Integrity, Availability | **9.9 (Critical)** | `CV-16` |
| **T-03** | Process 2.0 (Document Vault) | **Information Disclosure** | An authenticated user increments the document ID in `/documents/<id>` to view another tenant's confidential files (IDOR). | Confidentiality | **6.5 (Medium/High)** | `CV-12` |
| **T-04** | Process 2.0 (Ownership Transfer) | **Tampering / Spoofing** | An attacker tricks an authenticated user into visiting a page that submits a background POST to `/documents/<id>/transfer` without a CSRF token. | Integrity | **6.5 (Medium/High)** | `CV-14` |
| **T-05** | Process 2.0 (Admin Console) | **Tampering / Spoofing** | Attacker embeds `/admin/console` in an iframe with a transparent UI overlay to trick the admin into clicking sensitive buttons (Clickjacking). | Integrity | **4.3 (Medium)** | `CV-20` |

### 4.2 Attack Trees

#### Attack Tree 1: Remote Code Execution via Command Injection (Threat T-02)
* **Target:** Gain arbitrary command execution on the host operating system.
  * **Path 1.1:** Locate unauthenticated administrative debug script (Blocked: authentication enforced).
  * **Path 1.2:** Exploit network diagnostic tool via command chaining operators:
    * *Step 1:* Authenticate as standard user.
    * *Step 2:* Navigate to `/diagnostics`.
    * *Step 3:* Inject command separator `; whoami` or `&& dir`.
    * *Step 4:* Server invokes `os.popen()` with shell interpretation.
    * *Step 5:* Arbitrary command executes with server permissions.
  * *Defense Applied:* Replaced shell invocation with `subprocess.run(shell=False)` using an argument list, combined with a strict regex whitelist (`^[a-zA-Z0-9.-]+$`).

#### Attack Tree 2: Privilege Escalation via Stack Buffer Overflow (Threat T-01)
* **Target:** Overwrite stack frame and seize process control flow.
  * **Path 2.1:** Exploit heap allocation in image parser (Not present).
  * **Path 2.2:** Exploit stack buffer in custom document header parser:
    * *Step 1:* Craft binary payload exceeding 32 bytes.
    * *Step 2:* Upload payload via `/documents/upload`.
    * *Step 3:* Native parser executes unbounded `strcpy()` into stack buffer.
    * *Step 4:* Overwrite adjacent memory, stack canary, and saved return address.
    * *Step 5:* Trigger segmentation fault or redirect execution.
  * *Defense Applied:* Replaced `strcpy` with bounded `memcpy`/`snprintf`, validated magic bytes and length limits, and compiled with `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, ASLR, and NX/DEP.

### 4.3 CVSS v3.1 Quantitative Scoring

| Threat ID | Threat Class | CVSS v3.1 Vector String | Score | Severity | Vector Justification |
|:---:|:---:|:---|:---:|:---:|:---|
| **T-01** | Buffer Overflow | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` | **8.8** | **High** | Network accessible; low attack complexity; standard user privileges; high impact across confidentiality, integrity, and availability. |
| **T-02** | Command Injection | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` | **9.9** | **Critical** | Network accessible; low complexity; authenticated user; scope changed (`S:C`) because injection escapes Python into the host OS shell. |
| **T-03** | IDOR | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` | **6.5** | **Medium** | Simple parameter tampering; direct breach of confidentiality across tenants. |
| **T-04** | CSRF | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N` | **6.5** | **Medium** | Requires user interaction; unauthorized state change compromises data integrity. |
| **T-05** | Clickjacking | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N` | **4.3** | **Medium** | Missing anti-framing headers; requires user interaction; low integrity impact. |

---

## 5. Detailed Vulnerability Remediation & Secure Implementation

### 5.1 Buffer Overflow in Native C Metadata Parser (CWE-120)
* **Vulnerable State:** `metadata_parser_vulnerable.c` allocated a 32-byte stack buffer and invoked `strcpy(stack_author_buffer, payload)` without verifying input length. When tested with 64 bytes of input, the program crashed with `*** stack smashing detected ***: terminated`. AddressSanitizer flagged a stack-buffer-overflow write error.
* **Secure Remediation:** In `metadata_parser_secure.c`:
  1. Validated header magic bytes (`CVLT`).
  2. Enforced maximum payload limit of 4096 bytes.
  3. Checked that declared length does not exceed actual buffer size.
  4. Used bounded copies (`memcpy`) with guaranteed null-termination: `out_author[author_len] = '\0'`.
* **Compiler Defenses:** Compiled with `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, `-fPIE -pie`, `-Wl,-z,relro,-z,now`, and `-Wl,-z,noexecstack`.

### 5.2 OS Command Injection in DevOps Diagnostics (CWE-78)
* **Vulnerable State:** `app/diagnostics.py` passed user input directly into `os.popen(f"ping -c 1 {target_host}").read()`. Entering `127.0.0.1; whoami` caused the shell to execute `whoami`.
* **Secure Remediation:** In `app/security.py`:
  1. Input validated against strict regex: `^[a-zA-Z0-9.-]+$`. Any semicolon, pipe, ampersand, or backtick is immediately rejected.
  2. Executed via `subprocess.run(["ping", "-c", "1", target], shell=False, timeout=5)`. Because `shell=False` is set, arguments are passed directly to the operating system's `execve` call without invoking a shell interpreter.

### 5.3 Insecure Direct Object Reference - IDOR (CWE-639)
* **Vulnerable State:** `app/vault.py` retrieved documents using `db.session.get(Document, doc_id)` and rendered the template without checking whether the logged-in user owned the document. User Alice was able to view User Bob's private financial report simply by changing `/documents/1` to `/documents/2`.
* **Secure Remediation:** Implemented centralized ownership verification:
  ```python
  def check_document_access(document, user):
      if not user:
          return False
      if user.role == "admin":
          return True
      return document.owner_id == user.id
  ```
  If access is unauthorized, an audit event is logged and the request is rejected with HTTP 403 Forbidden.

### 5.4 Cross-Site Request Forgery - CSRF (CWE-352)
* **Vulnerable State:** The `/documents/<id>/transfer` endpoint accepted POST requests without validating an anti-CSRF token. An external attacker site could trigger a background form submission to transfer document ownership.
* **Secure Remediation:**
  1. Generated cryptographically secure synchronizer tokens using `secrets.token_hex(32)`.
  2. Embedded the token in forms: `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">`.
  3. Verified the token using constant-time comparison (`secrets.compare_digest`) on every state-changing POST request.
  4. Configured session cookies with `SameSite=Strict` and `HttpOnly=True`.

### 5.5 Clickjacking & UI Redressing (CWE-1021)
* **Vulnerable State:** The administrative console (`/admin/console`) lacked framing restriction headers. An adversary could frame the page in a semi-transparent `<iframe>` and trick an administrator into clicking sensitive buttons.
* **Secure Remediation:** Injected security headers via a global response middleware in `app/security.py`:
  * `X-Frame-Options: DENY`
  * `Content-Security-Policy: ... frame-ancestors 'none';`
  * `X-Content-Type-Options: nosniff`

---

## 6. Automated DevSecOps Pipeline & Security Testing

### 6.1 GitHub Actions CI/CD Pipeline
Our automated pipeline (`.github/workflows/ci-cd.yml`) executes on every push and pull request to `main` and `develop`. It runs four sequential stages:
1. **Build & Compile:** Compiles the native C parser with `-fstack-protector-strong` and `-D_FORTIFY_SOURCE=2`.
2. **Unit & Security Tests:** Executes all 27 `pytest` test cases.
3. **Static Analysis (SAST):** Runs Bandit across `app/`. Fails the build if any High-severity finding is detected.
4. **Dynamic Analysis (DAST):** Runs automated baseline scans against live endpoints. Fails the build if any Critical or High vulnerability is found.

### 6.2 SAST & DAST Comparative Results

| Security Stage | Pre-Remediation (Vulnerable State) | Post-Remediation (Secure State) | Security Gate Decision |
|:---|:---:|:---:|:---:|
| **Bandit SAST (High Severity)** | 1 Finding (`B605` shell execution) | **0 Findings** | :white_check_mark: **PASSED** |
| **DAST IDOR Check** | HTTP 200 (Unauthorized read allowed) | **HTTP 403 (Blocked)** | :white_check_mark: **PASSED** |
| **DAST CSRF Check** | State changed without token | **HTTP 403 (Token required)** | :white_check_mark: **PASSED** |
| **DAST Clickjacking Check** | Missing anti-framing headers | **X-Frame-Options: DENY** | :white_check_mark: **PASSED** |
| **Unit Test Suite (`pytest`)** | Failures in security assertions | **27 Passed, 0 Failed** | :white_check_mark: **PASSED** |

---

## 7. CIA Residual Risk Analysis

Following full implementation and verification of defensive controls, residual risks were evaluated:
1. **Confidentiality:** Residual risk is **Low**. Object-level authorization strictly prevents IDOR. User passwords are secure against offline dictionary attacks due to slow hashing.
2. **Integrity:** Residual risk is **Low**. Command injection is eliminated by removing shell interpretation. Ownership transfers are protected by anti-CSRF synchronizer tokens and `SameSite=Strict` cookies. Stack buffer overflows are prevented by bounded memory copies and compiler stack canaries.
3. **Availability:** Residual risk is **Low**. Payload size limits (4096 bytes) and diagnostic execution timeouts (5 seconds) protect against resource exhaustion.
4. **Overall System Posture:** CloudVault meets production-grade security requirements for enterprise deployment.

---

## 8. Lessons Learned & Secure Coding Principles

Key takeaways from this DevSecOps security sprint include:
1. **Never Trust User Input:** All external parameters must be strictly validated against whitelists rather than blacklists. Parameterizing system commands (`shell=False`) provides absolute protection against injection.
2. **Memory Safety Requires Defense-in-Depth:** Safe functions like `memcpy` and `snprintf` must always be paired with compiler protections (`-fstack-protector-strong`, ASLR, NX) to ensure robust memory safety.
3. **Centralized Security Controls:** Centralizing authorization checks in helper functions prevents human error and ensures consistent access control across all endpoints.
4. **Automated Security Gates:** Incorporating SAST and DAST into CI/CD pipelines ensures vulnerabilities are caught early before reaching production.

---

## 9. Individual Contribution Statement

Each team member contributed actively to the sprint across Git commits, pull requests, and code reviews:

| Member Name | Student ID | Primary Responsibilities & Key Deliverables | Git & PR Evidence |
|:---|:---:|:---|:---|
| **Muhammad Tallat** | `FA23-BCT-029` | **Lead Architect & Core Engineer:** Designed database models (`app/models.py`), authentication workflows (`app/auth.py`), IDOR remediation (`app/vault.py`), and CSRF protection (`app/security.py`). Authored PNE Report. | Branch `feature/CV-12-auth-idor`, PR #1, PR #3 approval |
| **Sadat Ali** | `FA23-BCT-034` | **AppSec & Threat Modeling Engineer:** Implemented C native parser and secure bounds checking (`native_parser/`), configured compiler defense flags in Makefile, implemented Clickjacking defense headers, and authored Threat Model & STRIDE analysis. | Branch `feature/CV-18-native-buffer`, PR #2, PR #1 approval |
| **Hassaan Shakoor** | `FA23-BCT-054` | **DevSecOps & QA Automation Engineer:** Remediated OS Command Injection (`app/security.py`), created automated test suites (27 `pytest` cases), built GitHub Actions CI/CD pipeline, configured Bandit SAST and DAST gates, and created Docker containerization. | Branch `feature/CV-16-cmd-injection`, PR #4, PR #2 approval |

---

## 10. References
1. OWASP Top 10:2021 — The Ten Most Critical Web Application Security Risks.
2. Common Weakness Enumeration: CWE-120 (Classic Buffer Overflow), CWE-78 (OS Command Injection), CWE-639 (Authorization Bypass Through User-Controlled Key), CWE-352 (Cross-Site Request Forgery), CWE-1021 (Improper Restriction of Rendered UI Layers).
3. FIRST, "Common Vulnerability Scoring System v3.1: Specification Document," 2019.
4. SEI CERT C Coding Standard: Rules for Developing Safe, Reliable, and Secure Systems, Carnegie Mellon University.
5. GitHub Actions Documentation: Continuous Integration and Security Scanning Workflows.
