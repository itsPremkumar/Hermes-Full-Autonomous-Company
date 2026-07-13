---
name: agent-sentinel
version: 1.0.0
description: Scan OpenClaw/Hermes skills for risky permission patterns before you install them. Stdlib-only, offline.
tags: [security, audit, skill, openclaw, hermes, vetting]
---

# agent-sentinel — vet a skill before you trust it

The #1 OpenClaw risk is installing a third-party skill that asks for more access than it
needs (e.g. a "weather" skill requesting shell execution). agent-sentinel scans a skill
folder and flags exactly that — before you give it machine access.

## Install
No dependencies. Python 3.8+. Copy `agent_sentinel.py` anywhere.

## Usage
```bash
python agent_sentinel.py scan <skill-folder> [--json]   # risk report
python agent_sentinel.py self-test                      # built-in test
```

## What it checks
- Simple-named skill (weather/hello/joke) requesting shell/exec → **HIGH**
- Shell/exec capability requested at all → **MEDIUM**
- Possible hardcoded secret (api_key/token) in skill files → **HIGH**
- No human approval gate for privileged actions → **LOW**
- Network egress without stated reason

Returns a risk level (OK / LOW / MEDIUM / HIGH) + actionable findings.

## Why
ClawHub's own docs tell you to "vet every skill before installing" and check its
security report. agent-sentinel is the local, private, offline version you can run
yourself — no upload, no telemetry.

## Support this work
This is free and MIT licensed. If it saves you from a bad skill, sponsor the builder:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar  *(add your link)*
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar      *(add your link)*
A premium "batch-scan + CI gate" bundle is on Gumroad.
