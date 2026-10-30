# Security Policy — CloudVault

## 1. Overview
The **CloudVault DevSecOps Engineering Team** takes application security and memory safety seriously. This project implements defense-in-depth engineering principles aligned with OWASP Top 10, CWE/SANS Top 25, and SEI CERT C Coding Standards as part of the **CYC386 Secure Software Design and Development** DevSecOps Security Sprint.

---

## 2. Supported Versions

| Version | Supported | Security Hardening Status |
|:---|:---:|:---|
| 2.0.0 (Hardened Production) | :white_check_mark: | Fully remediated, active SAST/DAST, memory bounds checked |
| 1.0.0 (Legacy / Lab Demonstration) | :x: | Vulnerable state for controlled lab demonstration only |

---

## 3. Vulnerability Reporting & Disclosure Process

If you discover a security vulnerability or weakness within CloudVault:
1. **Do not create a public issue** on GitHub.
2. Send an encrypted email with detailed reproduction steps to our AppSec lead:
   * **AppSec Lead:** Muhammad Tallat (FA23-BCT-029) — `fa23-bct-029@isb.student.comsats.edu.pk`
   * **Security Reviewer:** Engr. Muhammad Ahmad Nawaz — `m.ahmadnawazz@gmail.com`
3. Include the following details:
   * Target endpoint / module (e.g., C native parser, diagnostic API, document access control)
   * CWE identifier and vulnerability classification (STRIDE category)
   * Proof of Concept (PoC) description and environment specifications
   * Expected vs. observed behavior
   * Potential CIA Triad impact (Confidentiality, Integrity, Availability)
4. **Response SLA:** The security team acknowledges receipt within 24 hours and provides an initial remediation timeline within 48 hours.

---

## 4. Secure Development Life Cycle (SDLC) & Defense Gates
All contributions to this repository must satisfy our automated security gates:
* **Pre-commit:** Git hooks for secret detection (`detect-secrets` / Gitleaks)
* **Static Application Security Testing (SAST):** Bandit (High/Medium threshold) and Semgrep OWASP ruleset
* **Dynamic Application Security Testing (DAST):** OWASP ZAP baseline scan
* **Compiler Defenses:** `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, ASLR, NX/DEP enabled on native binaries
* **CI/CD Enforced Gate:** Pull requests fail automatically if any Critical or High vulnerability is flagged.
