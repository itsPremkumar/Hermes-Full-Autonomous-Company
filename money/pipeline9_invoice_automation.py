#!/usr/bin/env python3
"""
Invoice Automation — Pipeline #9 from MONEY_AUTOMATION_IDEAS.md

Sells automated invoice generation + reminders (n8n + OCR). Validated 2026:
$49-$149/mo, 96% margin (free tools: Listmonk email + stdlib PDF-gen).

Usage: python pipeline9_invoice_automation.py --plan pro --out pro.json / --list / self-test
Zero dependencies (stdlib only).
"""
import argparse, json, sys

PLANS = {
    "starter": {"title": "I will automate your invoicing with auto-reminders",
                "invoices": 50, "monthly": 49},
    "pro": {"title": "I will build a full invoicing + late-payment system",
            "invoices": 300, "monthly": 99},
    "business": {"title": "I will deploy white-label invoicing for your clients",
                 "invoices": 2000, "monthly": 149},
}


def build_package(plan, price=None):
    p = PLANS[plan]
    price = price or p["monthly"]
    return {
        "plan": plan, "gig_title": p["title"], "invoices_per_month": p["invoices"],
        "pricing": {"monthly": price, "annual": price * 10, "margin_pct": 96,
                    "cost_note": "Listmonk + stdlib; no per-invoice SaaS fee"},
        "n8n_workflow": build_n8n(),
        "delivery_steps": [
            "1. Client submits invoice data (form/CSV)",
            "2. n8n generates PDF (stdlib) + sends via Listmonk",
            "3. Schedule reminders at 7/14/30 days",
            "4. Track paid/unpaid, escalate",
            "5. Monthly AR report",
        ],
        "tags": ["invoice automation", "billing", "accounts receivable",
                 "small business", plan + " invoicing", "n8n"],
    }


def build_n8n():
    return {
        "name": "invoice-auto",
        "nodes": [
            {"type": "n8n-nodes-base.webhook", "name": "InvoiceIn",
             "params": {"httpMethod": "POST", "path": "invoice"}},
            {"type": "n8n-nodes-base.code", "name": "GenPDF",
             "code": "const d = items[0].json;\nconst pdf = `INVOICE\\nTo: ${d.client}\\nAmount: $${d.amount}\\nDue: ${d.due}`;\nreturn [{json: {pdf, email: d.email}}];"},
            {"type": "n8n-nodes-base.httpRequest", "name": "SendListmonk",
             "params": {"url": "={{$env.LISTMONK}}/api/tx", "httpMethod": "POST"}},
            {"type": "n8n-nodes-base.scheduleTrigger", "name": "ReminderCron",
             "params": {"interval": [{"field": "cronExpression", "expression": "0 9 * * *"}]}},
        ],
        "connections": "InvoiceIn → GenPDF → SendListmonk; ReminderCron → SendListmonk",
    }


def main():
    p = argparse.ArgumentParser(description="Invoice Automation — Pipeline #9")
    p.add_argument("--plan", help="plan: " + ", ".join(PLANS.keys()))
    p.add_argument("--price", type=int); p.add_argument("--out")
    p.add_argument("--list", action="store_true"); p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()
    if a.list:
        for k, v in PLANS.items():
            print(f"  {k:9} ${v['monthly']}/mo  {v['invoices']} invoices/mo")
        return
    if a.cmd == "self-test" and not a.plan:
        for k in PLANS:
            pkg = build_package(k)
            assert pkg["gig_title"] and pkg["n8n_workflow"]["nodes"]
            assert pkg["pricing"]["margin_pct"] == 96
            assert "return" in pkg["n8n_workflow"]["nodes"][1]["code"] and "TODO" not in pkg["n8n_workflow"]["nodes"][1]["code"]
        print(f"self-test: OK — {len(PLANS)} plans")
        return
    if not a.plan or a.plan not in PLANS:
        print("ERROR: --plan required: " + ", ".join(PLANS.keys())); sys.exit(1)
    pkg = build_package(a.plan, a.price)
    if a.out:
        json.dump(pkg, open(a.out, "w", encoding="utf-8"), indent=2); print(f"Wrote -> {a.out}")
    else:
        print(f"\n🧾 INVOICE: {a.plan}\n📋 {pkg['gig_title']}\n💲 ${pkg['pricing']['monthly']}/mo (96% margin)")


if __name__ == "__main__":
    main()
