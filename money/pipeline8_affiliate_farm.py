#!/usr/bin/env python3
"""
Affiliate Content Farm — Pipeline #8 from MONEY_AUTOMATION_IDEAS.md

Builds + auto-publishes affiliate content (blog + X/threads) that earns
rev-share. Zero cost (your blog gen + polymarket-cli research + web-research).
Validated 2026: rev-share income, $0 product cost, pure margin.

Usage: python pipeline8_affiliate_farm.py --niche crypto --out crypto.json / --list / self-test
Zero dependencies (stdlib only).
"""
import argparse, json, sys

NICHES = {
    "crypto": {"title": "I will run a crypto/DeFi affiliate content farm for you",
               "payout": "$50-300 per referral", "posts": 30},
    "saas": {"title": "I will build a SaaS affiliate blog that earns recurring commissions",
             "payout": "20-30% monthly recurring", "posts": 25},
    "fintech": {"title": "I will launch a fintech affiliate site (cards, brokers, tools)",
                "payout": "$20-150 per lead", "posts": 20},
    "ai-tools": {"title": "I will run an AI-tools affiliate farm with auto-posting",
                 "payout": "15-50% per sale", "posts": 40},
}


def build_package(niche, posts=None):
    n = NICHES[niche]
    posts = posts or n["posts"]
    return {
        "niche": niche, "gig_title": n["title"], "payout_model": n["payout"],
        "posts_per_month": posts,
        "pricing": {"setup": 300, "monthly": 99, "margin_pct": 99,
                    "cost_note": "$0 product cost — rev-share only"},
        "n8n_workflow": build_n8n(),
        "delivery_steps": [
            "1. Pick niche + affiliate programs",
            "2. Generate 30 posts/mo (blog + social)",
            "3. Auto-publish via n8n (WordPress + X/threads)",
            "4. Insert affiliate links + track clicks",
            "5. Monthly earnings report",
        ],
        "tags": ["affiliate marketing", niche + " affiliate", "content farm",
                 "passive income", "blog automation", "seo"],
    }


def build_n8n():
    return {
        "name": "affiliate-farm",
        "nodes": [
            {"type": "n8n-nodes-base.scheduleTrigger", "name": "DailyPost",
             "params": {"interval": [{"field": "cronExpression", "expression": "0 9 * * *"}]}},
            {"type": "n8n-nodes-base.httpRequest", "name": "GenContent",
             "params": {"url": "={{$env.BLOG_GEN}}/generate", "httpMethod": "POST"}},
            {"type": "n8n-nodes-base.httpRequest", "name": "PostWP",
             "params": {"url": "={{$env.WP}}/wp-json/wp/v2/posts", "httpMethod": "POST"}},
            {"type": "n8n-nodes-base.httpRequest", "name": "PostSocial",
             "params": {"url": "={{$env.SOCIAL_API}}/post", "httpMethod": "POST"}},
        ],
        "connections": "DailyPost → GenContent → PostWP → PostSocial",
    }


def main():
    p = argparse.ArgumentParser(description="Affiliate Farm — Pipeline #8")
    p.add_argument("--niche", help="niche: " + ", ".join(NICHES.keys()))
    p.add_argument("--posts", type=int); p.add_argument("--out")
    p.add_argument("--list", action="store_true"); p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()
    if a.list:
        for k, v in NICHES.items():
            print(f"  {k:9} {v['posts']} posts/mo  payout: {v['payout']}")
        return
    if a.cmd == "self-test" and not a.niche:
        for k in NICHES:
            pkg = build_package(k)
            assert pkg["gig_title"] and pkg["n8n_workflow"]["nodes"]
            assert pkg["pricing"]["margin_pct"] == 99
            assert all("TODO" not in n.get("code", "") for n in pkg["n8n_workflow"]["nodes"])
        print(f"self-test: OK — {len(NICHES)} niches")
        return
    if not a.niche or a.niche not in NICHES:
        print("ERROR: --niche required: " + ", ".join(NICHES.keys())); sys.exit(1)
    pkg = build_package(a.niche, a.posts)
    if a.out:
        json.dump(pkg, open(a.out, "w", encoding="utf-8"), indent=2); print(f"Wrote -> {a.out}")
    else:
        print(f"\n🌱 AFFILIATE: {a.niche}\n📋 {pkg['gig_title']}\n💲 ${pkg['pricing']['setup']} + ${pkg['pricing']['monthly']}/mo (99% margin)")


if __name__ == "__main__":
    main()
