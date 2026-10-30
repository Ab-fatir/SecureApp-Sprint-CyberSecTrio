import os
import sys
import subprocess
import win32com.client
from PIL import Image, ImageDraw, ImageFont

SLIDES = [
    {
        "title": "CloudVault — DevSecOps Midterm Demo",
        "subtitle": "CYC386 Secure Software Design and Development | Fall 2026",
        "bullets": [
            "Instructor: Engr. Muhammad Ahmad Nawaz",
            "COMSATS University Islamabad, CS Department",
            "",
            "Team Members:",
            "  1. Muhammad Tallat (FA23-BCT-029) - Lead Architect",
            "  2. Sadat Ali (FA23-BCT-034) - Threat Modeling & AppSec",
            "  3. Hassaan Shakoor (FA23-BCT-054) - DevSecOps & Automation"
        ],
        "speech": (
            "Hello everyone and respected instructor Engineer Muhammad Ahmad Nawaz. "
            "Today our team, Muhammad Tallat, Sadat Ali, and Hassaan Shakoor, presents "
            "our DevSecOps Midterm project titled CloudVault. "
            "CloudVault is an enterprise document repository and DevOps management system. "
            "In this sprint, we identified, reproduced, and remediated five mandatory vulnerability classes, "
            "built automated CI CD security gates, and maintained full traceability."
        )
    },
    {
        "title": "Architecture & Trust Boundaries",
        "subtitle": "Protection Needs & STRIDE Threat Modeling",
        "bullets": [
            "Trust Boundary 1: Untrusted Client Zone (Web Browsers & External Requests)",
            "Trust Boundary 2: Application Layer (Flask WSGI, Session Manager, RBAC)",
            "Trust Boundary 3: Host OS & Persistence (SQLite Database, Unprivileged Process)",
            "",
            "Core Security Components:",
            "  • Centralized Security Engine (app/security.py)",
            "  • Native C Metadata Parser (libparser_secure.so)",
            "  • Synchronizer Anti-CSRF Tokens & Frame-Deny Headers"
        ],
        "speech": (
            "Let us review the architecture. CloudVault enforces three primary trust boundaries: "
            "the Untrusted Client Zone, the Application Layer, and the Host Operating System. "
            "All assets were mapped to Confidentiality, Integrity, and Availability. "
            "Our centralized security layer handles tenancy authorization, CSRF token validation, "
            "and strict input filtering before requests reach internal system processes."
        )
    },
    {
        "title": "Vulnerability 1: IDOR Remediation (CWE-639)",
        "subtitle": "Before: Direct Object Manipulation | After: Object-Level Authorization",
        "bullets": [
            "Flaw: In vulnerable mode, /documents/<id> fetched files without checking ownership.",
            "Exploit Scenario: Alice logged in, requested /documents/2 (Bob's confidential report).",
            "Observation: Server returned HTTP 200 OK, leaking private financial data.",
            "",
            "Remediation: Implemented check_document_access(document, user) filter.",
            "Outcome: Foreign requests now strictly rejected with HTTP 403 Forbidden.",
            "Verification: Automated test suite test_idor.py passes 100%."
        ],
        "speech": (
            "The first vulnerability is Insecure Direct Object Reference. "
            "In vulnerable mode, document lookup relied solely on the URL parameter without checking tenancy. "
            "User Alice was able to view Bob's confidential report by simply changing the document ID from 1 to 2. "
            "In our secure mode, we implemented object-level authorization in check document access. "
            "Now, any unauthorized access attempt is rejected with HTTP 403 Forbidden, and an audit log is recorded."
        )
    },
    {
        "title": "Vulnerability 2: OS Command Injection (CWE-78)",
        "subtitle": "Before: Unsafe Shell Execution | After: Regex Whitelist & Parameterization",
        "bullets": [
            "Flaw: DevOps ping diagnostic passed user input to os.popen() with shell interpretation.",
            "Exploit Scenario: Attacker injected 127.0.0.1; whoami or 127.0.0.1 && dir.",
            "Observation: Server executed arbitrary commands with web server daemon privileges.",
            "",
            "Remediation: Enforced regex whitelist ^[a-zA-Z0-9.-]+$ and subprocess.run(shell=False).",
            "Outcome: Shell operators rejected; arguments isolated from system shell.",
            "Verification: Bandit SAST scan flags 0 High issues; test_command_injection.py passes."
        ],
        "speech": (
            "Next is OS Command Injection in our DevOps network diagnostic tool. "
            "In vulnerable mode, user input was passed directly into system shell functions, "
            "allowing command separators like semicolon or double ampersand to execute arbitrary operating system commands. "
            "We remediated this by validating inputs against a strict regex whitelist, and passing arguments "
            "directly via subprocess with shell set to false. "
            "Command chaining is completely blocked, and Bandit static analysis confirms zero high issues."
        )
    },
    {
        "title": "Vulnerability 3: Native Buffer Overflow (CWE-120)",
        "subtitle": "Before: Unbounded strcpy() | After: Bounded Memory & Compiler Mitigations",
        "bullets": [
            "Flaw: metadata_parser_vulnerable.c copied headers into 32-byte stack buffer via strcpy().",
            "Exploit Scenario: Uploading payload > 32 bytes smashed stack frame and return address.",
            "Observation: Process crashed with *** stack smashing detected *** and SIGSEGV.",
            "",
            "Remediation: metadata_parser_secure.c validates CVLT magic, caps payload at 4096 bytes,",
            "  and uses bounded memcpy with guaranteed null-termination.",
            "Compiler Flags: -fstack-protector-strong, -D_FORTIFY_SOURCE=2, ASLR, NX, and ASAN."
        ],
        "speech": (
            "The third vulnerability is a classic Stack Buffer Overflow in our native C binary header parser. "
            "The vulnerable parser used strcpy into a 32-byte stack buffer without bounds checking. "
            "Oversized payloads caused immediate stack smashing and segmentation faults. "
            "In our secure implementation, we validated magic header bytes, capped payloads at 4096 bytes, "
            "and used bounded memory copies. "
            "We also compiled with stack protector strong, FORTIFY SOURCE, ASLR, and non-executable stack flags."
        )
    },
    {
        "title": "DevSecOps CI/CD Pipeline & Automated Security Gates",
        "subtitle": "GitHub Actions Multi-Stage Workflow with Fail-on-Critical Policy",
        "bullets": [
            "Stage 1: Build & Native C Compilation (-fstack-protector-strong)",
            "Stage 2: 27 Automated Unit & Integration Tests (pytest) -> 100% Pass",
            "Stage 3: Static Application Security Testing (Bandit SAST Gate)",
            "Stage 4: Dynamic Application Security Testing (DAST Baseline Scan)",
            "",
            "Live Pipeline Evidence:",
            "  • Failed Run #41044238995: Demonstrates build failure on High severity finding.",
            "  • Passed Run #41045169191: Hardened production build verified clean."
        ],
        "speech": (
            "To enforce continuous security, we built an automated GitHub Actions CI CD pipeline. "
            "Our pipeline compiles native C code, runs 27 automated unit tests, and executes Bandit SAST "
            "and dynamic DAST baseline security scans. "
            "Our repository contains verified evidence of both: an initial run that failed when high vulnerabilities existed, "
            "and our latest production run that passes cleanly with a green checkmark."
        )
    },
    {
        "title": "Individual Contributions & Conclusion",
        "subtitle": "Full Traceability Across Jira, Git Branches, and Pull Requests",
        "bullets": [
            "Muhammad Tallat (FA23-BCT-029): Auth, IDOR & CSRF Defenses, PNE Report",
            "Sadat Ali (FA23-BCT-034): Native C Parser, Memory Bounds, Clickjacking, Threat Model",
            "Hassaan Shakoor (FA23-BCT-054): Command Injection, CI/CD Pipeline, SAST/DAST, Docker",
            "",
            "Public GitHub Repository: github.com/Ab-fatir/SecureApp-Sprint-CyberSecTrio",
            "All Deliverables: PNE_Report.pdf, THREAT_MODEL.pdf, FINAL_REPORT.pdf",
            "",
            "Thank you for reviewing our Midterm DevSecOps Security Sprint!"
        ],
        "speech": (
            "In conclusion, every team member actively contributed across code, tests, and documentation. "
            "Muhammad Tallat led architecture and access controls. "
            "Sadat Ali engineered native memory safety and threat modeling. "
            "Hassaan Shakoor built the CI CD automation and command injection defenses. "
            "Our complete source code, reports, and Jira backlog are available in our public GitHub repository. "
            "Thank you very much."
        )
    }
]

def generate_slide_image(slide_data, output_path):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), color="#0f172a")
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0, 0), (width, 16)], fill="#2563eb")
    draw.rectangle([(0, height - 16), (width, height)], fill="#2563eb")

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 52)
        font_sub = ImageFont.truetype("arial.ttf", 32)
        font_body = ImageFont.truetype("arial.ttf", 30)
        font_bold = ImageFont.truetype("arialbd.ttf", 30)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_bold = font_body

    draw.text((100, 80), slide_data["title"], fill="#f8fafc", font=font_title)
    draw.text((100, 155), slide_data["subtitle"], fill="#93c5fd", font=font_sub)
    draw.line([(100, 215), (width - 100, 215)], fill="#334155", width=2)

    y = 260
    for bullet in slide_data["bullets"]:
        if bullet == "":
            y += 20
            continue
        is_bold = bullet.startswith("Team") or bullet.startswith("Remediation") or bullet.startswith("Outcome") or bullet.startswith("Stage") or bullet.startswith("Live")
        font_to_use = font_bold if is_bold else font_body
        text_color = "#38bdf8" if is_bold else "#e2e8f0"
        draw.text((120, y), bullet, fill=text_color, font=font_to_use)
        y += 50

    draw.text((100, height - 60), "COMSATS University Islamabad | CYC386 DevSecOps Security Sprint", fill="#64748b", font=font_sub)
    img.save(output_path)

def generate_voice(text, output_path):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    filestream = win32com.client.Dispatch("SAPI.SpFileStream")
    filestream.Open(output_path, 3)
    speaker.AudioOutputStream = filestream
    speaker.Rate = 0
    speaker.Speak(text)
    filestream.Close()

def main():
    os.makedirs("demo_build", exist_ok=True)
    part_files = []

    print("[*] Generating CloudVault demo video slides and speech narration...")

    for i, slide in enumerate(SLIDES):
        idx = i + 1
        img_file = f"demo_build/slide_{idx}.png"
        wav_file = f"demo_build/audio_{idx}.wav"
        mp4_part = f"demo_build/part_{idx}.mp4"

        print(f"  -> Building Part {idx}: {slide['title']}")
        generate_slide_image(slide, img_file)
        generate_voice(slide["speech"], wav_file)

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", img_file,
            "-i", wav_file,
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest", mp4_part
        ]
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        part_files.append(mp4_part)

    concat_list_path = "demo_build/concat.txt"
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for p in part_files:
            abs_p = os.path.abspath(p).replace("\\", "/")
            f.write(f"file '{abs_p}'\n")

    print("[*] Merging parts into final demo_video.mp4...")
    output_video = "demo_video.mp4"
    merge_cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        output_video
    ]
    subprocess.run(merge_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if os.path.exists(output_video):
        size_mb = os.path.getsize(output_video) / (1024 * 1024)
        print(f"[+] Success! Demo video generated: {output_video} ({size_mb:.2f} MB)")
    else:
        print("[-] Failed to generate demo_video.mp4")

if __name__ == "__main__":
    main()
