#!/usr/bin/env python3
"""
Secret Scanner — offline, stdlib-only secret detection tool.

Commands:
  scan <file-or-dir>   Recursively scan files/directories for secrets.
  check <file>         Scan a single file with detailed output.
  list-patterns        List all supported detection patterns.

Detection includes 27 regex patterns + entropy-based high-entropy string detection.
"""

from __future__ import annotations

import argparse
import math
import os
import re
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

# ---------------------------------------------------------------------------
# Pattern definitions
# ---------------------------------------------------------------------------

PATTERNS: List[dict] = [
    # 1
    {
        "id": "aws-access-key",
        "name": "AWS Access Key ID",
        "severity": "high",
        "regex": re.compile(r"(?<![A-Z0-9])AKIA[0-9A-Z]{16}(?![0-9A-Z])"),
    },
    # 2
    {
        "id": "aws-secret-key",
        "name": "AWS Secret Access Key",
        "severity": "critical",
        "regex": re.compile(
            r"(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])"
        ),
    },
    # 3
    {
        "id": "github-pat",
        "name": "GitHub Personal Access Token",
        "severity": "critical",
        "regex": re.compile(r"(?:ghp|gho|ghu|ghs|ghf)_[A-Za-z0-9]{36,252}"),
    },
    # 4
    {
        "id": "openai-key",
        "name": "OpenAI API Key",
        "severity": "critical",
        "regex": re.compile(r"sk-[A-Za-z0-9]{20,60}(?:T3BlbkFJ[0-9A-Za-z]{1,60})?"),
    },
    # 5
    {
        "id": "slack-bot-token",
        "name": "Slack Bot / App Token",
        "severity": "high",
        "regex": re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,100}"),
    },
    # 6
    {
        "id": "google-api-key",
        "name": "Google API Key",
        "severity": "high",
        "regex": re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    },
    # 7
    {
        "id": "google-oauth",
        "name": "Google OAuth Access Token",
        "severity": "high",
        "regex": re.compile(r"ya29\.[0-9A-Za-z\-_]{50,200}"),
    },
    # 8
    {
        "id": "jwt",
        "name": "JSON Web Token (JWT)",
        "severity": "critical",
        "regex": re.compile(
            r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
        ),
    },
    # 9
    {
        "id": "ssh-private-key",
        "name": "SSH Private Key block indicator",
        "severity": "critical",
        "regex": re.compile(
            r"-----BEGIN\s*(?:RSA|DSA|EC|OPENSSH|SSH2)\s*PRIVATE\s*KEY-----"
        ),
    },
    # 10
    {
        "id": "pgp-private-key",
        "name": "PGP Private Key block indicator",
        "severity": "critical",
        "regex": re.compile(
            r"-----BEGIN\s*PGP\s*PRIVATE\s*KEY\s*BLOCK-----"
        ),
    },
    # 11
    {
        "id": "password-in-url",
        "name": "Password in URL (Basic Auth)",
        "severity": "high",
        "regex": re.compile(
            r"[a-zA-Z][a-zA-Z0-9+.-]*://[^:/\s]+:[^@/\s]+@[a-zA-Z0-9.-]+"
        ),
    },
    # 12
    {
        "id": "twitter-bearer",
        "name": "Twitter/X Bearer Token",
        "severity": "high",
        "regex": re.compile(r"AAAAAAAAAAAAAAAAAAAA[A-Za-z0-9%]{40,80}"),
    },
    # 13
    {
        "id": "heroku-api-key",
        "name": "Heroku API Key",
        "severity": "high",
        "regex": re.compile(r"[hH][eE][rR][oO][kK][uU].{0,30}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}", re.IGNORECASE),
    },
    # 14
    {
        "id": "discord-bot-token",
        "name": "Discord Bot Token",
        "severity": "high",
        "regex": re.compile(r"[MN][A-Za-z\d]{23}\.[Xx][A-Za-z\d]{6}\.[A-Za-z\d_-]{27}"),
    },
    # 15
    {
        "id": "telegram-bot-token",
        "name": "Telegram Bot Token",
        "severity": "high",
        "regex": re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35,45}\b"),
    },
    # 16
    {
        "id": "gitlab-pat",
        "name": "GitLab Personal Access Token",
        "severity": "high",
        "regex": re.compile(r"glpat-[A-Za-z0-9\-_]{20,40}"),
    },
    # 17
    {
        "id": "mongodb-connection-string",
        "name": "MongoDB Connection String",
        "severity": "critical",
        "regex": re.compile(
            r"mongodb(?:\+srv)?://[^\s:@]+:[^\s:@]+@[^\s,]+"
        ),
    },
    # 18
    {
        "id": "stripe-key",
        "name": "Stripe API Key",
        "severity": "critical",
        "regex": re.compile(r"(?:sk|pk)_(?:live|test)_[0-9A-Za-z]{24,48}"),
    },
    # 19
    {
        "id": "twilio-key",
        "name": "Twilio API Key / SID",
        "severity": "high",
        "regex": re.compile(r"SK[0-9a-fA-F]{32}"),
    },
    # 20
    {
        "id": "facebook-access-token",
        "name": "Facebook Access Token",
        "severity": "high",
        "regex": re.compile(r"EAACEdEose0cBA[0-9A-Za-z]{80,200}"),
    },
    # 21
    {
        "id": "slack-webhook",
        "name": "Slack Webhook URL",
        "severity": "high",
        "regex": re.compile(
            r"https?://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+"
        ),
    },
    # 22
    {
        "id": "azure-connection-string",
        "name": "Azure / SQL Connection String",
        "severity": "high",
        "regex": re.compile(
            r"(?:Server|Data\s*Source)=[^;]+;(?:Initial\s*Catalog|Database)=[^;]+;.*?(?:User\s*Id|UID)=[^;]+;.*?(?:Password|PWD)=[^;]+",
            re.IGNORECASE,
        ),
    },
    # 23
    {
        "id": "generic-private-key",
        "name": "Generic Private Key block",
        "severity": "critical",
        "regex": re.compile(
            r"-----BEGIN\s+PRIVATE\s+KEY-----"
        ),
    },
    # 24
    {
        "id": "generic-api-key-env",
        "name": "Generic API Key in env var pattern",
        "severity": "medium",
        "regex": re.compile(
            r"(?i)(?:API_KEY|API_SECRET|APP_SECRET|SECRET_KEY|ACCESS_TOKEN|"
            r"CLIENT_SECRET|DB_PASSWORD|DB_URL|DATABASE_URL)"
            r"\s*[=:]\s*['\"]?[A-Za-z0-9_\-/+=]{16,120}['\"]?"
        ),
    },
    # 25
    {
        "id": "private-key-file-ref",
        "name": "Private key file reference",
        "severity": "medium",
        "regex": re.compile(
            r"(?i)(?:-----BEGIN\s+.*?KEY-----|ssh-rsa\s+A[0-9A-Za-z+/]{20,}[=]{0,2})"
        ),
    },
    # 26
    {
        "id": "auth-header-basic",
        "name": "Basic Auth header / token",
        "severity": "medium",
        "regex": re.compile(
            r"(?i)(?:Authorization|auth)\s*[:=]\s*['\"]?(?:Basic\s+|Bearer\s+|Token\s+)"
        ),
    },
    # 27
    {
        "id": "generic-password",
        "name": "Generic password assignment",
        "severity": "medium",
        "regex": re.compile(
            r"(?i)(?:password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{4,60}['\"]"
        ),
    },
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """A single secret finding."""

    pattern_id: str
    pattern_name: str
    severity: str
    file: str
    line: int
    match: str
    context: str = ""
    entropy: Optional[float] = None

    @property
    def redacted(self) -> str:
        """Return a redacted version (show first 4 / last 4 chars)."""
        s = self.match.strip()
        if len(s) <= 12:
            return s[:4] + "****" + s[-4:] if len(s) >= 8 else "****"
        return s[:4] + "****" + s[-4:]


# ---------------------------------------------------------------------------
# Entropy calculation
# ---------------------------------------------------------------------------


def shannon_entropy(data: str) -> float:
    """Compute Shannon entropy of a string."""
    if not data:
        return 0.0
    entropy = 0.0
    length = len(data)
    for c in set(data):
        p = data.count(c) / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


HIGH_ENTROPY_THRESHOLD = 4.5


def is_high_entropy(s: str) -> bool:
    """Check if a string looks like a high-entropy token."""
    # Only check strings of reasonable length
    if len(s) < 16:
        return False
    # Skip pure hex strings (UUIDs, hashes used for IDs)
    if re.match(r'^[0-9a-fA-F]+$', s):
        return False
    # Skip purely numeric strings
    if re.match(r'^[0-9]+$', s):
        return False
    # Skip obvious non-secrets
    if s.lower() in ('true', 'false', 'none', 'null', 'undefined', 'nan'):
        return False
    ent = shannon_entropy(s)
    return ent >= HIGH_ENTROPY_THRESHOLD


# ---------------------------------------------------------------------------
# Scanning logic
# ---------------------------------------------------------------------------

# Binary extension blacklist — skip these files entirely
BINARY_EXTENSIONS: set = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot",
    ".mp3", ".mp4", ".avi", ".mov", ".wmv", ".flv",
    ".zip", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".pyc", ".pyo", ".pyd",
    ".o", ".so", ".dll", ".dylib", ".exe", ".bin",
    ".class", ".jar",
    ".whl", ".egg", ".tar",
    ".ico", ".icns",
}

# Files to always skip
SKIP_FILES: set = {
    ".gitignore", ".gitattributes", ".gitmodules",
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "poetry.lock", "Gemfile.lock",
    "*.pyc",
}

# Directories to never scan
SKIP_DIRS: set = {
    ".git", ".svn", ".hg", "__pycache__", ".venv", "venv",
    "node_modules", ".next", "dist", "build", ".tox",
    ".idea", ".vscode", ".DS_Store",
    ".bundle", "vendor/bundle", "target", "bin", "obj",
}


def is_binary_file(filepath: str, sample_size: int = 8192) -> bool:
    """Quick heuristic: check if first bytes contain a null byte."""
    try:
        with open(filepath, "rb") as f:
            head = f.read(sample_size)
        return b"\0" in head
    except Exception:
        return True  # treat unreadable as binary


def scan_file(filepath: str, use_entropy: bool = True) -> List[Finding]:
    """Scan a single file and return all findings."""
    findings: List[Finding] = []

    # Skip by extension
    ext = os.path.splitext(filepath)[1].lower()
    if ext in BINARY_EXTENSIONS:
        return findings

    # Skip by filename
    basename = os.path.basename(filepath)
    if basename in SKIP_FILES:
        return findings

    # Quick binary check
    if is_binary_file(filepath):
        return findings

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception:
        return findings

    for lineno, line in enumerate(lines, start=1):
        stripped = line.rstrip("\n").rstrip("\r")

        for pat in PATTERNS:
            for match in pat["regex"].finditer(stripped):
                matched_text = match.group()
                # Skip lines that look like test fixtures containing tokens
                if is_likely_test_fixture(stripped, matched_text):
                    continue

                finding = Finding(
                    pattern_id=pat["id"],
                    pattern_name=pat["name"],
                    severity=pat["severity"],
                    file=filepath,
                    line=lineno,
                    match=matched_text[:120],  # cap display length
                    context=stripped[:200].strip(),
                )
                findings.append(finding)

        # Entropy-based detection (catch potential unknown tokens)
        if use_entropy:
            for token in extract_potential_tokens(stripped):
                if is_high_entropy(token):
                    # Check if it was already flagged by a pattern
                    already_flagged = any(
                        f.match == token for f in findings
                    )
                    if not already_flagged:
                        finding = Finding(
                            pattern_id="high-entropy",
                            pattern_name="High-Entropy String (potential secret)",
                            severity="low",
                            file=filepath,
                            line=lineno,
                            match=token[:120],
                            context=stripped[:200].strip(),
                            entropy=shannon_entropy(token),
                        )
                        findings.append(finding)

    return findings


def extract_potential_tokens(line: str) -> List[str]:
    """Extract strings that look like they could be tokens or secrets."""
    tokens: List[str] = []

    # Match quoted strings
    for m in re.finditer(r"""['"]([A-Za-z0-9_\-/+=]{20,80})['"]""", line):
        tokens.append(m.group(1))

    # Match assignment values: KEY=value or KEY: value
    for m in re.finditer(r"""(?::\s*|=\s*|=>\s*)([A-Za-z0-9_\-/+=]{20,80})(?:\s|$|,)""", line):
        val = m.group(1)
        # Avoid matching common words
        if not val.isdigit() and not val.lower() in (
            "true", "false", "none", "null", "undefined"
        ):
            tokens.append(val)

    # Match standalone base64-like strings
    for m in re.finditer(r"\b([A-Za-z0-9+/]{40,})\b", line):
        tokens.append(m.group())

    return tokens


def is_likely_test_fixture(line: str, matched_text: str) -> bool:
    """Heuristic to filter out test fixtures and example tokens."""
    lowline = line.lower()
    indicators = [
        "example", "placeholder", "test_token", "fake_key",
        "your-key-here", "your_api_key", "changeme", "xxxx",
        "sample", "dummy", "test-", "test_", "mock_",
        "00000000-0000-0000-0000", "xxxxxxxx",
    ]
    for ind in indicators:
        if ind in lowline:
            return True
    return False


def scan_path(path: str, use_entropy: bool = True) -> List[Finding]:
    """Recursively scan a file or directory."""
    if not os.path.exists(path):
        print(f"Error: path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    all_findings: List[Finding] = []

    if os.path.isfile(path):
        return scan_file(path, use_entropy=use_entropy)

    for root, dirs, files in os.walk(path):
        # Prune skipped directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in files:
            fpath = os.path.join(root, fname)
            all_findings.extend(scan_file(fpath, use_entropy=use_entropy))

    return all_findings


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------


SEVERITY_COLORS = {
    "critical": "\033[91m",  # red
    "high": "\033[93m",      # yellow
    "medium": "\033[94m",    # blue
    "low": "\033[90m",       # grey
}
RESET = "\033[0m"


def color(text: str, severity: str) -> str:
    """Apply ANSI color for severity level (noop on Windows without VT support)."""
    if not sys.stdout.isatty():
        return text
    c = SEVERITY_COLORS.get(severity, "")
    return f"{c}{text}{RESET}"


def print_findings(findings: List[Finding], detailed: bool = True) -> None:
    """Pretty-print findings grouped by file."""
    if not findings:
        print("No secrets found.")
        return

    # Group by file
    by_file: dict = {}
    for f in findings:
        by_file.setdefault(f.file, []).append(f)

    total = len(findings)
    by_severity: dict = {}
    for f in findings:
        by_severity[f.severity] = by_severity.get(f.severity, 0) + 1

    print(f"\n{'='*60}")
    print(f"  SECRET SCANNER REPORT — {total} finding(s)")
    print(f"{'='*60}")

    for sev in ("critical", "high", "medium", "low"):
        count = by_severity.get(sev, 0)
        if count:
            print(f"    {sev.upper()}: {count}", file=sys.stderr)

    print()

    for filepath, file_findings in sorted(by_file.items()):
        print(f"\n  [{filepath}]")
        print(f"  {'-' * (len(filepath) + 4)}")
        for f in file_findings:
            severity_tag = color(f"[{f.severity.upper()}]", f.severity)
            print(f"    {severity_tag}  {f.pattern_name} (line {f.line})")
            print(f"           Match: {color(f.redacted, f.severity)}")
            if detailed and f.context:
                ctx = f.context[:140]
                print(f"           Context: {ctx}")

    print(f"\n{'='*60}")
    print(f"  Scan complete. {total} finding(s).")
    print(f"{'='*60}\n")


def print_json_output(findings: List[Finding]) -> None:
    """Print findings as JSON array."""
    import json

    output = []
    for f in findings:
        output.append({
            "pattern_id": f.pattern_id,
            "pattern_name": f.pattern_name,
            "severity": f.severity,
            "file": f.file,
            "line": f.line,
            "redacted": f.redacted,
            "context": f.context[:200] if f.context else "",
            "entropy": round(f.entropy, 2) if f.entropy is not None else None,
        })

    print(json.dumps(output, indent=2))


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def cmd_list_patterns() -> None:
    """Print all supported detection patterns."""
    print(f"\n  {'ID':<30} {'Name':<45} {'Severity':<10}")
    print(f"  {'-'*30} {'-'*45} {'-'*10}")
    for pat in sorted(PATTERNS, key=lambda p: p["id"]):
        sev = color(pat["severity"].upper(), pat["severity"])
        print(f"  {pat['id']:<30} {pat['name']:<45} {sev}")
    print(f"\n  Total patterns: {len(PATTERNS)} regex rules")
    print(f"  + high-entropy string detection (Shannon entropy >= {HIGH_ENTROPY_THRESHOLD})\n")


def cmd_scan(args: List[str]) -> None:
    """Scan a file or directory."""
    if not args:
        print("Usage: secret_scanner.py scan <file-or-dir> [--json]", file=sys.stderr)
        sys.exit(1)

    path = args[0]
    use_json = "--json" in args

    findings = scan_path(path, use_entropy=True)

    if use_json:
        print_json_output(findings)
    else:
        print_findings(findings)

    # Exit with non-zero if critical findings
    critical = [f for f in findings if f.severity == "critical"]
    if critical:
        sys.exit(2)


def cmd_check(args: List[str]) -> None:
    """Check a single file with detailed output."""
    if not args:
        print("Usage: secret_scanner.py check <file>", file=sys.stderr)
        sys.exit(1)

    filepath = args[0]
    if not os.path.isfile(filepath):
        print(f"Error: not a file: {filepath}", file=sys.stderr)
        sys.exit(1)

    findings = scan_file(filepath, use_entropy=True)
    print_findings(findings, detailed=True)

    if any(f.severity == "critical" for f in findings):
        sys.exit(2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Secret Scanner — detect leaked secrets, keys, and tokens in files.",
    )
    parser.add_argument(
        "--version", action="version", version="secret-scanner 1.0.0"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    scan_p = sub.add_parser("scan", help="Scan a file or directory recursively")
    scan_p.add_argument("path", nargs="?", help="File or directory to scan")
    scan_p.add_argument("--json", action="store_true", help="JSON output")

    check_p = sub.add_parser("check", help="Deep-check a single file")
    check_p.add_argument("file", nargs="?", help="File to check")

    sub.add_parser("list-patterns", help="List all detection patterns")

    parsed, rest = parser.parse_known_args()

    if parsed.command == "list-patterns":
        cmd_list_patterns()
    elif parsed.command == "scan":
        args = rest if not parsed.path else [parsed.path] + rest
        if getattr(parsed, "json", False):
            args.append("--json")
        cmd_scan(args)
    elif parsed.command == "check":
        cmd_check(rest if not parsed.file else [parsed.file] + rest)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
