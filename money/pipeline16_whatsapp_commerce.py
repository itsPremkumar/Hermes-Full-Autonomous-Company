#!/usr/bin/env python3
"""
WhatsApp AI Commerce Agent — Pipeline #16 (from research/MONEY_IDEAS_2026.md, rank #1 NEW)

Generates ready-to-sell WhatsApp AI-agent service packages (title, description,
3 tiers, SEO tags) + an importable n8n workflow JSON for delivery automation.

Validated 2026 market data (see research/MONEY_IDEAS_2026.md for full citations):
  - WhatsApp: 3.3B active users, 200M+ businesses (demandsage.com/whatsapp-statistics, 2026)
  - WhatsApp Business msg open rate ~98%, CTR 45-60% (vs email 3-5x) — outreach demand
  - AI-agent retainer rate: $2,500-$6,000/mo (betonai rate card, 54 invoices, Jun 2026)
  - AI chatbot dev gig: $200-$1,000 (RAG tier) on Fiverr (memvers, Jul 2026)
  - Free stack: Baileys (WhiskeySockets) + Chatwoot + n8n + Whisper + local LLM —
    all OSS / self-hosted. No paid WhatsApp Business API (use Baileys Web socket).

Usage:
  python pipeline16_whatsapp_commerce.py --service "catalog-bot" --price 600
  python pipeline16_whatsapp_commerce.py --list
  python pipeline16_whatsapp_commerce.py --service order-bot --out wa.json
  python pipeline16_whatsapp_commerce.py self-test
Zero dependencies (stdlib only).
"""
import argparse
import json
import sys

# ---- Validated 2026 pricing/demand data ----
SERVICES = {
    "catalog-bot": {
        "title": "I will build you a WhatsApp AI catalog & order bot (no paid API)",
        "outcome": "a self-hosted WhatsApp bot that shows your product catalog, answers FAQs, and takes orders 24/7",
        "tools": "Baileys (WhiskeySockets) + Chatwoot + n8n + local LLM — all free/self-hosted",
        "margin_note": "Charge $500-$1,500 setup + $199-$599/mo; your cost $0 (self-hosted, no Twilio/Meta fee)",
        "tags": ["whatsapp bot", "ai agent", "ecommerce automation", "chatwoot",
                 "baileys", "n8n", "whatsapp business", "no code automation"],
        "default_price": 600,
    },
    "lead-bot": {
        "title": "I will deploy a WhatsApp lead-capture & nurture agent for your SMB",
        "outcome": "an AI agent that captures leads from WhatsApp, qualifies them, and nudges them to a call",
        "tools": "Baileys + Chatwoot + n8n + local LLM — all free/self-hosted",
        "margin_note": "Charge $400-$1,200 setup + $149-$499/mo; 98% open-rate channel beats email 3-5x",
        "tags": ["whatsapp marketing", "lead generation", "ai agent", "chatwoot",
                 "baileys", "n8n", "customer automation", "smb growth"],
        "default_price": 500,
    },
    "support-agent": {
        "title": "I will automate your WhatsApp customer support with an AI agent",
        "outcome": "a 24/7 support agent trained on your FAQs that resolves common tickets and escalates the rest",
        "tools": "Baileys + Chatwoot + n8n + local LLM + your doc-extractor skill — all free",
        "margin_note": "Charge $600-$1,800 setup + $299-$799/mo; recovers lost after-hours inquiries",
        "tags": ["whatsapp support", "ai chatbot", "customer service automation", "chatwoot",
                 "baileys", "n8n", "helpdesk automation", "rag"],
        "default_price": 800,
    },
    "broadcast-agent": {
        "title": "I will set up a WhatsApp broadcast & re-engagement agent",
        "outcome": "a compliant broadcast system that re-engages opted-in customers with AI-personalized offers",
        "tools": "Baileys + n8n + Listmonk (email fallback) — all free/self-hosted",
        "margin_note": "Charge $300-$900 setup + $99-$399/mo; 45-60% CTR vs email 3-5x",
        "tags": ["whatsapp broadcast", "re engagement", "ai marketing", "baileys",
                 "n8n", "listmonk", "retention automation", "smb"],
        "default_price": 400,
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
• Free, open-source tools (you own it, no lock-in, no per-message fees)
• {s['margin_note']}
• 7-day support after delivery

📦 Packages:
{bullet_tiers(tiers)}

🚀 How it works:
1. You tell me your products/goals (form on order)
2. I build & test the WhatsApp agent
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
         "delivery": "3 days", "revisions": 1,
         "features": ["Single flow", "1 workflow", "Email support"]},
        {"name": "Standard", "price": price,
         "delivery": "5 days", "revisions": 2,
         "features": ["Setup + test", "Up to 3 flows", "Loom walkthrough", "7-day support"]},
        {"name": "Premium", "price": price * 2,
         "delivery": "7 days", "revisions": 3,
         "features": ["Full system", "Unlimited flows", "Monthly retainer option", "Priority support"]},
    ]


def bullet_tiers(tiers):
    out = []
    for t in tiers:
        out.append(f"• {t['name']} (${t['price']}, {t['delivery']}, {t['revisions']} rev): "
                   + ", ".join(t["features"]))
    return "\n".join(out)


def build_n8n_workflow(service_key, s):
    return {
        "name": f"deliver-wa-{service_key}",
        "nodes": [
            {"parameters": {}, "name": "Baileys (WhatsApp intake)",
             "type": "n8n-nodes-base.webhook", "typeVersion": 1, "position": [0, 0]},
            {"parameters": {}, "name": "Agent / Chatwoot logic",
             "type": "n8n-nodes-base.code", "typeVersion": 1, "position": [300, 0]},
            {"parameters": {}, "name": "Deliver + notify",
             "type": "n8n-nodes-base.emailSend", "typeVersion": 1, "position": [600, 0]},
        ],
        "connections": {
            "Baileys (WhatsApp intake)": {"main": [[{"node": "Agent / Chatwoot logic", "type": "main", "index": 0}]]},
            "Agent / Chatwoot logic": {"main": [[{"node": "Deliver + notify", "type": "main", "index": 0}]]},
        },
        "note": f"Tools: {s['tools']}. Replace code node with your agent logic. Baileys repo: https://github.com/WhiskeySockets/Baileys",
    }


def main():
    p = argparse.ArgumentParser(description="WhatsApp AI Commerce Agent — Pipeline #16")
    p.add_argument("--service", help="service key: " + ", ".join(SERVICES.keys()))
    p.add_argument("--price", type=int, help="override price")
    p.add_argument("--out", help="write package JSON to file")
    p.add_argument("--list", action="store_true", help="list services")
    p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()

    if a.list:
        for k, v in SERVICES.items():
            print(f"  {k:16} {v['default_price']:>5}/gig  {v['title'][:44]}")
        return

    if a.cmd == "self-test" and not a.service:
        for k in SERVICES:
            pkg = build_package(k)
            assert pkg["package_title"] and pkg["description"] and len(pkg["packages"]) == 3
            assert pkg["n8n_workflow"]["name"].startswith("deliver-wa-")
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
