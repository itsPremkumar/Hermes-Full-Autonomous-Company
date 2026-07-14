#!/usr/bin/env python3
"""
AI UGC / Ad-Creative Factory — Pipeline #17 (from research/MONEY_IDEAS_2026.md, rank #2 NEW)

Generates ready-to-sell AI UGC & ad-creative service packages (title, description,
3 tiers, SEO tags) + an importable n8n workflow JSON for delivery automation.

Validated 2026 market data (see research/MONEY_IDEAS_2026.md for full citations):
  - AI video generation gig on Fiverr: $25-$1,500 (memvers, Jul 2026)
  - AI UGC / avatar ads sub-tier: $100-$500 for 1-3min branded + avatar
  - UGC ad spend is the fastest-growing paid-social format (creator-economy demand)
  - Free stack: Remotion + Edge-TTS + CogVideoX + InfernoFX (ComfyUI nodes) + Flowise
    (local orchestration) — all OSS / self-hosted. No paid Runway/Kling subscription.

Usage:
  python pipeline17_ugc_ad_factory.py --service "ugc-avatar" --price 300
  python pipeline17_ugc_ad_factory.py --list
  python pipeline17_ugc_ad_factory.py --service product-ad --out ugc.json
  python pipeline17_ugc_ad_factory.py self-test
Zero dependencies (stdlib only).
"""
import argparse
import json
import sys

# ---- Validated 2026 pricing/demand data ----
SERVICES = {
    "ugc-avatar": {
        "title": "I will generate AI UGC avatar ad videos (no actors, no studio)",
        "outcome": "scroll-stopping 15-60s UGC-style ad videos with a consistent AI spokesperson, in any niche",
        "tools": "Remotion + Edge-TTS + CogVideoX + Flowise (local) — all free/self-hosted",
        "margin_note": "Charge $100-$500/video; your cost $0 (self-hosted GPU or free tier)",
        "tags": ["ugc ads", "ai video", "facebook ads", "tiktok ads", "ai avatar",
                 "remotion", "cogvideox", "ad creative"],
        "default_price": 300,
    },
    "product-ad": {
        "title": "I will make AI product.demo ad videos for ecommerce brands",
        "outcome": "a batch of 5-20 product showcase/ad variations from your product URL or images",
        "tools": "Remotion + CogVideoX + InfernoFX (ComfyUI) + n8n — all free/self-hosted",
        "margin_note": "Charge $250-$1,000/batch; 20 variations vs 1 film shoot",
        "tags": ["product video", "ai ads", "ecommerce", "ad creative", "cogvideox",
                 "remotion", "video generation", "dropshipping"],
        "default_price": 500,
    },
    "translation-ads": {
        "title": "I will localize your ad videos into 10 languages with AI dubbing",
        "outcome": "one ad video adapted to 10 languages with AI voice dub + subtitles",
        "tools": "Edge-TTS + Whisper + LibreTranslate + Remotion — all free/self-hosted",
        "margin_note": "Charge $150-$600/video; multilingual reach at $0 marginal cost",
        "tags": ["video translation", "ai dubbing", "multilingual ads", "libretranslate",
                 "edge tts", "whisper", "localization", "ad creative"],
        "default_price": 250,
    },
    "faceless-youtube": {
        "title": "I will produce faceless YouTube/TikTok automation videos",
        "outcome": "a packaged faceless video (script + voice + visuals) you can post daily",
        "tools": "Edge-TTS + Remotion + your youtube-content skill — all free/self-hosted",
        "margin_note": "Charge $50-$300/video; recurring content-retainer model",
        "tags": ["faceless youtube", "tiktok automation", "ai video", "edge tts",
                 "remotion", "content creator", "passive income", "shorts"],
        "default_price": 120,
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
• Free, open-source tools (you own it, no SaaS lock-in)
• {s['margin_note']}
• 7-day support after delivery

📦 Packages:
{bullet_tiers(tiers)}

🚀 How it works:
1. You send product URL / script / brand kit
2. I generate & test the video creatives
3. I hand over + a 5-min Loom walkthrough

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
         "features": ["1 video", "1 workflow", "Email support"]},
        {"name": "Standard", "price": price,
         "delivery": "5 days", "revisions": 2,
         "features": ["Up to 5 videos", "Setup + test", "Loom walkthrough", "7-day support"]},
        {"name": "Premium", "price": price * 2,
         "delivery": "7 days", "revisions": 3,
         "features": ["Unlimited videos", "Full system", "Monthly retainer option", "Priority support"]},
    ]


def bullet_tiers(tiers):
    out = []
    for t in tiers:
        out.append(f"• {t['name']} (${t['price']}, {t['delivery']}, {t['revisions']} rev): "
                   + ", ".join(t["features"]))
    return "\n".join(out)


def build_n8n_workflow(service_key, s):
    return {
        "name": f"deliver-ugc-{service_key}",
        "nodes": [
            {"parameters": {}, "name": "Webhook (intake)",
             "type": "n8n-nodes-base.webhook", "typeVersion": 1, "position": [0, 0]},
            {"parameters": {}, "name": "Render video (Remotion/CogVideoX)",
             "type": "n8n-nodes-base.code", "typeVersion": 1, "position": [300, 0]},
            {"parameters": {}, "name": "Deliver + notify",
             "type": "n8n-nodes-base.emailSend", "typeVersion": 1, "position": [600, 0]},
        ],
        "connections": {
            "Webhook (intake)": {"main": [[{"node": "Render video (Remotion/CogVideoX)", "type": "main", "index": 0}]]},
            "Render video (Remotion/CogVideoX)": {"main": [[{"node": "Deliver + notify", "type": "main", "index": 0}]]},
        },
        "note": f"Tools: {s['tools']}. Replace code node with your render logic.",
    }


def main():
    p = argparse.ArgumentParser(description="AI UGC / Ad-Creative Factory — Pipeline #17")
    p.add_argument("--service", help="service key: " + ", ".join(SERVICES.keys()))
    p.add_argument("--price", type=int, help="override price")
    p.add_argument("--out", help="write package JSON to file")
    p.add_argument("--list", action="store_true", help="list services")
    p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()

    if a.list:
        for k, v in SERVICES.items():
            print(f"  {k:18} {v['default_price']:>5}/gig  {v['title'][:42]}")
        return

    if a.cmd == "self-test" and not a.service:
        for k in SERVICES:
            pkg = build_package(k)
            assert pkg["package_title"] and pkg["description"] and len(pkg["packages"]) == 3
            assert pkg["n8n_workflow"]["name"].startswith("deliver-ugc-")
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
