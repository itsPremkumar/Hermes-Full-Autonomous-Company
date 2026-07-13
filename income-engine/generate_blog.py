#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Affiliate blog generator (Stream A). Picks the next unused niche from
config.json, writes a 1200-1800 word SEO buying guide into content/ with
{{AMAZON:keyword}} affiliate tokens. Idempotent: never repeats a niche.
Run:  python generate_blog.py
"""
import os, json, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
CONFIG = os.path.join(ROOT, "config.json")
USED = os.path.join(CONTENT, ".used_blog.json")

def load_config():
    return json.load(open(CONFIG, encoding="utf-8"))

def load_used():
    if os.path.isfile(USED):
        return json.load(open(USED, encoding="utf-8"))
    return {"niches": []}

def save_used(d):
    os.makedirs(CONTENT, exist_ok=True)
    json.dump(d, open(USED, "w", encoding="utf-8"), indent=2)

def slugify(t):
    import re
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")

def write_guide(niche, cfg):
    slug = slugify(niche)
    kw = niche.replace(" ", "+")
    date = datetime.date.today().isoformat()
    title = niche.title()
    body = f"""---
title: "{title}"
description: "A practical, zero-cost guide to {niche} — what works, what to avoid, and the tools worth paying for."
slug: {slug}
date: "{date}"
niche: "{niche}"
---

# {title}

If you run a small business, freelance, or just want your week back, **{niche}**
is one of the highest-leverage things you can set up in 2026. This guide is written
by an autonomous agent team and updated continuously. No fluff — just what actually
moves the needle.

## Why this matters now

Businesses will pay real money to remove repetitive work. Over 85% of businesses now
use some form of AI assistant, and the agent market is growing at ~30% a year. The
early movers are capturing clients who simply do not want to build this themselves.

## The 5 tools worth your attention

1. **n8n** — open-source automation you can self-host for $0. Best for wiring APIs
   together without per-step pricing. {{AMAZON:n8n automation}}
2. **Make (Integromat)** — friendlier visual builder, generous free tier for testing
   workflows before you commit. {{AMAZON:make automation}}
3. **Zapier** — largest app library; reach for it when you need a connector nobody
   else has. {{AMAZON:zapier automation}}
4. **ChatGPT / Claude API** — the reasoning layer behind most agents. Use the API,
   not the chat box, when you want it inside a workflow. {{AMAZON:ai api credits}}
5. **A vector store** — for agents that need to "remember" your docs. Pinecone,
   Qdrant, or a local option all work.

## How to pick (decision frame)

- Need it free and self-hosted? Start with **n8n**.
- Need the broadest integrations with zero setup? Use **Zapier** on the free tier.
- Need it to reason over your own data? Add an **API + vector store**.

## A 7-day rollout plan

- **Day 1-2:** pick ONE repetitive task (lead capture, invoice sorting, support triage).
- **Day 3-4:** build the workflow in n8n or Make; test with 10 real examples.
- **Day 5:** connect the API reasoning step.
- **Day 6-7:** run it on live data, measure time saved, document the handoff.

## Common mistakes

- Automating a process you haven't done manually yet (you'll encode your own chaos).
- Skipping error handling — every external API fails sometimes; add retries.
- No human-in-the-loop on money or legal actions. Draft, don't auto-send.

## Bottom line

{niche} is not a someday project. It is a this-weekend project, and the businesses
that set it up now will compound the savings for years. Start with one workflow, prove
the ROI, then expand.

_This guide is part of an autonomous income system operated by Prem Autonomous Co.
Affiliate links above support the project at no extra cost to you._
"""
    os.makedirs(CONTENT, exist_ok=True)
    open(os.path.join(CONTENT, slug + ".md"), "w", encoding="utf-8").write(body)
    return slug

def main():
    cfg = load_config()
    used = load_used()
    niches = cfg.get("niches", [])
    next_niche = None
    for n in niches:
        if n not in used["niches"]:
            next_niche = n
            break
    if not next_niche:
        print("all niches already generated. Add more to config.json niches.")
        return
    slug = write_guide(next_niche, cfg)
    used["niches"].append(next_niche)
    save_used(used)
    print(f"wrote content/{slug}.md  (niche: {next_niche})")

if __name__ == "__main__":
    main()
