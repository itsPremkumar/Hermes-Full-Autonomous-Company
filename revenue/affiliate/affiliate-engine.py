#!/usr/bin/env python3
"""
affiliate-engine.py — generates SEO/affiliate blog drafts (agent-safe, $0).

Pipeline (all automatable except affiliate-program APPLICATION + link disclosure,
which are human steps per Charter S0.3/0.4):
  1. Pick a topic from topics.json
  2. Generate a Markdown article draft (template-based, no external API needed)
  3. Append the mandatory affiliate disclosure
  4. Write to revenue/affiliate/drafts/<slug>.md

The agent then commits + pushes (GitHub = source of truth). The human later:
  - applies to the affiliate programs listed in topics.json
  - inserts their OWN affiliate IDs into the {{AFF_ID}} placeholders
  - publishes to the blog platform of choice

No secrets, no network calls, no money movement. Runs on stdlib only.
"""
import json
import os
import re
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
TOPICS = os.path.join(HERE, "topics.json")
DRAFTS = os.path.join(HERE, "drafts")
REPO = os.path.dirname(os.path.dirname(HERE))  # revenue/ -> repo root

DISCLAIMER = (
    "\n---\n"
    "**Disclosure:** This article may contain affiliate links. If you buy through them, "
    "we may earn a commission — at no extra cost to you. We only recommend tools we have "
    "personally verified (see tools/approved.md). This is not financial advice.\n"
)

def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60]

def load_topics():
    if not os.path.isfile(TOPICS):
        return []
    with open(TOPICS, encoding="utf-8") as f:
        return json.load(f)

def draft_for(topic):
    name = topic.get("product", "the tool")
    problem = topic.get("problem", "a common workflow bottleneck")
    audience = topic.get("audience", "builders and small teams")
    return f"""# {topic['title']}

*Category: {topic.get('category', 'AI Tools')} · Target keyword: {topic.get('keyword', topic['title'])}*

## Why this matters
{audience} hit a real wall with {problem}. The usual fixes are slow, manual, or
overpriced. This guide covers a lean, $0-friendly approach using verified tools.

## The approach
1. Identify the exact bottleneck (don't automate what isn't measured).
2. Pick a tool that fits the constraint — for us, that means zero-cost and low-RAM.
3. Wire it into a repeatable workflow so it runs without daily babysitting.

## Tool we verified: {name}
We use {name} because it is open about what it does, runs without a heavy stack,
and solves the specific problem above. (Full write-up: our product line on Gumroad.)

**Get {name}:** [{{AFF_ID:{name}}}] — *insert your affiliate/store link here.*

## Caveat
No tool manufactures revenue. {name} saves time on a real task; the return depends
on whether that task was worth doing in the first place. We avoid any "passive income
guarantee" framing — it is a red flag (Charter S0.3).

## Related
- Our Autonomous Company OS (GitHub, MIT)
- Agent capability toolkit (product #9)
"""

def main():
    topics = load_topics()
    if not topics:
        print("No topics.json found — create one with a list of topic objects.")
        return 1
    os.makedirs(DRAFTS, exist_ok=True)
    # generate the next unpublished topic (skip existing drafts)
    existing = {f[:-3] for f in os.listdir(DRAFTS) if f.endswith(".md")}
    made = 0
    for t in topics:
        sl = slugify(t["title"])
        if sl in existing:
            continue
        body = draft_for(t) + DISCLAIMER
        out = os.path.join(DRAFTS, sl + ".md")
        with open(out, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"draft written: {out}")
        made += 1
        break  # one per run; the loop schedules many
    if made == 0:
        print("All topics drafted. Add more to topics.json to continue.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
