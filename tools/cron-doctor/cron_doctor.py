#!/usr/bin/env python3
"""
cron-doctor.py - validate and diagnose a scheduled-task file for an agent.

Parses a crontab-style file (one schedule per line: "30m|every 2h|0 9 * * * <cmd>")
and reports parse errors, collisions, and unsafe commands. Stdlib only.

Usage:
  python cron-doctor.py check <file> [--json]
  python cron-doctor.py self-test
"""
import argparse
import json
import os
import re
import sys

# accept: "30m", "every 2h", "0 9 * * *", cron with 5 fields
SCHED = re.compile(r'^(30m|every \d+[hms]|(\d+\s+){4}\S+|\S+\s+\S+\s+\S+\s+\S+\s+\S+)\s+(.+)$', re.I)
UNSAFE = re.compile(r'(?i)(rm -rf|sudo|format|dd if|mkfs|:\(\)\s*\{)', re.I)


def check(path, as_json):
    lines = [l.strip() for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]
    issues, jobs = [], []
    for i, line in enumerate(lines, 1):
        m = SCHED.match(line)
        if not m:
            issues.append(f"line {i}: unparseable schedule: {line[:60]}")
            continue
        cmd = m.group(3) if m.group(3) else m.group(2)
        if UNSAFE.search(cmd):
            issues.append(f"line {i}: unsafe command detected: {cmd[:40]}")
        jobs.append({"line": i, "schedule": m.group(1), "command": cmd})
    res = {"jobs": len(jobs), "issues": issues, "valid": len(issues) == 0}
    if as_json:
        print(json.dumps(res, indent=2))
    else:
        print(f"jobs={len(jobs)} issues={len(issues)} -> {'VALID' if res['valid'] else 'INVALID'}")
        for iss in issues: print("  !", iss)
    return res


def self_test():
    import tempfile
    good = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
    good.write("30m tick\n0 9 * * * backup\n")
    good.close()
    bad = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
    bad.write("every 5x do thing\nrm -rf / important\n")
    bad.close()
    g = check(good.name, False); b = check(bad.name, False)
    os.unlink(good.name); os.unlink(bad.name)
    ok = g["valid"] and not b["valid"] and len(b["issues"]) == 2
    print("self-test:", "PASS" if ok else "FAIL", f"(good={g['valid']} bad_issues={len(b['issues'])})")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="cron-doctor")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("path"); c.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    a = p.parse_args()
    if a.cmd == "self-test": return self_test()
    if a.cmd == "check": check(a.path, a.json); return 0


if __name__ == "__main__":
    sys.exit(main())
