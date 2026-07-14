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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "listings")

# Single source of truth: derive every pack directory from run_all.PIPELINES
# so listings always match the live pipeline set (no drift when pipelines
# are added/renamed). Falls back to an explicit list if run_all can't import.
FALLBACK_DIRS = ["gigs", "email_packs", "video_packs", "bot_packs", "audit_packs",
                 "lead_packs", "rag_packs", "affiliate_packs", "invoice_packs",
                 "security_packs", "proposal_packs", "social_packs",
                 "voice_packs", "doc_packs", "retainer_packs"]

def resolve_pack_dirs():
    prev = sys.path[:]
    sys.path.insert(0, HERE)
    try:
        import run_all  # noqa: E402
        dirs = [pl["outdir"] for pl in run_all.PIPELINES]
        # de-dup, preserve order
        seen, ordered = set(), []
        for d in dirs:
            if d not in seen:
                seen.add(d)
                ordered.append(d)
        return ordered
    except Exception:
        return list(FALLBACK_DIRS)
    finally:
        sys.path[:] = prev

PACK_DIRS = resolve_pack_dirs()


def price_range(pkg):
    p = pkg.get("pricing", {})
    # Flat-shape packages carry a top-level "price" (e.g. voice/doc/retainer packs)
    flat = pkg.get("price")
    if isinstance(flat, (int, float)):
        return f"${flat}/gig"
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


def _title(pkg, fname):
    return pkg.get("package_title") or pkg.get("gig_title") or pkg.get("title") or fname


def _delivery_steps(pkg):
    # New shape: explicit delivery_steps list
    if pkg.get("delivery_steps"):
        return [f"- {s}" for s in pkg["delivery_steps"]]
    # Older/other shape: derive from the `packages` tier list
    pkgs = pkg.get("packages") or []
    if pkgs:
        out = []
        for pk in pkgs:
            feats = pk.get("features") or []
            line = f"- **{pk.get('name', 'Package')}** (${pk.get('price', '?')}"
            if pk.get("delivery"):
                line += f", {pk['delivery']}"
            line += "): " + "; ".join(feats) if feats else ")"
            out.append(line)
        return out
    return ["- Configured, tested, and handed over with a walkthrough."]


def _margin(pkg):
    m = pkg.get("margin_pct") or pkg.get("pricing", {}).get("margin_pct", "—")
    return m


def render(pkg, fname):
    title = _title(pkg, fname)
    tags = ", ".join(pkg.get("tags", [])[:8])
    steps = "\n".join(_delivery_steps(pkg))
    margin = _margin(pkg)
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
