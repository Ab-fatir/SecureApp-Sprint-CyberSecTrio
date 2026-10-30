# CloudVault Midterm Demo Video Script (6 to 10 Minutes)

**Course:** CYC386 — Secure Software Design and Development (Fall 2026)  
**Project:** CloudVault (SecureApp-Sprint-CyberSecTrio)  
**Speakers:**  
* **Muhammad Tallat** (FA23-BCT-029)  
* **Sadat Ali** (FA23-BCT-034)  
* **Hassaan Shakoor** (FA23-BCT-054)  

---

## Video Outline & Time Budget

| Section | Duration | Presenter | What to Show on Screen |
|:---|:---:|:---:|:---|
| **1. Introduction & Project Architecture** | 1:30 | Muhammad Tallat | Slide / Browser showing CloudVault homepage and architecture diagram |
| **2. Vulnerability 1 Demo: IDOR (Before -> After)** | 1:45 | Muhammad Tallat | Browser tabs: Alice accessing Bob's doc in vulnerable mode vs 403 Forbidden in secure mode |
| **3. Vulnerability 2 Demo: Command Injection (Before -> After)** | 1:45 | Hassaan Shakoor | Terminal & Browser: `127.0.0.1; whoami` succeeding vs rejected with clean error |
| **4. Vulnerability 3 Demo: Buffer Overflow in C Native Parser** | 1:45 | Sadat Ali | WSL Terminal: `parser_vulnerable` crashing with stack smash vs `parser_secure` handling bounds safely |
| **5. DevSecOps CI/CD Pipeline & Automated Security Gates** | 1:30 | Hassaan Shakoor | GitHub Actions / Terminal running Bandit SAST and DAST scan |
| **6. Conclusion & Individual Contributions** | 0:45 | All Members | Summary slide showing team roles and sprint board |

---

## Detailed Minute-by-Minute Script

### Part 1: Introduction & Architecture (0:00 - 1:30)
**Speaker: Muhammad Tallat**
> "Hello everyone and respected instructor Engr. Muhammad Ahmad Nawaz. Today, our team—consisting of myself, Muhammad Tallat, Sadat Ali, and Hassaan Shakoor—is presenting our 1-Week DevSecOps Midterm Lab Exam project titled CloudVault.
>
> CloudVault is an enterprise document repository and DevOps platform. In this project, we started by eliciting protection needs, mapped every single asset to the CIA triad, built a complete STRIDE threat model, and then hardened five mandatory vulnerability classes: Buffer Overflow, OS Command Injection, IDOR, CSRF, and Clickjacking.
>
> Our application is built in Python Flask with a native C parsing helper. It supports two runtime modes: vulnerable mode, which we used to study the flaws in a controlled lab setting, and secure mode, which includes our full production defenses."

---

### Part 2: IDOR Demonstration (1:30 - 3:15)
**Speaker: Muhammad Tallat**
> "First, let's look at Insecure Direct Object Reference, or IDOR. 
>
> In our database, we have user Alice and user Bob. Document #2 belongs to Bob and contains confidential financial audits.
>
> Now, I run the server in vulnerable mode using `python run.py --mode vulnerable`. I log in as Alice and open Document #1, which is Alice's document. Now, notice the URL: `/documents/1`. If I change the URL ID from 1 to 2, look at what happens: Alice is able to see Bob's private document! There was no object-level authorization check.
>
> Now, let's switch the server to hardened secure mode using `python run.py --mode secure`. Alice tries the exact same request: `/documents/2`. This time, the server rejects the request with HTTP 403 Forbidden! Our centralized function `check_document_access()` verifies that the logged-in user owns the document or is an admin, completely closing the IDOR vulnerability."

---

### Part 3: Command Injection Demonstration (3:15 - 5:00)
**Speaker: Hassaan Shakoor**
> "Next, I am Hassaan Shakoor, and I will demonstrate the remediation of OS Command Injection in our DevOps network diagnostic tool.
>
> In vulnerable mode, our diagnostics page accepted a target hostname and directly passed it to `os.popen()` with shell execution. If an attacker enters `127.0.0.1; whoami` on Linux or `127.0.0.1 && dir` on Windows, the shell executes the second command, giving the attacker arbitrary command execution on the host server!
>
> In our secure mode, we fixed this by taking two critical steps: First, we added a strict regex whitelist `^[a-zA-Z0-9.-]+$` that rejects any semicolon, pipe, ampersand, or backtick characters. Second, we completely disabled shell interpretation by using `subprocess.run(shell=False)` with a structured argument array.
>
> Let's test it: when I enter `127.0.0.1; whoami`, the application immediately blocks it and returns an 'Invalid host format' error. The system command is never passed to a shell."

---

### Part 4: Native Buffer Overflow Demonstration (5:00 - 6:45)
**Speaker: Sadat Ali**
> "I am Sadat Ali, and I will walk you through the Buffer Overflow vulnerability in our native C document parser.
>
> CloudVault uses a native C shared library to parse custom `.cvlt` binary headers. In `metadata_parser_vulnerable.c`, the author field is copied into a fixed 32-byte stack buffer using `strcpy()`. If a user uploads a header with an author longer than 32 bytes, `strcpy()` writes past the buffer boundary, overwriting the stack frame.
>
> In our WSL Ubuntu terminal, when we run `./parser_vulnerable` with a 64-byte payload, it immediately triggers a crash: `*** stack smashing detected ***: terminated`.
>
> In our secure version, `metadata_parser_secure.c`, we replaced `strcpy()` with bounded memory functions (`memcpy` and `snprintf`), validated the header magic bytes `CVLT`, and checked that the declared length does not exceed our safe limit. We also compiled it with `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, ASLR, and NX/DEP. When we run `./parser_secure` with the exact same oversized input, it safely clamps the string without any crash or memory corruption."

---

### Part 5: CI/CD Pipeline & Automated Security Gates (6:45 - 8:15)
**Speaker: Hassaan Shakoor**
> "To enforce these defenses automatically, we built a production-ready DevSecOps CI/CD pipeline using GitHub Actions.
>
> Our pipeline runs on every push and pull request. It has automated security gates:
> 1. It compiles our native C code with compiler hardening flags.
> 2. It runs 27 automated tests in `pytest`.
> 3. It runs Bandit for SAST. If any High or Critical severity issue is detected, the build immediately fails!
> 4. It runs our dynamic DAST baseline scanner to ensure no IDOR, CSRF, or Clickjacking issues exist.
>
> As shown on screen, all 27 tests pass, and both SAST and DAST report zero High severity vulnerabilities in our secure build."

---

### Part 6: Conclusion & Wrap-up (8:15 - 9:00)
**Speaker: Muhammad Tallat**
> "In summary, our team successfully built, demonstrated, and secured CloudVault against all mandatory vulnerability classes: Buffer Overflow, Command Injection, IDOR, CSRF, and Clickjacking. 
>
> Every vulnerability fix is tracked in our Jira sprint board with full traceability from PNE to Threat to Fix to Test. Thank you very much for watching our demo!"
