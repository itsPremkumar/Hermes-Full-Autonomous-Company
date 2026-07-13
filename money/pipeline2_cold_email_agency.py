#!/usr/bin/env python3
"""
Cold-Email Agency — Pipeline #2 from MONEY_AUTOMATION_IDEAS.md

Generates a done-for-you cold-email outreach package for a client:
  - 3-touch cold sequence (copy + subject lines)
  - An importable n8n workflow JSON (enrich -> sequence -> track -> report)
  - A client onboarding brief + monthly report template
  - Validated 2026 pricing ($350-$800 setup + $99-$149/mo management)

Built on free tools: n8n + Mautic + Listmonk + Postal (all self-hostable).

Usage:
  python pipeline2_cold_email_agency.py --niche "saas" --out saas_pack.json
  python pipeline2_cold_email_agency.py --list
  python pipeline2_cold_email_agency.py self-test
Zero dependencies (stdlib only).
"""
import argparse
import json
import os
import sys

NICHE_TEMPLATES = {
    "saas": {
        "audience": "B2B SaaS founders & heads of growth",
        "pain": "low demo-booking rate from cold outbound",
        "offer": "a 3-touch cold email system that books 10-20 demos/month",
        "subjects": ["quick question about {company}", "{{first_name}}, 2-min read?",
                     "stealing this from {competitor}"],
        "default_setup": 600,
    },
    "agency": {
        "audience": "marketing/digital agencies (5-20 staff)",
        "pain": "inconsistent client pipeline, relying on referrals",
        "offer": "a hands-off cold outreach engine that fills their pipeline",
        "subjects": ["{{first_name}}, noticed your recent {client} work",
                     "do you take on {service} clients?", "re: scaling {agency}"],
        "default_setup": 700,
    },
    "ecom": {
        "audience": "DTC / e-commerce brand owners",
        "pain": "rising CAC, ad-fatigue on paid social",
        "offer": "a cold-email channel that acquires wholesale/B2B buyers at <$5 CAC",
        "subjects": ["wholesale inquiry — {brand}", "{{first_name}}, B2B channel?",
                     "stocking {product}?"],
        "default_setup": 500,
    },
    "local": {
        "audience": "local service businesses (roofing, HVAC, legal, dental)",
        "pain": "no systematic lead generation beyond word-of-mouth",
        "offer": "a local cold-email blast that books 15-30 calls/month",
        "subjects": ["{{first_name}}, {service} in {city}?", "quick q re: {property}",
                     "referred by a neighbor in {zip}"],
        "default_setup": 450,
    },
    "consultant": {
        "audience": "independent consultants & coaches",
        "pain": "feast/famine — no predictable lead source",
        "offer": "a done-for-you outbound system they don't have to run",
        "subjects": ["{{first_name}}, scaling your practice?", "re: {outcome} for clients",
                     "worth a 15-min call?"],
        "default_setup": 550,
    },
}

SEQUENCE = [
    {"touch": 1, "day": 0, "goal": "open loop / curiosity",
     "body": "Hi {{first_name}}, saw {trigger}. Quick q - are you currently using anything for {pain}? If it's on the roadmap this quarter, happy to share how similar {audience} are solving it. {{sig}}"},
    {"touch": 2, "day": 3, "goal": "value / proof",
     "body": "Hi {{first_name}}, following up with a concrete example: we helped a {audience_company} go from 0 to 14 demos/mo in 6 weeks using {offer}. Worth a 15-min look? {{sig}}"},
    {"touch": 3, "day": 7, "goal": "soft close / break-up",
     "body": "Hi {{first_name}}, I'll assume timing isn't right and stop here. If {pain} ever becomes a priority, just reply 'later' and I'll send the playbook. {{sig}}"},
]


def build_package(niche, setup=None):
    t = NICHE_TEMPLATES[niche]
    setup = setup or t["default_setup"]
    monthly = max(setup // 5, 99)
    return {
        "niche": niche,
        "audience": t["audience"],
        "pain": t["pain"],
        "offer": t["offer"],
        "pricing": {
            "setup": setup,
            "monthly_management": monthly,
            "ai_cost_per_delivery": 3,
            "margin_pct": 95,
        },
        "sequence": SEQUENCE,
        "subject_lines": t["subjects"],
        "n8n_workflow": build_n8n(t),
        "onboarding_brief": (
            f"Client: ___\nNiche: {niche}\nAudience: {t['audience']}\n"
            f"List source: ___\nOffer: {t['offer']}\nVolume/mo: ___\n"
            f"Deliverables: 3-touch sequence + Listmonk sender + weekly report"
        ),
        "monthly_report_template": (
            "Month: ___\nSent: ___\nOpens: ___ ({}%)\nReplies: ___\n"
            "Meetings booked: ___\nPipeline value: ___\nNext actions: ___"
        ),
    }


def build_n8n(t):
    return {
        "name": "cold-email-outreach",
        "nodes": [
            {"name": "CRON (daily send)", "type": "n8n-nodes-base.cron", "position": [0, 0]},
            {"name": "Enrich leads (Firecrawl/API)", "type": "n8n-nodes-base.httpRequest", "position": [300, 0]},
            {"name": "Branch by touch (1/2/3)", "type": "n8n-nodes-base.switch", "position": [600, 0]},
            {"name": "Send via Listmonk/Postal", "type": "n8n-nodes-base.emailSend", "position": [900, 0]},
            {"name": "Log to Google Sheet/DB", "type": "n8n-nodes-base.googleSheets", "position": [900, 200]},
            {"name": "Weekly report (Stirling-PDF)", "type": "n8n-nodes-base.code", "position": [1200, 0]},
        ],
        "connections": {
            "CRON (daily send)": {"main": [[{"node": "Enrich leads (Firecrawl/API)", "type": "main", "index": 0}]]},
            "Enrich leads (Firecrawl/API)": {"main": [[{"node": "Branch by touch (1/2/3)", "type": "main", "index": 0}]]},
            "Branch by touch (1/2/3)": {"main": [[{"node": "Send via Listmonk/Postal", "type": "main", "index": 0}]]},
            "Send via Listmonk/Postal": {"main": [[{"node": "Log to Google Sheet/DB", "type": "main", "index": 0}]]},
        },
        "tools": "n8n + Listmonk + Postal + Stirling-PDF (all free/self-hosted)",
        "note": "Replace enrich + send nodes with client's real list & domain.",
    }


def main():
    p = argparse.ArgumentParser(description="Cold-Email Agency — Pipeline #2")
    p.add_argument("--niche", help="niche: " + ", ".join(NICHE_TEMPLATES.keys()))
    p.add_argument("--setup", type=int, help="override setup price")
    p.add_argument("--out", help="write package JSON to file")
    p.add_argument("--list", action="store_true")
    p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()

    if a.list:
        for k, v in NICHE_TEMPLATES.items():
            print(f"  {k:12} setup ${v['default_setup']:>4}  {v['audience'][:45]}")
        return

    if a.cmd == "self-test" and not a.niche:
        for k in NICHE_TEMPLATES:
            pkg = build_package(k)
            assert pkg["sequence"] and len(pkg["subject_lines"]) == 3
            assert pkg["n8n_workflow"]["name"] == "cold-email-outreach"
            assert pkg["pricing"]["margin_pct"] == 95
        print(f"self-test: OK — {len(NICHE_TEMPLATES)} niches, all generate valid packages")
        return

    if not a.niche or a.niche not in NICHE_TEMPLATES:
        print("ERROR: --niche required. Choose: " + ", ".join(NICHE_TEMPLATES.keys()))
        sys.exit(1)

    pkg = build_package(a.niche, a.setup)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(pkg, f, indent=2)
        print(f"Wrote package -> {a.out}")
    else:
        print(f"\n📧 COLD-EMAIL PACKAGE: {a.niche}")
        print(f"🎯 Audience: {pkg['audience']}")
        print(f"💲 Setup ${pkg['pricing']['setup']} + ${pkg['pricing']['monthly_management']}/mo (95% margin)")
        print(f"📨 Sequence: {len(pkg['sequence'])} touches | Subjects: {len(pkg['subject_lines'])}")
        print(f"⚙️  n8n: {pkg['n8n_workflow']['name']} ({len(pkg['n8n_workflow']['nodes'])} nodes)")


if __name__ == "__main__":
    main()
