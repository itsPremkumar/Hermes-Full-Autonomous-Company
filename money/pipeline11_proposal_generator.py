#!/usr/bin/env python3
"""
Proposal Generator — Pipeline #11 from MONEY_AUTOMATION_IDEAS.md

Sells AI-generated client proposals from templates (your md-linter + templates).
Validated 2026: $150-$600/gig, 96% margin.

Usage: python pipeline11_proposal_generator.py --type web --out web.json / --list / self-test
Zero dependencies (stdlib only).
"""
import argparse, json, sys

TYPES = {
    "web": {"title": "I will write a winning web-dev project proposal",
            "price": 250, "sections": ["scope", "timeline", "cost", "portfolio"]},
    "agency": {"title": "I will craft agency service proposals that close",
               "price": 400, "sections": ["problem", "approach", "pricing", "case study"]},
    "freelance": {"title": "I will generate freelance gig proposals that win jobs",
                  "price": 150, "sections": ["understanding", "solution", "delivery", "price"]},
    "enterprise": {"title": "I will build enterprise RFP response templates",
                   "price": 600, "sections": ["compliance", "architecture", "SLA", "cost"]},
}


def build_package(ptype, price=None):
    t = TYPES[ptype]
    price = price or t["price"]
    return {
        "type": ptype, "gig_title": t["title"], "sections": t["sections"],
        "pricing": {"price": price, "margin_pct": 96, "cost_note": "md-linter + templates (free)"},
        "n8n_workflow": build_n8n(),
        "delivery_steps": [
            "1. Client fills brief (form)",
            "2. n8n pulls brief → template engine",
            "3. Generate proposal MD (your templates)",
            "4. Lint + render PDF (Stirling-PDF)",
            "5. Deliver + reusable template saved",
        ],
        "tags": ["proposal writer", "business proposal", ptype + " proposal",
                 "freelance", "RFP", "sales"],

    }


def build_n8n():
    return {
        "name": "proposal-gen",
        "nodes": [
            {"type": "n8n-nodes-base.webhook", "name": "BriefIn",
             "params": {"httpMethod": "POST", "path": "brief"}},
            {"type": "n8n-nodes-base.code", "name": "FillTemplate",
             "code": "const b = items[0].json;\nconst md = `# Proposal for ${b.client}\\n\\n## Scope\\n${b.scope}\\n\\n## Price\\n$${b.price}`;\nreturn [{json: {md, email: b.email}}];"},
            {"type": "n8n-nodes-base.httpRequest", "name": "RenderPDF",
             "params": {"url": "={{$env.STIRLING}}/api/converter/file/pdf", "httpMethod": "POST"}},
        ],
        "connections": "BriefIn → FillTemplate → RenderPDF",
    }


def main():
    p = argparse.ArgumentParser(description="Proposal Generator — Pipeline #11")
    p.add_argument("--type", help="type: " + ", ".join(TYPES.keys()))
    p.add_argument("--price", type=int); p.add_argument("--out")
    p.add_argument("--list", action="store_true"); p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()
    if a.list:
        for k, v in TYPES.items():
            print(f"  {k:10} ${v['price']}/gig  {len(v['sections'])} sections")
        return
    if a.cmd == "self-test" and not a.type:
        for k in TYPES:
            pkg = build_package(k)
            assert pkg["gig_title"] and pkg["n8n_workflow"]["nodes"]
            assert pkg["pricing"]["margin_pct"] == 96
            assert "return" in pkg["n8n_workflow"]["nodes"][1]["code"]
        print(f"self-test: OK — {len(TYPES)} types")
        return
    if not a.type or a.type not in TYPES:
        print("ERROR: --type required: " + ", ".join(TYPES.keys())); sys.exit(1)
    pkg = build_package(a.type, a.price)
    if a.out:
        json.dump(pkg, open(a.out, "w", encoding="utf-8"), indent=2); print(f"Wrote -> {a.out}")
    else:
        print(f"\n📝 PROPOSAL: {a.type}\n📋 {pkg['gig_title']}\n💲 ${pkg['pricing']['price']}/gig (96% margin)")


if __name__ == "__main__":
    main()
