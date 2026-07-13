---
name: company-ops
version: 1.0.0
description: Run a self-improving autonomous company OS from a single CONSTITUTION + confidence-gated autonomy loop. Zero cash.
tags: [autonomous, company, ops, openclaw, hermes, agent]
---

# company-ops — operate an autonomous AI company

A working operating system for running a 7-agent company on a $0 budget: a CONSTITUTION
(behavioral spec), an autonomy loop with confidence gates (only act above threshold,
escalate below), and a failure taxonomy. Built and proven in production.

## Install
Copy `CONSTITUTION.md` into your agent workspace as SOUL/behavior spec.
Run `autonomy-loop.py` on a schedule (cron every 30m) — it builds, tests, commits,
and pushes, but only ships work that clears the confidence gate.

## What it enforces
- Human-in-the-loop for money/privacy/legal (never auto-publishes payouts)
- Confidence gate: PROCEED >= 75, ESCALATE < 50
- Every rule is a scar from a real failure (failure-taxonomy baked in)

## Why
Most "agent company" repos are pitches. This is the running OS. Free + MIT. A setup-as-
a-service tier is available on Gumroad for those who want it configured.

## Support this work
Free + MIT. Sponsor the builder if it helps:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar  *(add your link)*
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar      *(add your link)*
