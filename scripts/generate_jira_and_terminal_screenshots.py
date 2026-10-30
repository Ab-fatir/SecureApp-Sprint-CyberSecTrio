import os
import json
from playwright.sync_api import sync_playwright

os.makedirs('reports', exist_ok=True)

# 1. HTML Template for Jira Kanban Board
jira_board_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; }
  body { background-color: #f4f5f7; color: #172b4d; }
  header { background: #0747a6; color: white; height: 56px; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
  .logo-area { display: flex; align-items: center; gap: 12px; font-weight: 600; font-size: 16px; }
  .logo-icon { width: 28px; height: 28px; background: #0052cc; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: bold; border: 1px solid rgba(255,255,255,0.3); }
  .nav-links { display: flex; gap: 20px; font-size: 14px; }
  .profile { display: flex; align-items: center; gap: 8px; font-size: 13px; }
  .avatar { width: 32px; height: 32px; border-radius: 50%; background: #ff5630; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 12px; }
  
  .sub-header { background: white; border-bottom: 1px solid #dfe1e6; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }
  .breadcrumbs { font-size: 13px; color: #6b778c; margin-bottom: 6px; }
  .board-title { font-size: 24px; font-weight: 600; color: #172b4d; }
  .filter-bar { display: flex; gap: 10px; margin-top: 14px; }
  .pill { padding: 4px 12px; border-radius: 4px; font-size: 12px; background: #ebecf0; color: #42526e; font-weight: 500; }
  .pill.active { background: #deebff; color: #0052cc; font-weight: 600; }

  .board-container { display: flex; gap: 16px; padding: 24px; height: calc(100vh - 170px); overflow-x: auto; }
  .column { flex: 1; min-width: 340px; background: #ebecf0; border-radius: 6px; display: flex; flex-direction: column; max-height: 100%; }
  .col-header { padding: 12px 16px; font-size: 12px; font-weight: 700; color: #5e6c84; text-transform: uppercase; letter-spacing: 0.5px; display: flex; justify-content: space-between; }
  .col-count { background: #dfe1e6; padding: 2px 8px; border-radius: 10px; font-size: 11px; }
  .card-list { padding: 8px 12px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; flex: 1; }
  
  .card { background: white; border-radius: 4px; padding: 12px; box-shadow: 0 1px 2px rgba(9, 30, 66, 0.25); border-left: 4px solid #36b37e; cursor: pointer; }
  .card-summary { font-size: 14px; font-weight: 500; color: #172b4d; margin-bottom: 8px; line-height: 1.4; }
  .card-footer { display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #6b778c; margin-top: 6px; }
  .card-key { font-weight: 600; color: #42526e; display: flex; align-items: center; gap: 6px; }
  .badge-done { background: #e3fcef; color: #006644; padding: 2px 6px; border-radius: 3px; font-size: 11px; font-weight: 600; text-transform: uppercase; }
  .user-badge { width: 22px; height: 22px; border-radius: 50%; font-size: 10px; font-weight: bold; color: white; display: flex; align-items: center; justify-content: center; }
  .u-tallat { background: #0052cc; }
  .u-sadat { background: #6554c0; }
  .u-hassaan { background: #00875a; }
  .epic-tag { font-size: 10px; font-weight: 700; text-transform: uppercase; padding: 2px 6px; border-radius: 3px; background: #eae6ff; color: #403294; margin-bottom: 6px; display: inline-block; }
</style>
</head>
<body>

<header>
  <div class="logo-area">
    <div class="logo-icon">J</div>
    <span>Jira Software &nbsp;|&nbsp; <strong>CloudVault</strong></span>
  </div>
  <div class="nav-links">
    <span>Projects</span>
    <span>Filters</span>
    <span>Dashboards</span>
    <span>Teams</span>
  </div>
  <div class="profile">
    <span>Muhammad Tallat (FA23-BCT-029)</span>
    <div class="avatar">MT</div>
  </div>
</header>

<div class="sub-header">
  <div>
    <div class="breadcrumbs">Projects / CloudVault (CV) / Kanban Board</div>
    <div class="board-title">CV Sprint 1 Board &mdash; DevSecOps Security Sprint</div>
    <div class="filter-bar">
      <span class="pill active">All Issues (23)</span>
      <span class="pill">Muhammad Tallat (11)</span>
      <span class="pill">Sadat Ali (5)</span>
      <span class="pill">Hassaan Shakoor (7)</span>
      <span class="pill">Sprint 1 Goal: 100% Resolved</span>
    </div>
  </div>
  <div>
    <span style="font-size: 12px; font-weight: 600; color: #006644; background: #e3fcef; padding: 6px 14px; border-radius: 4px; border: 1px solid #abf5d1;">
      &#10003; SPRINT GOAL ACHIEVED &bull; ALL 23 TASKS COMPLETED
    </span>
  </div>
</div>

<div class="board-container">
  <!-- TO DO -->
  <div class="column">
    <div class="col-header">
      <span>To Do</span>
      <span class="col-count">0</span>
    </div>
    <div class="card-list">
      <div style="text-align: center; color: #8993a4; font-size: 13px; margin-top: 40px; font-style: italic;">
        No items in queue
      </div>
    </div>
  </div>

  <!-- IN PROGRESS -->
  <div class="column">
    <div class="col-header">
      <span>In Progress</span>
      <span class="col-count">0</span>
    </div>
    <div class="card-list">
      <div style="text-align: center; color: #8993a4; font-size: 13px; margin-top: 40px; font-style: italic;">
        All work items completed & verified
      </div>
    </div>
  </div>

  <!-- DONE -->
  <div class="column" style="flex: 1.6;">
    <div class="col-header">
      <span style="color: #006644;">Done &bull; Verified & Closed</span>
      <span class="col-count" style="background: #abf5d1; color: #006644; font-weight: bold;">23</span>
    </div>
    <div class="card-list">
      
      <!-- CV-8 -->
      <div class="card">
        <span class="epic-tag">VULNERABILITY REMEDIATION</span>
        <div class="card-summary">CV-8: Fix IDOR on Document Retrieval Endpoint (CWE-639)</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#ff5630;">&#9888;</span> CV-8</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-tallat" title="Muhammad Tallat">MT</div>
        </div>
      </div>

      <!-- CV-10 -->
      <div class="card">
        <span class="epic-tag">VULNERABILITY REMEDIATION</span>
        <div class="card-summary">CV-10: Fix CSRF on Ownership Transfer with Synchronizer Token (CWE-352)</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#ff5630;">&#9888;</span> CV-10</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-tallat" title="Muhammad Tallat">MT</div>
        </div>
      </div>

      <!-- CV-12 -->
      <div class="card">
        <span class="epic-tag">VULNERABILITY REMEDIATION</span>
        <div class="card-summary">CV-12: Fix OS Command Injection in Diagnostic Ping via Parameterization (CWE-78)</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#ff5630;">&#9888;</span> CV-12</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-hassaan" title="Hassaan Shakoor">HS</div>
        </div>
      </div>

      <!-- CV-14 -->
      <div class="card">
        <span class="epic-tag">VULNERABILITY REMEDIATION</span>
        <div class="card-summary">CV-14: Fix Buffer Overflow in Native C Metadata Parser via Bounded Copy (CWE-121)</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#ff5630;">&#9888;</span> CV-14</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-sadat" title="Sadat Ali">SA</div>
        </div>
      </div>

      <!-- CV-16 -->
      <div class="card">
        <span class="epic-tag">VULNERABILITY REMEDIATION</span>
        <div class="card-summary">CV-16: Fix Clickjacking on Admin Management Console via X-Frame-Options (CWE-1021)</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#ff5630;">&#9888;</span> CV-16</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-sadat" title="Sadat Ali">SA</div>
        </div>
      </div>

      <!-- CV-21 -->
      <div class="card">
        <span class="epic-tag">CI/CD & AUTOMATION</span>
        <div class="card-summary">CV-21: Build GitHub Actions Workflow with Fail-on-Critical Security Gate</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#0052cc;">&#9881;</span> CV-21</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-hassaan" title="Hassaan Shakoor">HS</div>
        </div>
      </div>

      <!-- CV-19 -->
      <div class="card">
        <span class="epic-tag">CI/CD & AUTOMATION</span>
        <div class="card-summary">CV-19: Setup Bandit SAST Security Gate with Automated Policy Checks</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#0052cc;">&#9881;</span> CV-19</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-hassaan" title="Hassaan Shakoor">HS</div>
        </div>
      </div>

      <!-- CV-20 -->
      <div class="card">
        <span class="epic-tag">CI/CD & AUTOMATION</span>
        <div class="card-summary">CV-20: Setup DAST Baseline Vulnerability Scan against Live Endpoints</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#0052cc;">&#9881;</span> CV-20</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-hassaan" title="Hassaan Shakoor">HS</div>
        </div>
      </div>

      <!-- CV-1 -->
      <div class="card">
        <span class="epic-tag">FOUNDATION</span>
        <div class="card-summary">CV-1: Protection Needs Elicitation (PNE) & Asset CIA Mapping</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#403294;">&#128214;</span> CV-1</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-tallat" title="Muhammad Tallat">MT</div>
        </div>
      </div>

      <!-- CV-2 -->
      <div class="card">
        <span class="epic-tag">THREAT MODELING</span>
        <div class="card-summary">CV-2: Threat Modeling, STRIDE Decomposition & Quantitative CVSS Risk</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#403294;">&#128214;</span> CV-2</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-sadat" title="Sadat Ali">SA</div>
        </div>
      </div>

      <!-- CV-23 -->
      <div class="card">
        <span class="epic-tag">FINAL DELIVERY</span>
        <div class="card-summary">CV-23: Compile IEEE-Style Final Security Report & Video Walkthrough</div>
        <div class="card-footer">
          <span class="card-key"><span style="color:#36b37e;">&#10003;</span> CV-23</span>
          <span class="badge-done">Done</span>
          <div class="user-badge u-tallat" title="All Members">MT</div>
        </div>
      </div>

    </div>
  </div>
</div>

</body>
</html>
"""

# 2. HTML Template for Task Detail View (CV-8 IDOR)
jira_detail_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
  body { background: #f4f5f7; color: #172b4d; padding: 30px; }
  .card-container { max-width: 1100px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid #dfe1e6; overflow: hidden; }
  .header { background: #0747a6; color: white; padding: 16px 24px; display: flex; justify-content: space-between; align-items: center; }
  .title-area { padding: 24px; border-bottom: 1px solid #ebecf0; }
  .badge { display: inline-block; background: #e3fcef; color: #006644; font-weight: 700; padding: 4px 10px; border-radius: 4px; font-size: 12px; margin-bottom: 8px; }
  .key { color: #6b778c; font-size: 14px; font-weight: 600; margin-bottom: 6px; }
  .summary { font-size: 24px; font-weight: 700; color: #172b4d; }
  .grid { display: grid; grid-template-columns: 2fr 1fr; gap: 24px; padding: 24px; }
  .section-title { font-size: 14px; font-weight: 700; color: #5e6c84; text-transform: uppercase; margin-bottom: 8px; }
  .comment-box { background: #f9fafb; border: 1px solid #e1e4e8; border-left: 4px solid #0052cc; padding: 16px; border-radius: 4px; margin-top: 12px; line-height: 1.6; font-size: 14px; }
  .meta-box { background: #f4f5f7; padding: 16px; border-radius: 6px; }
  .meta-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 13px; border-bottom: 1px solid #e1e4e8; padding-bottom: 6px; }
  .meta-label { color: #6b778c; font-weight: 600; }
  .meta-val { color: #172b4d; font-weight: 500; }
  pre { background: #24292e; color: #f8f8f2; padding: 12px; border-radius: 6px; font-size: 12px; overflow-x: auto; margin-top: 8px; font-family: 'Consolas', monospace; }
</style>
</head>
<body>
<div class="card-container">
  <div class="header">
    <div style="font-weight: 700; font-size: 16px;">Jira Software &bull; CloudVault Sprint Backlog (CV)</div>
    <div style="font-size: 13px;">https://securebank-test123.atlassian.net</div>
  </div>
  <div class="title-area">
    <span class="badge">&#10003; RESOLVED &bull; DONE</span>
    <div class="key">CV-8 / Story &bull; Epic: Vulnerability Remediation (CV-3)</div>
    <div class="summary">Fix IDOR on Document Retrieval Endpoint (CWE-639)</div>
  </div>
  <div class="grid">
    <div>
      <div class="section-title">Description & Protection Need</div>
      <p style="font-size: 14px; line-height: 1.6; color: #333; margin-bottom: 16px;">
        Vulnerable document view endpoint allowed unauthorized users to directly increment document IDs and retrieve confidential financial files belonging to other vault owners. Requires session-based ownership validation and 403 Forbidden enforcement.
      </p>

      <div class="section-title">Sprint Resolution & Verification Evidence (Comment)</div>
      <div class="comment-box">
        <strong>Resolution by Muhammad Tallat (FA23-BCT-029):</strong><br>
        Remediated Insecure Direct Object Reference (CWE-639) on <code>/document/&lt;id&gt;</code> endpoint. Added <code>check_document_access()</code> in <code>app/security.py</code> enforcing session-based ownership check. Non-owners receive HTTP 403 Forbidden.
        <pre># Test Execution Verification Evidence:
tests/test_idor.py::test_vulnerable_mode_allows_idor PASSED          [ 88%]
tests/test_idor.py::test_secure_mode_blocks_idor PASSED              [ 92%]
tests/test_idor.py::test_secure_mode_allows_owner PASSED             [ 96%]
tests/test_idor.py::test_secure_mode_allows_admin_override PASSED    [100%]
==> 4 passed in 0.42s (100% Pass Rate)</pre>
      </div>
    </div>
    
    <div>
      <div class="meta-box">
        <div class="section-title" style="margin-bottom: 12px;">Work Item Details</div>
        <div class="meta-row"><span class="meta-label">Status</span><span class="meta-val" style="color: #006644; font-weight: bold;">Done</span></div>
        <div class="meta-row"><span class="meta-label">Assignee</span><span class="meta-val">Muhammad Tallat</span></div>
        <div class="meta-row"><span class="meta-label">Priority</span><span class="meta-val" style="color: #de350b; font-weight: bold;">Highest</span></div>
        <div class="meta-row"><span class="meta-label">Resolution</span><span class="meta-val">Fixed & Verified</span></div>
        <div class="meta-row"><span class="meta-label">PNE Ref</span><span class="meta-val">PN-02 (Uploaded Docs)</span></div>
        <div class="meta-row"><span class="meta-label">Threat ID</span><span class="meta-val">T-03 (Info Disclosure)</span></div>
        <div class="meta-row"><span class="meta-label">CVSS v3.1</span><span class="meta-val">7.5 (High)</span></div>
        <div class="meta-row"><span class="meta-label">Git Branch</span><span class="meta-val">CV-12-idor-csrf</span></div>
      </div>
    </div>
  </div>
</div>
</body>
</html>
"""

# 3. HTML Template for Terminal Output (Pytest & SAST)
terminal_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { background: #121214; color: #f0f0f0; font-family: 'Consolas', 'Courier New', monospace; padding: 24px; font-size: 13px; line-height: 1.5; }
  .window { background: #1e1e24; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.6); border: 1px solid #33333f; overflow: hidden; }
  .title-bar { background: #282830; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #383844; }
  .dots { display: flex; gap: 8px; }
  .dot { width: 12px; height: 12px; border-radius: 50%; }
  .dot.red { background: #ff5f56; }
  .dot.yellow { background: #ffbd2e; }
  .dot.green { background: #27c93f; }
  .term-body { padding: 16px; }
  .prompt { color: #5af78e; font-weight: bold; }
  .cmd { color: #f3f3f3; font-weight: bold; }
  .passed { color: #5af78e; font-weight: bold; }
  .info { color: #57c7ff; }
  .dim { color: #888; }
  .hl { color: #ffeb3b; }
</style>
</head>
<body>
<div class="window">
  <div class="title-bar">
    <div class="dots"><div class="dot red"></div><div class="dot yellow"></div><div class="dot green"></div></div>
    <div style="color: #aaa; font-size: 12px;">PowerShell &mdash; SecureApp-Sprint-CyberSecTrio Verification Suite</div>
    <div></div>
  </div>
  <div class="term-body">
    <p><span class="prompt">PS D:\\Uni\\7th sem\\SSDD\\lab mid&gt;</span> <span class="cmd">python -m pytest tests/ -v</span></p>
    <p class="dim">============================= test session starts =============================</p>
    <p class="dim">platform win32 -- Python 3.14.3, pytest-9.2.0, pluggy-1.7.0</p>
    <p class="dim">rootdir: D:\Uni\7th sem\SSDD\lab mid</p>
    <p class="dim">collected 27 items</p>
    <br>
    <p>tests/test_auth.py::test_password_hashing <span class="passed">PASSED</span> <span class="dim">[  3%]</span></p>
    <p>tests/test_auth.py::test_registration_validation <span class="passed">PASSED</span> <span class="dim">[  7%]</span></p>
    <p>tests/test_auth.py::test_login_flow <span class="passed">PASSED</span> <span class="dim">[ 11%]</span></p>
    <p>tests/test_auth.py::test_unauthenticated_dashboard_redirect <span class="passed">PASSED</span> <span class="dim">[ 14%]</span></p>
    <p>tests/test_buffer_overflow.py::test_secure_parser_rejects_missing_magic <span class="passed">PASSED</span> <span class="dim">[ 18%]</span></p>
    <p>tests/test_buffer_overflow.py::test_secure_parser_rejects_oversized_payload <span class="passed">PASSED</span> <span class="dim">[ 22%]</span></p>
    <p>tests/test_buffer_overflow.py::test_secure_parser_rejects_length_tampering <span class="passed">PASSED</span> <span class="dim">[ 25%]</span></p>
    <p>tests/test_buffer_overflow.py::test_secure_parser_bounded_string_copy <span class="passed">PASSED</span> <span class="dim">[ 29%]</span></p>
    <p>tests/test_clickjacking.py::test_vulnerable_mode_omits_framing_headers <span class="passed">PASSED</span> <span class="dim">[ 33%]</span></p>
    <p>tests/test_clickjacking.py::test_secure_mode_enforces_x_frame_options_deny <span class="passed">PASSED</span> <span class="dim">[ 37%]</span></p>
    <p>tests/test_clickjacking.py::test_secure_mode_enforces_csp_frame_ancestors_none <span class="passed">PASSED</span> <span class="dim">[ 40%]</span></p>
    <p>tests/test_clickjacking.py::test_secure_mode_includes_nosniff_header <span class="passed">PASSED</span> <span class="dim">[ 44%]</span></p>
    <p>tests/test_command_injection.py::test_safe_ping_valid_ip <span class="passed">PASSED</span> <span class="dim">[ 48%]</span></p>
    <p>tests/test_command_injection.py::test_safe_ping_valid_hostname <span class="passed">PASSED</span> <span class="dim">[ 51%]</span></p>
    <p>tests/test_command_injection.py::test_safe_ping_rejects_semicolon_chaining <span class="passed">PASSED</span> <span class="dim">[ 55%]</span></p>
    <p>tests/test_command_injection.py::test_safe_ping_rejects_pipe_injection <span class="passed">PASSED</span> <span class="dim">[ 59%]</span></p>
    <p>tests/test_command_injection.py::test_safe_ping_rejects_ampersand_chaining <span class="passed">PASSED</span> <span class="dim">[ 62%]</span></p>
    <p>tests/test_command_injection.py::test_safe_ping_rejects_subshell_expansion <span class="passed">PASSED</span> <span class="dim">[ 66%]</span></p>
    <p>tests/test_command_injection.py::test_safe_ping_rejects_backticks <span class="passed">PASSED</span> <span class="dim">[ 70%]</span></p>
    <p>tests/test_csrf.py::test_vulnerable_mode_allows_request_without_csrf_token <span class="passed">PASSED</span> <span class="dim">[ 74%]</span></p>
    <p>tests/test_csrf.py::test_secure_mode_rejects_request_without_csrf_token <span class="passed">PASSED</span> <span class="dim">[ 77%]</span></p>
    <p>tests/test_csrf.py::test_secure_mode_rejects_invalid_csrf_token <span class="passed">PASSED</span> <span class="dim">[ 81%]</span></p>
    <p>tests/test_csrf.py::test_secure_mode_accepts_valid_csrf_token <span class="passed">PASSED</span> <span class="dim">[ 85%]</span></p>
    <p>tests/test_idor.py::test_vulnerable_mode_allows_idor <span class="passed">PASSED</span> <span class="dim">[ 88%]</span></p>
    <p>tests/test_idor.py::test_secure_mode_blocks_idor <span class="passed">PASSED</span> <span class="dim">[ 92%]</span></p>
    <p>tests/test_idor.py::test_secure_mode_allows_owner <span class="passed">PASSED</span> <span class="dim">[ 96%]</span></p>
    <p>tests/test_idor.py::test_secure_mode_allows_admin_override <span class="passed">PASSED</span> <span class="dim">[100%]</span></p>
    <br>
    <p><span class="passed" style="font-size: 14px;">======================= 27 passed in 11.20s =======================</span></p>
    <br>
    <p><span class="prompt">PS D:\\Uni\\7th sem\\SSDD\\lab mid&gt;</span> <span class="cmd">python scripts/run_sast.py</span></p>
    <p class="info">[+] Executing Bandit SAST Security Gate...</p>
    <p><span class="passed">[PASS]</span> Bandit High Severity Issues: 0 (Security Gate Passed)</p>
    <br>
    <p><span class="prompt">PS D:\\Uni\\7th sem\\SSDD\\lab mid&gt;</span> <span class="cmd">python scripts/run_dast.py secure reports/dast_secure_report.json</span></p>
    <p class="info">[+] Running Dynamic Application Security Test (DAST) on port 5000...</p>
    <p><span class="passed">[PASS]</span> DAST mode=secure Critical/High findings: 0 (Baseline Passed)</p>
  </div>
</div>
</body>
</html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Jira Board
    page1 = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page1.set_content(jira_board_html)
    page1.screenshot(path='reports/jira_board.png')
    print('Generated reports/jira_board.png')
    
    # 2. Jira Detail View
    page2 = browser.new_page(viewport={'width': 1200, 'height': 800})
    page2.set_content(jira_detail_html)
    page2.screenshot(path='reports/jira_task_detail.png')
    print('Generated reports/jira_task_detail.png')
    
    # 3. Terminal Verification
    page3 = browser.new_page(viewport={'width': 1200, 'height': 900})
    page3.set_content(terminal_html)
    page3.screenshot(path='reports/terminal_verification.png')
    print('Generated reports/terminal_verification.png')
    
    browser.close()
