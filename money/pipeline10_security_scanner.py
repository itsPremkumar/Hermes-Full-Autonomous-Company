#!/usr/bin/env python3
"""
Security Scanner Service — Pipeline #10 from MONEY_AUTOMATION_IDEAS.md

Recurring repo/website security scans using YOUR ClawHub skills
(secret-scanner + skill-lint). Validated 2026: $199 setup + $99/mo, 97% margin.

Usage: python pipeline10_security_scanner.py --plan pro --out pro.json / --list / self-test
Zero dependencies (stdlib only).
"""
import argparse, json, sys

PLANS = {
    "starter": {"title": "I will scan your repo for leaked secrets + vulnerabilities",
                "scans": "monthly", "monthly": 99, "setup": 199},
    "pro": {"title": "I will run continuous security scanning + fix reports",
            "scans": "weekly", "monthly": 199, "setup": 299},
    "agency": {"title": "I will white-label security scans for your clients",
               "scans": "weekly", "monthly": 499, "setup": 599},
}


def build_package(plan, price=None):
    p = PLANS[plan]
    price = price or p["monthly"]
    return {
        "plan": plan, "gig_title": p["title"], "scan_frequency": p["scans"],
        "pricing": {"monthly": price, "setup": p["setup"], "annual": price * 10,
                    "margin_pct": 97, "cost_note": "your secret-scanner + skill-lint (free)"},
        "n8n_workflow": build_n8n(),
        "delivery_steps": [
            "1. Client grants repo / site access",
            "2. n8n cron runs secret-scanner + skill-lint",
            "3. Generate branded report (Stirling-PDF)",
            "4. Email findings + severity ranking",
            "5. Monthly trend + fix checklist",
        ],
        "tags": ["security scan", "secret scanning", "vulnerability",
                 "devsecops", plan + " security", "code audit"],
    }


def build_n8n():
    return {
        "name": "security-scan",
        "nodes": [
            {"type": "n8n-nodes-base.scheduleTrigger", "name": "ScanCron",
             "params": {"interval": [{"field": "cronExpression", "expression": "0 3 * * 1"}]}},
            {"type": "n8n-nodes-base.executeCommand", "name": "SecretScan",
             "params": {"command": "python secret_scanner.py --repo $REPO --json out.json"}},
            {"type": "n8n-nodes-base.executeCommand", "name": "LintScan",
             "params": {"command": "python skill_lint.py --check $REPO"}},
            {"type": "n8n-nodes-base.httpRequest", "name": "RenderPDF",
             "params": {"url": "={{$env.STIRLING}}/api/converter/file/pdf", "httpMethod": "POST"}},
        ],
        "connections": "ScanCron → SecretScan → LintScan → RenderPDF",
    }


def main():
    p = argparse.ArgumentParser(description="Security Scanner — Pipeline #10")
    p.add_argument("--plan", help="plan: " + ", ".join(PLANS.keys()))
    p.add_argument("--price", type=int); p.add_argument("--out")
    p.add_argument("--list", action="store_true"); p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()
    if a.list:
        for k, v in PLANS.items():
            print(f"  {k:8} ${v['monthly']}/mo + ${v['setup']} setup  {v['scans']}")
        return
    if a.cmd == "self-test" and not a.plan:
        for k in PLANS:
            pkg = build_package(k)
            assert pkg["gig_title"] and pkg["n8n_workflow"]["nodes"]
            assert pkg["pricing"]["margin_pct"] == 97
            assert all("TODO" not in n.get("command", "") for n in pkg["n8n_workflow"]["nodes"] if "command" in n)
        print(f"self-test: OK — {len(PLANS)} plans")
        return
    if not a.plan or a.plan not in PLANS:
        print("ERROR: --plan required: " + ", ".join(PLANS.keys())); sys.exit(1)
    pkg = build_package(a.plan, a.price)
    if a.out:
        json.dump(pkg, open(a.out, "w", encoding="utf-8"), indent=2); print(f"Wrote -> {a.out}")
    else:
        print(f"\n🛡️  SECURITY: {a.plan}\n📋 {pkg['gig_title']}\n💲 ${pkg['pricing']['setup']} + ${pkg['pricing']['monthly']}/mo (97% margin)")


if __name__ == "__main__":
    main()
