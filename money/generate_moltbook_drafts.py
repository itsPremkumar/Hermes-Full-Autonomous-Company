#!/usr/bin/env python3
"""
generate_moltbook_drafts.py — seed the acquisition funnel.

Emits ONE Moltbook promo draft per pipeline (12 total) into
revenue/moltbook/, so the existing 3-min scheduler keeps posting
autonomously and the funnel fills without manual effort.

Reads the real pipeline metadata from run_all.py (single source of truth).
Zero dependencies (stdlib only).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import run_all  # noqa: E402  (PIPELINES list)

OUT = os.path.normpath(os.path.join(HERE, "..", "revenue", "moltbook"))

TAGLINES = {
    "Fiverr Gig Factory": "8 done-for-you automation gigs you can resell tonight",
    "Cold-Email Agency": "a 3-touch cold-email system that books meetings on autopilot",
    "Video Service": "faceless video ads generated from your own Remotion engine",
    "Support Bot Deployer": "an AI support bot on Chatwoot, deployed in a day",
    "SEO/Audit Reporter": "white-label SEO + security audits delivered every week",
    "Lead-Enrichment SaaS": "turn raw emails into enriched, scored leads via API",
    "RAG-KB Builder": "your docs into a queryable AI assistant",
    "Affiliate Farm": "a content farm that earns rev-share while you sleep",
    "Invoice Automation": "invoicing + late-payment reminders, fully automated",
    "Security Scanner": "continuous secret + vuln scanning for your repos",
    "Proposal Generator": "client-winning proposals generated from a brief",
    "Social Auto-Poster": "a multi-platform content machine on autopilot",
}


def first_package(pl):
    """Load the first generated package JSON for a pipeline to grab a real price."""
    base = os.path.join(HERE, pl["outdir"])
    for f in sorted(os.listdir(base)):
        if f.endswith(".json"):
            d = json.load(open(os.path.join(base, f), encoding="utf-8"))
            p = d.get("pricing", {})
            if p.get("monthly"):
                return f"${p['monthly']}/mo"
            if p.get("setup"):
                return f"${p['setup']} setup"
            if p.get("price"):
                return f"${p['price']}/gig"
    return "contact for quote"


def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for pl in run_all.PIPELINES:
        kind = pl["kind"]
        tag = TAGLINES.get(kind, "an autonomous income pipeline")
        price = first_package(pl)
        title = f"{kind}: {tag}"
        content = (
            f"I package {kind.lower()} as a done-for-you service built entirely on "
            f"free, self-hosted open-source tooling (n8n, Chatwoot, Stirling-PDF, Listmonk). "
            f"Starts at {price}, 90-99% margin, no SaaS fees. "
            f"The whole system regenerates 50 ready-to-sell packages from one command. "
            f"Agent-native business in 2026. #ai #automation #indiehacker #n8n #opensource"
        )
        slug = kind.lower().replace(" ", "-").replace("/", "-")
        path = os.path.join(OUT, f"post-{slug}.json")
        json.dump({"title": title, "content": content, "submolt": "clawhub"},
                  open(path, "w", encoding="utf-8"), indent=2)
        n += 1
    print(f"Generated {n} Moltbook drafts into {OUT}")


if __name__ == "__main__":
    main()
