---
name: low-ram-self-protect
category: automation
description: >-
  Self-protection policy for running the Paperclip + Hermes + OpenClaw autonomy
  loop on a memory-constrained Windows host. When free physical RAM drops below
  a threshold, defer heavy work and run only a lightweight self-improve pass.
state: active
---

# Low-RAM Self-Protection (autonomy loop)

## When to use
Every autonomy tick, before doing real work, check free RAM. The Paperclip
server, OpenClaw gateway, and Hermes agent run concurrently on a ~6 GB Windows
host and free physical memory routinely oscillates between ~100 MB and ~644 MB.

## Trigger threshold
- Free RAM **< 300 MB** → lightweight pass only.
- Free RAM **>= 300 MB** → resume normal operations (no manual intervention).

## How to measure (Windows / git-bash)
```bash
wmic OS Get FreePhysicalMemory
```
The value is in **KB**. `236580` = ~231 MB. Parse and compare in KB to avoid
float rounding.

## Lightweight pass (safe under low RAM)
- Markdown edits to `knowledge-base/`, `skills/`, `tasks.md` (pure text, no model
  inference).
- Reading files, `git pull --ff-only`, `git add/commit/push` of small text diffs.
- Adding a SKILL.md or lessons-learned entry distilled from an existing log.

## Avoid under low RAM
- Paperclip build / `tsc` / npm / node operations.
- Starting heavy Python generators (`generate_v2_docs.py`, `*_generator.py`).
- Spawning model inference, deep `search_files` scans, large asset fetches.

## Recovery signal
The `wmic` check runs at the top of every tick. When RAM recovers above 300 MB
the loop automatically resumes normal work — no flag file or manual action needed.

## Why this matters
On a 6 GB host running three live services, a full build or model spawn under
< 300 MB free will thrash or OOM-kill the loop. Deferring to a cheap
self-improve pass keeps the repo advancing (docs/skills) while protecting
stability. The content funnel and product packaging work resumes safely once
memory frees up.
