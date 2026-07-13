#!/usr/bin/env python3
"""
generate_listings.py — turn every package JSON into platform-ready
Fiverr/Upwork listing copy under listings/.

Reads money/*_packs/*.json + money/gigs/*.json, emits one .md per package
with: title, 3-tier description, FAQ, tags. Zero deps (stdlib).
"""
import json
import os
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "listings")

PACK_DIRS = ["gigs", "email_packs", "video_packs", "bot_packs", "audit_packs",
             "lead_packs", "rag_packs", "affiliate_packs", "invoice_packs",
             "security_packs", "proposal_packs", "social_packs"]


def price_range(pkg):
    p = pkg.get("pricing", {})
    vals = [v for v in [p.get("price"), p.get("setup"), p.get("monthly")] if isinstance(v, (int, float))]
    if p.get("monthly") and p.get("setup"):
        return f"${p['setup']} setup + ${p['monthly']}/mo"
    if p.get("monthly"):
        return f"${p['monthly']}/mo"
    if p.get("price"):
        return f"${p['price']}/gig"
    if vals:
        return f"${min(vals)}–${max(vals)}"
    return "contact for quote"


def render(pkg, fname):
    title = pkg.get("gig_title") or pkg.get("title") or fname
    tags = ", ".join(pkg.get("tags", [])[:8])
    steps = "\n".join(f"- {s}" for s in pkg.get("delivery_steps", []))
    margin = pkg.get("pricing", {}).get("margin_pct", "—")
    wp = json.dumps(pkg.get("n8n_workflow") or pkg.get("render_manifest") or {}, indent=1)
    return f"""# {title}

**Price:** {price_range(pkg)}
**Margin:** {margin}%
**Tags:** {tags}

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
{steps}

## Why this works
- Self-hosted stack (n8n + free tools) → 90–99% profit margin
- Every deliverable is generated and delivered automatically
- You own the system; scale to unlimited clients

## FAQ
**Q: Do I need to pay for software?**
A: No. Everything runs on free open-source tools (n8n, Chatwoot, Stirling-PDF, Listmonk).

**Q: Is this a one-time build or ongoing?**
A: Both. One-time setup + optional monthly retainer for monitoring/optimization.

**Q: Can you customize for my niche?**
A: Yes — every package is generated from a template and tuned to your vertical.

## Technical spec (for the build)
```json
{wp}
```
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    count = 0
    for d in PACK_DIRS:
        base = os.path.join(HERE, d)
        if not os.path.isdir(base):
            continue
        for f in sorted(glob.glob(os.path.join(base, "*.json"))):
            pkg = json.load(open(f, encoding="utf-8"))
            name = os.path.splitext(os.path.basename(f))[0]
            sub = os.path.join(OUT, d)
            os.makedirs(sub, exist_ok=True)
            out = os.path.join(sub, f"{name}.md")
            open(out, "w", encoding="utf-8").write(render(pkg, name))
            count += 1
    print(f"Generated {count} listings under {OUT}")


if __name__ == "__main__":
    main()
