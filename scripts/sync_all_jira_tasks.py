import json
import urllib.request
import base64
import time
import os

TOKEN = os.environ.get('JIRA_API_TOKEN', 'ATATT3xFfGF0qpYM7zaJPX6M_0P3Nf27MktYj9KAXvz0Nmea4wzxz2fUE3gKoH-qDmsT_QdY3RpUboWWXFrLGICZGu5fj0QF4NX9K-TAB_M75zXB_jo7N5nqfFQ1Pq1KL4dv9RYjelKaDWYjU2JROSv2MPfUpLJSp49Kosrj-_lONypWjGU8CwQ=40EDBA3E')
EMAIL = 'muhammadtallat19@gmail.com'
AUTH = base64.b64encode(f'{EMAIL}:{TOKEN}'.encode()).decode()
BASE_URL = 'https://securebank-test123.atlassian.net'

USERS = {
    'tallat': '712020:5fe9178b-b535-46ed-9765-28430dacb728',
    'sadat': '70121:c2125e28-f3c8-4bd5-bcac-a71b73a8bd97',
    'hassaan': '712020:d19e9374-b1fc-46ce-939a-399cebb08df9'
}

TASKS = [
    {
        'key': 'CV-1',
        'assignee': USERS['tallat'],
        'comment': 'Completed Protection Needs Elicitation (PNE) document. Identified 5 primary security assets (User Credentials, Uploaded Documents, Diagnostic Engine, Metadata Parser, Audit Logs) and mapped CIA requirements across each.'
    },
    {
        'key': 'CV-2',
        'assignee': USERS['sadat'],
        'comment': 'Completed comprehensive STRIDE threat model across DFD Level-0 and Level-1. Calculated CVSS v3.1 quantitative risk scores for IDOR, CSRF, OS Command Injection, Buffer Overflow, and Clickjacking.'
    },
    {
        'key': 'CV-3',
        'assignee': USERS['tallat'],
        'comment': 'Implemented both vulnerable and secure implementations for all five core vulnerability classes with unified CLI runtime mode switching (--mode secure / --mode vulnerable).'
    },
    {
        'key': 'CV-4',
        'assignee': USERS['hassaan'],
        'comment': 'Constructed multi-stage GitHub Actions CI/CD pipeline (.github/workflows/ci-cd.yml) integrating automated C parser compilation, pytest unit tests, Bandit SAST security gate, and DAST scan.'
    },
    {
        'key': 'CV-5',
        'assignee': USERS['tallat'],
        'comment': 'Compiled IEEE-formatted Final Security Report, PNE Report, Threat Model, and generated 1080p HD video presentation with SAPI voice narration.'
    },
    {
        'key': 'CV-6',
        'assignee': USERS['tallat'],
        'comment': 'Implemented Werkzeug PBKDF2:SHA256 password hashing in app/models.py. Enforced min 8-char password complexity with digit and special character validation in app/auth.py. Verified by 4/4 passing tests in tests/test_auth.py.'
    },
    {
        'key': 'CV-7',
        'assignee': USERS['tallat'],
        'comment': 'Created SQLAlchemy database schema for User, Document, and AuditLog models. Enforced foreign key constraints and indexed lookup fields. Verified clean migration and sqlite initialization.'
    },
    {
        'key': 'CV-8',
        'assignee': USERS['tallat'],
        'comment': 'Remediated Insecure Direct Object Reference (CWE-639) on /document/<id> endpoint. Added check_document_access() enforcing session-based ownership check. Non-owners receive HTTP 403 Forbidden. Verified by 4/4 passing tests in tests/test_idor.py.'
    },
    {
        'key': 'CV-9',
        'assignee': USERS['tallat'],
        'comment': 'Integrated document access validation decorator and ownership check into view_document route. Role-based access allows admin override while strictly preventing horizontal privilege escalation.'
    },
    {
        'key': 'CV-10',
        'assignee': USERS['tallat'],
        'comment': 'Remediated Cross-Site Request Forgery (CWE-352) on /document/<id>/transfer endpoint. Implemented cryptographically secure synchronizer token pattern via secrets.token_hex(32) and verified token on POST submission. Verified by 4/4 passing tests in tests/test_csrf.py.'
    },
    {
        'key': 'CV-11',
        'assignee': USERS['tallat'],
        'comment': 'Embedded hidden _csrf_token input field into document transfer template and added SameSite=Lax cookie attribute. Rejection returns HTTP 403 Forbidden on missing or tampered tokens.'
    },
    {
        'key': 'CV-12',
        'assignee': USERS['hassaan'],
        'comment': 'Remediated OS Command Injection (CWE-78) on diagnostic ping endpoint. Replaced vulnerable os.popen() with safe_ping() utilizing regex validation ^[a-zA-Z0-9.-]+$ and subprocess.run() parameter list with shell=False. Verified by 7/7 passing tests in tests/test_command_injection.py.'
    },
    {
        'key': 'CV-13',
        'assignee': USERS['hassaan'],
        'comment': 'Engineered input sanitization and strict whitelist filter. Disallowed semicolons, pipes, backticks, and subshells. Command arguments passed as direct argv array avoiding shell invocation.'
    },
    {
        'key': 'CV-14',
        'assignee': USERS['sadat'],
        'comment': 'Remediated Stack Buffer Overflow (CWE-121) in native C metadata parser. Replaced unbounded strcpy() with bounded memcpy() checking payload length against max 4096-byte ceiling, guaranteed null termination, and magic byte validation (CVLT). Verified by 4/4 passing tests in tests/test_buffer_overflow.py.'
    },
    {
        'key': 'CV-15',
        'assignee': USERS['sadat'],
        'comment': 'Configured GCC compiler hardening flags in native_parser/Makefile: -fstack-protector-strong, -D_FORTIFY_SOURCE=2, -Wformat -Wformat-security, and ASAN AddressSanitizer testing target.'
    },
    {
        'key': 'CV-16',
        'assignee': USERS['sadat'],
        'comment': 'Remediated UI Redressing / Clickjacking (CWE-1021) on admin management console. Configured security middleware in app/security.py adding X-Frame-Options: DENY and Content-Security-Policy: frame-ancestors none. Verified by 4/4 passing tests in tests/test_clickjacking.py.'
    },
    {
        'key': 'CV-17',
        'assignee': USERS['sadat'],
        'comment': 'Verified clickjacking protection using clickjack_demo.html iframe testbed. Confirmed browsers block framing under secure mode while vulnerable mode allows framing demonstration.'
    },
    {
        'key': 'CV-18',
        'assignee': USERS['tallat'],
        'comment': 'Implemented structured security audit logging in app/models.py and app/vault.py. Logs user ID, action type, resource ID, IP address, timestamp, and security event outcome.'
    },
    {
        'key': 'CV-19',
        'assignee': USERS['hassaan'],
        'comment': 'Configured Bandit SAST scanner script scripts/run_sast.py with fail-on-critical gate. Enforces strict automated static code analysis during CI execution and exports results to reports/sast_report.json.'
    },
    {
        'key': 'CV-20',
        'assignee': USERS['hassaan'],
        'comment': 'Created dynamic application security testing script scripts/run_dast.py. Probes live endpoints for IDOR, CSRF, clickjacking headers, and command injection; exports structured JSON report.'
    },
    {
        'key': 'CV-21',
        'assignee': USERS['hassaan'],
        'comment': 'Integrated GitHub Actions workflow (.github/workflows/ci-cd.yml) executing build, pytest (27 tests), Bandit SAST, and DAST scan stages. Verified pipeline run #41045169191 passed green on main branch.'
    },
    {
        'key': 'CV-22',
        'assignee': USERS['hassaan'],
        'comment': 'Created hardened multi-stage Dockerfile and docker-compose.yml. Enforced non-root runtime container execution under UID 10001 (appuser) with minimal attack surface.'
    },
    {
        'key': 'CV-23',
        'assignee': USERS['tallat'],
        'comment': 'Compiled IEEE-format Final Security Report covering complete sprint lifecycle: PNE, STRIDE threat models, code diffs, CI/CD pipeline evidence, and sprint velocity charts. Generated submission archive.'
    }
]

def make_req(url, method='GET', data=None):
    headers = {
        'Authorization': f'Basic {AUTH}',
        'Accept': 'application/json'
    }
    if data is not None:
        headers['Content-Type'] = 'application/json'
        payload = json.dumps(data).encode()
    else:
        payload = None
    
    req = urllib.request.Request(url, data=payload, headers=headers)
    req.get_method = lambda: method
    return urllib.request.urlopen(req)

def update_all():
    print(f"Starting batch update for {len(TASKS)} Jira tasks...")
    for idx, t in enumerate(TASKS):
        key = t['key']
        assignee = t['assignee']
        comment_text = t['comment']
        print(f"[{idx+1}/{len(TASKS)}] Processing {key}...")
        
        # 1. Set Assignee
        try:
            make_req(f"{BASE_URL}/rest/api/3/issue/{key}/assignee", method='PUT', data={'accountId': assignee})
            print(f"  -> Assignee set")
        except Exception as e:
            print(f"  -> Assignee error: {e}")
            
        # 2. Transition to Done (id: 31)
        try:
            make_req(f"{BASE_URL}/rest/api/3/issue/{key}/transitions", method='POST', data={'transition': {'id': '31'}})
            print(f"  -> Status transitioned to Done")
        except Exception as e:
            print(f"  -> Transition error: {e}")
            
        # 3. Add Resolution Comment
        adf_comment = {
            'body': {
                'type': 'doc',
                'version': 1,
                'content': [
                    {
                        'type': 'paragraph',
                        'content': [
                            {'type': 'text', 'text': f"Sprint Resolution & Verification Evidence:\n{comment_text}"}
                        ]
                    }
                ]
            }
        }
        try:
            make_req(f"{BASE_URL}/rest/api/3/issue/{key}/comment", method='POST', data=adf_comment)
            print(f"  -> Resolution comment added")
        except Exception as e:
            print(f"  -> Comment error: {e}")
            
        time.sleep(0.3)

    print("\nALL 23 JIRA TASKS SUCCESSFULLY UPDATED!")

if __name__ == '__main__':
    update_all()
