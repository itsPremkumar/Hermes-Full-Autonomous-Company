#!/usr/bin/env python3
"""
Autonomous Backend Agent (DevOps/Data) — Pipeline #18 (from research/MONEY_IDEAS_2026.md, rank #3 NEW)

Generates ready-to-sell autonomous-backend-agent service packages (title, description,
3 tiers, SEO tags) + an importable n8n workflow JSON for delivery automation.

Validated 2026 market data (see research/MONEY_IDEAS_2026.md for full citations):
  - AI-agent integration retainers: $2,500-$6,000/mo (betonai rate card, 54 invoices, Jun 2026)
  - n8n self-hosted premium over Zapier: +40-60% (betonai rate card)
  - Fiverr "AI Agents" category: $500-$10,000 (memvers, Jul 2026)
  - Free stack: Flowise + n8n + Crawl4AI + pgvector + your verify-untested-repo /
    codebase-inspection skills — all OSS / self-hosted. No paid agent framework.

Usage:
  python pipeline18_backend_agent.py --service "data-agent" --price 1500
  python pipeline18_backend_agent.py --list
  python pipeline18_backend_agent.py --service devops-agent --out be.json
  python pipeline18_backend_agent.py self-test
Zero dependencies (stdlib only).
"""
import argparse
import json
import sys

# ---- Validated 2026 pricing/demand data ----
SERVICES = {
    "data-agent": {
        "title": "I will build an autonomous data-pipeline agent for your business",
        "outcome": "an agent that scrapes, cleans, enriches, and loads data into your DB on a schedule — hands-free",
        "tools": "Crawl4AI + n8n + pgvector + Flowise — all free/self-hosted",
        "margin_note": "Charge $1,500-$4,000 setup + $499-$1,500/mo retainer",
        "tags": ["ai agent", "data pipeline", "web scraping", "automation",
                 "crawl4ai", "n8n", "pgvector", "etl"],
        "default_price": 1500,
    },
    "devops-agent": {
        "title": "I will deploy an autonomous DevOps monitoring & fix agent",
        "outcome": "an agent that watches your repos/services, runs checks, and opens fix PRs or alerts on failure",
        "tools": "n8n + your verify-untested-repo + codebase-inspection + Flowise — all free",
        "margin_note": "Charge $1,200-$3,500 setup + $399-$1,200/mo retainer",
        "tags": ["devops automation", "ai agent", "ci cd", "monitoring",
                 "n8n", "code review", "site reliability", "opensource"],
        "default_price": 1200,
    },
    "research-agent": {
        "title": "I will build an autonomous market/competitor research agent",
        "outcome": "an agent that monitors competitors, pricing, and news and emails you a weekly digest",
        "tools": "Crawl4AI + n8n + Listmonk + Flowise — all free/self-hosted",
        "margin_note": "Charge $800-$2,500 setup + $299-$999/mo retainer",
        "tags": ["market research", "competitor monitoring", "ai agent", "crawl4ai",
                 "n8n", "listmonk", "business intelligence", "automation"],
        "default_price": 900,
    },
    "crm-agent": {
        "title": "I will wire an autonomous CRM/enrichment agent into your stack",
        "outcome": "an agent that watches your CRM, enriches new leads, and triggers follow-up flows",
        "tools": "n8n + Crawl4AI + maps-cli patterns + Flowise — all free/self-hosted",
        "margin_note": "Charge $1,000-$3,000 setup + $349-$999/mo retainer",
        "tags": ["crm automation", "lead enrichment", "ai agent", "n8n",
                 "crawl4ai", "sales automation", "workflow", "b2b"],
        "default_price": 1000,
    },
}


def build_package(service_key, price=None):
    s = SERVICES[service_key]
    price = price or s["default_price"]
    tiers = build_tiers(service_key, price)
    desc = f"""🔧 {s['title']}

I deliver {s['outcome']} using {s['tools']}.

✅ What you get:
• Done-for-you setup — no technical skills needed
• Free, open-source tools (you own it, no lock-in)
• {s['margin_note']}
• 7-day support after delivery

📦 Packages:
{bullet_tiers(tiers)}

🚀 How it works:
1. You tell me your stack/goals (form on order)
2. I build & test the autonomous agent
3. I hand over + record a 5-min Loom walkthrough

⚡ Why me: I use the same tools that power a 100-skill autonomous company.
"""
    return {
        "service": service_key,
        "package_title": s["title"],
        "price": price,
        "tags": s["tags"],
        "description": desc,
        "packages": tiers,
        "n8n_workflow": build_n8n_workflow(service_key, s),
    }


def build_tiers(service_key, price):
    return [
        {"name": "Basic", "price": max(price // 4, 30),
         "delivery": "5 days", "revisions": 1,
         "features": ["Single agent", "1 workflow", "Email support"]},
        {"name": "Standard", "price": price,
         "delivery": "10 days", "revisions": 2,
         "features": ["Setup + test", "Up to 3 agents", "Loom walkthrough", "7-day support"]},
        {"name": "Premium", "price": price * 2,
         "delivery": "14 days", "revisions": 3,
         "features": ["Full system", "Unlimited agents", "Monthly retainer option", "Priority support"]},
    ]


def bullet_tiers(tiers):
    out = []
    for t in tiers:
        out.append(f"• {t['name']} (${t['price']}, {t['delivery']}, {t['revisions']} rev): "
                   + ", ".join(t["features"]))
    return "\n".join(out)


def build_n8n_workflow(service_key, s):
    return {
        "name": f"deliver-be-{service_key}",
        "nodes": [
            {"parameters": {}, "name": "Webhook / Schedule (intake)",
             "type": "n8n-nodes-base.webhook", "typeVersion": 1, "position": [0, 0]},
            {"parameters": {}, "name": "Agent logic (Flowise/Crawl4AI)",
             "type": "n8n-nodes-base.code", "typeVersion": 1, "position": [300, 0]},
            {"parameters": {}, "name": "Deliver + notify",
             "type": "n8n-nodes-base.emailSend", "typeVersion": 1, "position": [600, 0]},
        ],
        "connections": {
            "Webhook / Schedule (intake)": {"main": [[{"node": "Agent logic (Flowise/Crawl4AI)", "type": "main", "index": 0}]]},
            "Agent logic (Flowise/Crawl4AI)": {"main": [[{"node": "Deliver + notify", "type": "main", "index": 0}]]},
        },
        "note": f"Tools: {s['tools']}. Replace code node with your agent logic.",
    }


def main():
    p = argparse.ArgumentParser(description="Autonomous Backend Agent — Pipeline #18")
    p.add_argument("--service", help="service key: " + ", ".join(SERVICES.keys()))
    p.add_argument("--price", type=int, help="override price")
    p.add_argument("--out", help="write package JSON to file")
    p.add_argument("--list", action="store_true", help="list services")
    p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()

    if a.list:
        for k, v in SERVICES.items():
            print(f"  {k:14} {v['default_price']:>5}/gig  {v['title'][:44]}")
        return

    if a.cmd == "self-test" and not a.service:
        for k in SERVICES:
            pkg = build_package(k)
            assert pkg["package_title"] and pkg["description"] and len(pkg["packages"]) == 3
            assert pkg["n8n_workflow"]["name"].startswith("deliver-be-")
            assert all(isinstance(t, str) and t for t in pkg["tags"])
        print(f"self-test: OK — {len(SERVICES)} services, all generate valid packages + n8n stubs")
        return

    if not a.service or a.service not in SERVICES:
        print("ERROR: --service required. Choose from: " + ", ".join(SERVICES.keys()))
        sys.exit(1)

    pkg = build_package(a.service, a.price)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(pkg, f, indent=2)
        print(f"Wrote package JSON -> {a.out}")
    else:
        pkgs = ", ".join(f"{t['name']}(${t['price']})" for t in pkg["packages"])
        print(f"\n📦 PACKAGE: {pkg['package_title']}")
        print(f"💲 Price: ${pkg['price']} | Tags: {', '.join(pkg['tags'][:5])}")
        print(f"📋 Packages: {pkgs}")
        print(f"⚙️  n8n workflow: {pkg['n8n_workflow']['name']} ({len(pkg['n8n_workflow']['nodes'])} nodes)")


if __name__ == "__main__":
    main()
