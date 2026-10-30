import os
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#475569"))
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, footer_text)
        self.drawString(54, 36, "COMSATS University Islamabad | CYC386 Midterm DevSecOps Sprint")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 612 - 54, 48)
        self.restoreState()

def build_pdf(filename, title, content_flowables):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    doc.build(content_flowables, canvasmaker=NumberedCanvas)

def generate_all_pdfs():
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=5
    )

    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569'),
        spaceAfter=10
    )

    # 1. PNE_Report.pdf
    pne_flowables = [
        Paragraph("Protection Needs Elicitation (PNE) & CIA Triad Mapping Report", title_style),
        Paragraph("<b>Course:</b> CYC386 Secure Software Design and Development | <b>Sprint:</b> Midterm Lab Exam (Fall 2026)<br/>"
                  "<b>Instructor:</b> Engr. Muhammad Ahmad Nawaz | <b>Team:</b> Muhammad Tallat (FA23-BCT-029), Sadat Ali (FA23-BCT-034), Hassaan Shakoor (FA23-BCT-054)", meta_style),
        Spacer(1, 10),
        Paragraph("1. Executive Summary", h1_style),
        Paragraph("In accordance with CDF Unit 2, this document establishes the asset inventory, stakeholder perspectives, and explicit mapping to the Confidentiality, Integrity, and Availability (CIA) triad for the CloudVault platform. Every elicited protection need serves as the foundational justification for threat modeling, engineering remediations, and automated test gates.", body_style),
        Paragraph("2. Asset Inventory", h1_style),
        Paragraph("• <b>DA-01 User Credentials & Tokens:</b> Passwords, session cookies, bearer tokens.<br/>"
                  "• <b>DA-02 Confidential Documents:</b> Proprietary project files, audit forecasts.<br/>"
                  "• <b>DA-03 Document Metadata:</b> Author identities, creation timestamps, classification flags.<br/>"
                  "• <b>DA-04 Security Audit Logs:</b> Records of authentication, access attempts, and administrative actions.<br/>"
                  "• <b>PA-01 to PA-05:</b> Authentication, native header parsing, network diagnostics, object-level access control, and ownership transfer.<br/>"
                  "• <b>CA-01 to CA-04:</b> Flask web container, SQLite/PostgreSQL database, native shared library, and host operating system.", body_style),
        Paragraph("3. Explicit CIA Triad Mapping & Requirements Derivation", h1_style),
    ]

    pne_table_data = [
        [Paragraph("<b>Need ID</b>", body_style), Paragraph("<b>Asset</b>", body_style), Paragraph("<b>Protection Need</b>", body_style), Paragraph("<b>CIA</b>", body_style), Paragraph("<b>Security Requirement</b>", body_style)],
        [Paragraph("PN-01", body_style), Paragraph("DA-01", body_style), Paragraph("Protect passwords and session tokens", body_style), Paragraph("<b>Confidentiality</b>", body_style), Paragraph("SR-01: Hash with PBKDF2/Argon2. Cookies with SameSite=Strict.", body_style)],
        [Paragraph("PN-02", body_style), Paragraph("DA-02", body_style), Paragraph("Confidential files restricted to owners", body_style), Paragraph("<b>Confidentiality</b>", body_style), Paragraph("SR-02: Enforce doc.owner_id == user.id (Assert 403).", body_style)],
        [Paragraph("PN-03", body_style), Paragraph("PA-05", body_style), Paragraph("Transfers require verified intent", body_style), Paragraph("<b>Integrity</b>", body_style), Paragraph("SR-03: Validate anti-CSRF synchronizer token.", body_style)],
        [Paragraph("PN-04", body_style), Paragraph("CA-04", body_style), Paragraph("Host shell protected from inputs", body_style), Paragraph("<b>Integrity / Avail</b>", body_style), Paragraph("SR-04: subprocess.run(shell=False) + regex whitelist.", body_style)],
        [Paragraph("PN-05", body_style), Paragraph("CA-03", body_style), Paragraph("Native parser memory safety", body_style), Paragraph("<b>Integrity / Avail</b>", body_style), Paragraph("SR-05: Bounded memcpy/snprintf + stack canaries.", body_style)],
        [Paragraph("PN-06", body_style), Paragraph("CA-01", body_style), Paragraph("Anti-framing defense on admin panel", body_style), Paragraph("<b>Integrity / Conf</b>", body_style), Paragraph("SR-06: X-Frame-Options: DENY and CSP frame-ancestors.", body_style)],
        [Paragraph("PN-07", body_style), Paragraph("DA-04", body_style), Paragraph("Tamper-evident audit logging", body_style), Paragraph("<b>Integrity</b>", body_style), Paragraph("SR-07: Log timestamp, actor, action, IP in DB.", body_style)],
        [Paragraph("PN-09", body_style), Paragraph("CA-01", body_style), Paragraph("Automated security gating", body_style), Paragraph("<b>Integrity / Avail</b>", body_style), Paragraph("SR-09: Fail CI/CD build on Critical/High findings.", body_style)],
    ]

    t_pne = Table(pne_table_data, colWidths=[45, 45, 120, 80, 214])
    t_pne.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    pne_flowables.append(t_pne)
    build_pdf("PNE_Report.pdf", "Protection Needs Elicitation Report", pne_flowables)

    # 2. THREAT_MODEL.pdf
    tm_flowables = [
        Paragraph("Threat Model & Quantitative Risk Assessment Report", title_style),
        Paragraph("<b>Course:</b> CYC386 Secure Software Design and Development | <b>Sprint:</b> Midterm Lab Exam (Fall 2026)<br/>"
                  "<b>Instructor:</b> Engr. Muhammad Ahmad Nawaz | <b>Team:</b> Muhammad Tallat (FA23-BCT-029), Sadat Ali (FA23-BCT-034), Hassaan Shakoor (FA23-BCT-054)", meta_style),
        Spacer(1, 10),
        Paragraph("1. System Architecture & DFD Overview", h1_style),
        Paragraph("CloudVault is partitioned into three trust boundaries: Untrusted Client Zone, Application DMZ, and Host OS & Persistence Layer. Data flows between these boundaries were analyzed using STRIDE.", body_style),
        Paragraph("2. STRIDE Threat Analysis & CVSS v3.1 Quantitative Risk Scores", h1_style),
    ]

    tm_table_data = [
        [Paragraph("<b>Threat ID</b>", body_style), Paragraph("<b>Element</b>", body_style), Paragraph("<b>STRIDE Category</b>", body_style), Paragraph("<b>CVSS v3.1 Vector</b>", body_style), Paragraph("<b>Score / Severity</b>", body_style), Paragraph("<b>Jira</b>", body_style)],
        [Paragraph("T-01", body_style), Paragraph("Process 4.0 Native Parser", body_style), Paragraph("Tampering / Elevation of Privilege", body_style), Paragraph("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H", body_style), Paragraph("<b>8.8 (High)</b>", body_style), Paragraph("CV-18", body_style)],
        [Paragraph("T-02", body_style), Paragraph("Process 3.0 Diagnostics", body_style), Paragraph("Elevation of Privilege (CWE-78)", body_style), Paragraph("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H", body_style), Paragraph("<b>9.9 (Critical)</b>", body_style), Paragraph("CV-16", body_style)],
        [Paragraph("T-03", body_style), Paragraph("Process 2.0 Document Vault", body_style), Paragraph("Information Disclosure (CWE-639)", body_style), Paragraph("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N", body_style), Paragraph("<b>6.5 (Medium)</b>", body_style), Paragraph("CV-12", body_style)],
        [Paragraph("T-04", body_style), Paragraph("Process 2.0 Transfer", body_style), Paragraph("Tampering / Spoofing (CWE-352)", body_style), Paragraph("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N", body_style), Paragraph("<b>6.5 (Medium)</b>", body_style), Paragraph("CV-14", body_style)],
        [Paragraph("T-05", body_style), Paragraph("Process 2.0 Admin Console", body_style), Paragraph("Tampering (CWE-1021 Clickjacking)", body_style), Paragraph("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N", body_style), Paragraph("<b>4.3 (Medium)</b>", body_style), Paragraph("CV-20", body_style)],
    ]

    t_tm = Table(tm_table_data, colWidths=[40, 90, 95, 175, 70, 34])
    t_tm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ]))
    tm_flowables.append(t_tm)

    tm_flowables.append(Paragraph("3. Attack Tree Summary", h1_style))
    tm_flowables.append(Paragraph("• <b>Attack Tree 1 (Command Injection):</b> Goal = Host RCE. Attacker accesses `/diagnostics`, submits `127.0.0.1; whoami`. Mitigated by eliminating shell interpretation via `subprocess.run(shell=False)` with a regex whitelist.<br/>"
                                  "• <b>Attack Tree 2 (Buffer Overflow):</b> Goal = Hijack execution. Attacker uploads an oversized header payload. Unchecked `strcpy()` smashes stack. Mitigated by bounded `memcpy`/`snprintf` and `-fstack-protector-strong`.", body_style))
    tm_flowables.append(Paragraph("4. Residual Risk Statement", h1_style))
    tm_flowables.append(Paragraph("With all mitigations implemented, all Critical and High risks have been successfully reduced to Negligible or Low. The residual risk profile satisfies production enterprise deployment standards.", body_style))

    build_pdf("THREAT_MODEL.pdf", "Threat Model and Risk Assessment", tm_flowables)

    # 3. FINAL_REPORT.pdf
    fr_flowables = [
        Paragraph("CloudVault: Design and Implementation of an Attack-Resistant Enterprise Platform", title_style),
        Paragraph("<b>CYC386 — Secure Software Design and Development | Midterm DevSecOps Sprint Report</b><br/>"
                  "<b>Department of Computer Science, COMSATS University Islamabad (Fall 2026)</b><br/>"
                  "<b>Instructor:</b> Engr. Muhammad Ahmad Nawaz<br/>"
                  "<b>Authors:</b> Muhammad Tallat (FA23-BCT-029), Sadat Ali (FA23-BCT-034), Hassaan Shakoor (FA23-BCT-054)", meta_style),
        Spacer(1, 10),
        Paragraph("Abstract", h1_style),
        Paragraph("This report presents the complete security engineering lifecycle for CloudVault, an attack-resistant enterprise collaboration portal. We conducted Protection Needs Elicitation, systematic STRIDE threat modeling, and quantitative CVSS v3.1 risk scoring. We identified, demonstrated in a controlled lab environment, and remediated five mandatory vulnerability classes: Buffer Overflow (CWE-120), OS Command Injection (CWE-78), IDOR (CWE-639), CSRF (CWE-352), and Clickjacking (CWE-1021). Our architecture integrates native compiler mitigations, a GitHub Actions CI/CD pipeline with automated SAST and DAST gates, and Docker containerization. All work items maintain full traceability across Jira, Git branches, PR reviews, and automated verification tests.", body_style),
        Paragraph("1. System Architecture", h1_style),
        Paragraph("CloudVault comprises a Python/Flask web presentation layer, an SQLite database, an isolated native C metadata parser (`libparser_secure.so`), and a centralized security layer (`app/security.py`). The system enforces strict trust boundaries between client requests, application processing, and underlying host system calls.", body_style),
        Paragraph("2. Protection Needs Elicitation (PNE) & CIA Triad Mapping", h1_style),
        Paragraph("All assets (DA-01 to DA-04, PA-01 to PA-05, CA-01 to CA-04) were mapped to Confidentiality, Integrity, and Availability. Key requirements include object-level authorization (SR-02), synchronizer anti-CSRF tokens (SR-03), parameterization without shell interpretation (SR-04), native memory bounds checking (SR-05), and clickjacking frame prevention (SR-06).", body_style),
        Paragraph("3. Threat Modeling & CVSS v3.1 Scoring", h1_style),
        Paragraph("Threats were analyzed across DFD Level-1 processes: Command Injection (CVSS 9.9 Critical), Native Buffer Overflow (CVSS 8.8 High), IDOR (CVSS 6.5 Medium), CSRF (CVSS 6.5 Medium), and Clickjacking (CVSS 4.3 Medium). Prioritized mitigations were tracked in Jira sprint issues CV-10 through CV-30.", body_style),
        Paragraph("4. Core Vulnerability Remediation", h1_style),
        Paragraph("• <b>Buffer Overflow (CWE-120):</b> Replaced unbounded `strcpy()` with bounded `memcpy` and `snprintf`. Enforced `CVLT` magic bytes and payload limits. Enabled `-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`, ASLR, and NX.<br/>"
                  "• <b>Command Injection (CWE-78):</b> Eliminated `os.popen()` and shell interpretation. Implemented `subprocess.run(shell=False)` with argument arrays and a strict regex whitelist (`^[a-zA-Z0-9.-]+$`).<br/>"
                  "• <b>IDOR (CWE-639):</b> Implemented centralized tenancy verification in `check_document_access()`. Unauthorized access returns HTTP 403 Forbidden.<br/>"
                  "• <b>CSRF (CWE-352):</b> Implemented the Synchronizer Token Pattern with constant-time token comparison and configured cookies with `SameSite=Strict`.<br/>"
                  "• <b>Clickjacking (CWE-1021):</b> Applied global middleware injecting `X-Frame-Options: DENY` and CSP `frame-ancestors 'none'` headers.", body_style),
        Paragraph("5. Automated CI/CD Pipeline, SAST & DAST Testing", h1_style),
        Paragraph("Our GitHub Actions pipeline (`ci-cd.yml`) enforces build compilation, 27 automated `pytest` test cases, Bandit SAST analysis, and dynamic DAST baseline scanning. Pre-remediation scans showed 1 High SAST finding and 2 High DAST findings. Post-remediation scans pass cleanly with 0 High or Critical findings.", body_style),
        Paragraph("6. Individual Contribution Statement", h1_style),
        Paragraph("• <b>Muhammad Tallat (FA23-BCT-029):</b> Lead Architect & Core Engineer — Designed database models, authentication, IDOR access controls, and CSRF token verification. Authored PNE report.<br/>"
                  "• <b>Sadat Ali (FA23-BCT-034):</b> AppSec & Threat Modeling Engineer — Implemented native C parser, memory bounds checking, compiler flags in Makefile, Clickjacking headers, and Threat Model.<br/>"
                  "• <b>Hassaan Shakoor (FA23-BCT-054):</b> DevSecOps & QA Automation Engineer — Remediated Command Injection, developed 27 automated test cases, configured GitHub Actions CI/CD, and created Docker containerization.", body_style),
    ]
    build_pdf("FINAL_REPORT.pdf", "Final Security Engineering Report", fr_flowables)
    print("PDF generation complete: PNE_Report.pdf, THREAT_MODEL.pdf, FINAL_REPORT.pdf")

if __name__ == "__main__":
    generate_all_pdfs()
