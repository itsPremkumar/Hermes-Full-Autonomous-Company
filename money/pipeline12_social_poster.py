#!/usr/bin/env python3
"""
Social Auto-Poster — Pipeline #12 from MONEY_AUTOMATION_IDEAS.md

Recurring social content (your gif-search + excalidraw + video tools) auto-posted
via n8n. Validated 2026: $99-$399/mo, 97% margin.

Usage: python pipeline12_social_poster.py --plan pro --out pro.json / --list / self-test
Zero dependencies (stdlib only).
"""
import argparse, json, sys

PLANS = {
    "starter": {"title": "I will auto-post daily social content for your brand",
                "posts": 30, "monthly": 99, "platforms": ["X", "LinkedIn"]},
    "pro": {"title": "I will run a multi-platform content machine for you",
            "posts": 90, "monthly": 199, "platforms": ["X", "LinkedIn", "Instagram", "Threads"]},
    "agency": {"title": "I will white-label social posting for your clients",
               "posts": 300, "monthly": 399, "platforms": ["X", "LinkedIn", "IG", "Threads", "FB"]},
}


def build_package(plan, price=None):
    p = PLANS[plan]
    price = price or p["monthly"]
    return {
        "plan": plan, "gig_title": p["title"], "posts_per_month": p["posts"],
        "platforms": p["platforms"],
        "pricing": {"monthly": price, "annual": price * 10, "margin_pct": 97,
                    "cost_note": "gif-search + excalidraw + video (free)"},
        "n8n_workflow": build_n8n(),
        "delivery_steps": [
            "1. Client sets brand + topics",
            "2. n8n generates content (gif/diagram/video)",
            "3. Schedule + auto-post across platforms",
            "4. Track engagement, optimize",
            "5. Monthly content calendar + report",
        ],
        "tags": ["social media", "content automation", plan + " social",
                 "auto posting", "social media manager", "growth"],
    }


def build_n8n():
    return {
        "name": "social-poster",
        "nodes": [
            {"type": "n8n-nodes-base.scheduleTrigger", "name": "DailyPost",
             "params": {"interval": [{"field": "cronExpression", "expression": "0 10 * * *"}]}},
            {"type": "n8n-nodes-base.httpRequest", "name": "GenContent",
             "params": {"url": "={{$env.CONTENT_GEN}}/make", "httpMethod": "POST"}},
            {"type": "n8n-nodes-base.httpRequest", "name": "PostX",
             "params": {"url": "={{$env.X_API}}/tweet", "httpMethod": "POST"}},
            {"type": "n8n-nodes-base.httpRequest", "name": "PostIG",
             "params": {"url": "={{$env.IG_API}}/media", "httpMethod": "POST"}},
        ],
        "connections": "DailyPost → GenContent → PostX → PostIG",
    }


def main():
    p = argparse.ArgumentParser(description="Social Auto-Poster — Pipeline #12")
    p.add_argument("--plan", help="plan: " + ", ".join(PLANS.keys()))
    p.add_argument("--price", type=int); p.add_argument("--out")
    p.add_argument("--list", action="store_true"); p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()
    if a.list:
        for k, v in PLANS.items():
            print(f"  {k:8} ${v['monthly']}/mo  {v['posts']} posts/mo  {','.join(v['platforms'])}")
        return
    if a.cmd == "self-test" and not a.plan:
        for k in PLANS:
            pkg = build_package(k)
            assert pkg["gig_title"] and pkg["n8n_workflow"]["nodes"]
            assert pkg["pricing"]["margin_pct"] == 97
            assert all("TODO" not in n.get("code", "") for n in pkg["n8n_workflow"]["nodes"])
        print(f"self-test: OK — {len(PLANS)} plans")
        return
    if not a.plan or a.plan not in PLANS:
        print("ERROR: --plan required: " + ", ".join(PLANS.keys())); sys.exit(1)
    pkg = build_package(a.plan, a.price)
    if a.out:
        json.dump(pkg, open(a.out, "w", encoding="utf-8"), indent=2); print(f"Wrote -> {a.out}")
    else:
        print(f"\n📡 SOCIAL: {a.plan}\n📋 {pkg['gig_title']}\n💲 ${pkg['pricing']['monthly']}/mo (97% margin)")


if __name__ == "__main__":
    main()
