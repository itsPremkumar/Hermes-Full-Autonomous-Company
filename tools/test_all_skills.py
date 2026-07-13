#!/usr/bin/env python3
"""
test_all_skills.py - canonical verification for this company's tools + marketing drafts.

Run:  python tools/test_all_skills.py
Exit 0 = all pass. This is the repo's test command (no external deps).
"""
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = {
    "agent-cost-tracker": "agent_cost_tracker.py",
    "agent-health": "agent_health.py",
    "prompt-lint": "prompt_lint.py",
    "skill-lint": "skill_lint.py",
    "agent-sentinel": "agent_sentinel.py",
}


def check(name, cond):
    print(("PASS" if cond else "FAIL"), "-", name)
    return bool(cond)


def main():
    ok = True
    # 1) every tool self-tests
    for name, fn in TOOLS.items():
        p = os.path.join(REPO, "tools", name, fn)
        r = subprocess.run([sys.executable, p, "self-test"], capture_output=True, text=True)
        ok = check(f"tool {name} self-test", "self-test: PASS" in r.stdout) and ok

    # 2) agent-caps has its own test file
    ac = os.path.join(REPO, "tools", "agent-caps", "test_agent_caps.py")
    if os.path.isfile(ac):
        r = subprocess.run([sys.executable, ac], capture_output=True, text=True)
        ok = check("agent-caps test suite", r.returncode == 0) and ok

    # 3) every Moltbook draft: valid + honest + links a live ClawHub skill + donation ask
    mdir = os.path.join(REPO, "revenue", "moltbook")
    for fn in os.listdir(mdir):
        if not fn.startswith("post-") or not fn.endswith(".json"):
            continue
        d = json.load(open(os.path.join(mdir, fn), encoding="utf-8"))
        body = d.get("content", "")
        cond = (bool(d.get("title")) and bool(body) and bool(d.get("submolt"))
                and "clawhub.ai/skills/skills/" in body
                and ("Sponsors" in body or "Buy Me a Coffee" in body)
                and ("guarantee" not in body.lower() or "appreciated" in body or "not a revenue" in body))
        ok = check(f"draft {fn} valid+honest+linked", cond) and ok

    # 4) no secret leaked into moltbook dir
    leaked = any("moltbook_key" in f for f in os.listdir(mdir))
    ok = check("no .moltbook_key in moltbook dir", not leaked) and ok

    print("\nCANONICAL TEST SUITE:", "ALL PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
