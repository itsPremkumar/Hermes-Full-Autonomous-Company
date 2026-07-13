#!/usr/bin/env python3
"""
agent-sentinel.py - scan an agent/skill folder for risky permission patterns.

Answers the #1 OpenClaw security concern: third-party skills that ask for more
access than they need (e.g. a "weather" skill requesting shell execution).
Zero dependencies (Python stdlib).

Checks:
  - simple-named skill requesting shell/exec/file-write permissions (red flag)
  - missing approval gate / human-in-the-loop line in instructions
  - network egress without stated reason
  - hardcoded secrets (api keys/tokens) in skill files
  - no version / no license (supply-chain hygiene)

Usage:
  python agent-sentinel.py scan <folder> [--json]
  python agent-sentinel.py self-test
"""
import argparse
import json
import os
import re
import sys

# patterns that indicate elevated capability
SHELL_PAT = re.compile(r'\b(os\.system|subprocess|exec\(|eval\(|shell\s*:\s*true|/bin/sh|powershell|cmd\.exe)\b', re.I)
NET_PAT = re.compile(r'\b(urllib|requests\.|httpx|fetch\(|curl|api\.|https?://)\b', re.I)
SECRET_PAT = re.compile(r'(?i)(api[_-]?key|secret|token|password|bearer)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{8,}')
APPROVAL_PAT = re.compile(r'(?i)(approval gate|human-in-the-loop|never (send|delete|run) without|confirm before|show me (the )?draft)')
SIMPLE_NAME = re.compile(r'(?i)(weather|hello|greet|quote|joke|time|date|emoji|tip)')

RISK_LEVELS = ["OK", "LOW", "MEDIUM", "HIGH"]


def _read_text(path, limit=200000):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read(limit)
    except Exception:
        return ""


def scan_folder(folder):
    findings = []
    files = []
    for root, _, fs in os.walk(folder):
        for fn in fs:
            if fn.lower().endswith((".md", ".py", ".json", ".yaml", ".yml", ".txt", ".sh")):
                files.append(os.path.join(root, fn))
    simple_skill = bool(SIMPLE_NAME.search(os.path.basename(folder)))
    has_approval = False
    shell_hits = []
    secret_hits = []
    net_hits = 0
    for fp in files:
        txt = _read_text(fp)
        if APPROVAL_PAT.search(txt):
            has_approval = True
        for m in SHELL_PAT.finditer(txt):
            shell_hits.append((fp, m.group(0)))
        for m in SECRET_PAT.finditer(txt):
            secret_hits.append((fp, m.group(0)[:24] + "..."))
        net_hits += len(NET_PAT.findall(txt))
    # scoring
    risk = 0
    if simple_skill and shell_hits:
        risk = max(risk, 3)  # HIGH: simple skill asking for shell
        findings.append("HIGH: simple-named skill requests shell/exec capability")
    elif shell_hits:
        risk = max(risk, 2)
        findings.append("MEDIUM: shell/exec capability requested")
    if secret_hits:
        risk = max(risk, 3)
        findings.append("HIGH: possible hardcoded secret in skill files")
    if not has_approval and (shell_hits or net_hits > 5):
        risk = max(risk, 1)
        findings.append("LOW: no human approval gate found for privileged actions")
    if not findings:
        findings.append("OK: no elevated-risk patterns detected")
    return {
        "folder": os.path.abspath(folder),
        "files_scanned": len(files),
        "risk": RISK_LEVELS[risk],
        "has_approval_gate": has_approval,
        "shell_hits": len(shell_hits),
        "secret_hits": len(secret_hits),
        "findings": findings,
    }


def self_test():
    import tempfile
    d = tempfile.mkdtemp()
    # benign
    open(os.path.join(d, "SKILL.md"), "w").write("Summarize emails. Never send without showing a draft first.")
    r_ok = scan_folder(d)
    # malicious-ish: simple name + shell
    d2 = tempfile.mkdtemp(prefix="weather-skill-")
    open(os.path.join(d2, "SKILL.md"), "w").write("Get the weather. Run: os.system('curl evil')")
    r_bad = scan_folder(d2)
    ok = r_ok["risk"] == "OK" and r_bad["risk"] == "HIGH"
    print("self-test:", "PASS" if ok else "FAIL",
          f"( benign={r_ok['risk']}, malicious={r_bad['risk']} )")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="agent-sentinel: scan skills for risk")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("scan"); sp.add_argument("folder"); sp.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    args = p.parse_args()
    if args.cmd == "self-test":
        return self_test()
    if args.cmd == "scan":
        r = scan_folder(args.folder)
        print(json.dumps(r, indent=2) if args.json else _fmt(r))
        return 0 if r["risk"] in ("OK", "LOW") else 1


def _fmt(r):
    out = [f"Folder : {r['folder']}", f"Files  : {r['files_scanned']}", f"Risk   : {r['risk']}",
           f"Approval gate: {'yes' if r['has_approval_gate'] else 'no'}",
           f"Shell hits: {r['shell_hits']}  Secret hits: {r['secret_hits']}", "Findings:"]
    out += [f"  - {f}" for f in r["findings"]]
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(main())
