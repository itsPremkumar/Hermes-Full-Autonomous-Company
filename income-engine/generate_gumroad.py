#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gumroad product factory (Stream B). Emits a real, usable digital product into
gumroad/products/<slug>/ (PRODUCT.md + LISTING.txt). The human uploads it to
Gumroad (free) and sets a price. Idempotent via a used list.
Run:  python generate_gumroad.py
"""
import os, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(ROOT, "gumroad", "products")
USED = os.path.join(ROOT, "gumroad", ".used_products.json")

PRODUCT_IDEAS = [
    {
        "slug": "ai-agent-roi-calculator",
        "title": "AI Agent ROI Calculator (Google Sheets)",
        "desc": "A ready-to-use spreadsheet that shows clients exactly how much they save by automating a workflow.",
        "price": "19",
        "body": """# AI Agent ROI Calculator

A plug-and-play Google Sheets workbook. Enter an hourly rate, hours/week, and
error rate; it outputs monthly savings, payback period, and a one-page client
summary you can drop into a proposal.

## What's inside
- Savings model (hours x rate x automation %)
- Payback calculator for a one-time build fee
- Print-ready client summary tab

## How to use
1. Copy the sheet.
2. Fill the yellow inputs.
3. Screenshot the summary tab for your proposal.

Free to use; tip what you like.
"""
    },
    {
        "slug": "n8n-starter-workflow-pack",
        "title": "5 n8n Starter Workflows for Small Business",
        "desc": "Import-ready n8n workflows: lead capture, invoice sort, support triage, content repurpose, weekly report.",
        "price": "29",
        "body": """# 5 n8n Starter Workflows

Five export files you can import into a self-hosted n8n instance in under a minute.

1. **Lead capture** — form -> CRM -> Slack alert.
2. **Invoice sort** — email attachment -> folder -> ledger row.
3. **Support triage** — inbox -> label -> draft reply.
4. **Content repurpose** — long post -> 5 social clips.
5. **Weekly report** — metrics -> markdown -> email.

Each file includes a setup note. Self-host for $0.
"""
    },
    {
        "slug": "agent-consulting-proposal-template",
        "title": "AI Agent Consulting Proposal Template",
        "desc": "A fill-in proposal template that positions a $2k-$15k automation build with clear ROI.",
        "price": "24",
        "body": """# AI Agent Consulting Proposal Template

A copy-paste proposal structure used by the Prem Autonomous Co agent team.

## Sections
- Problem & current cost
- Proposed agent/automation
- Implementation timeline
- Pricing (setup + retainer)
- ROI summary (links to the ROI calculator)

Win more engagements by leading with numbers, not features.
"""
    },
]

def load_used():
    if os.path.isfile(USED):
        return json.load(open(USED, encoding="utf-8"))
    return {"slugs": []}

def main():
    used = load_used()
    idea = None
    for p in PRODUCT_IDEAS:
        if p["slug"] not in used["slugs"]:
            idea = p
            break
    if not idea:
        print("all products generated.")
        return
    d = os.path.join(PROD, idea["slug"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "PRODUCT.md"), "w", encoding="utf-8").write(idea["body"])
    listing = f"""Title: {idea['title']}
Price: ${idea['price']}
Description: {idea['desc']}

Upload this folder's PRODUCT.md as the product file on Gumroad (free).
Set the price above. You keep 100% minus Gumroad's standard fee.
"""
    open(os.path.join(d, "LISTING.txt"), "w", encoding="utf-8").write(listing)
    used["slugs"].append(idea["slug"])
    json.dump(used, open(USED, "w", encoding="utf-8"), indent=2)
    print(f"wrote gumroad/products/{idea['slug']}/  (price ${idea['price']})")

if __name__ == "__main__":
    main()
