---
name: agent-sentinel
version: 2.0.0
description: Scan OpenClaw/Hermes skills for risky permission patterns before installation
tags: ["security", "audit", "skill", "openclaw", "hermes", "vetting", "cli", "python", "open-source", "agent", "automation", "MIT"]
---

# Skill Security Sentinel

**Scan OpenClaw/Hermes skills for risky permission patterns before you install them.**

> *Keywords: security, audit, skill, openclaw, hermes, vetting, cli, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

A 'weather' skill can quietly request shell execution — supply-chain risk at install time. Skill Security Sentinel solves this: Scan OpenClaw/Hermes skills for risky permission patterns before you install them.

**Best for:** Anyone installing third-party ClawHub / OpenClaw / Hermes skills.

## Features

- **Vet a skill folder before install**
- **Flag over-broad permission requests**
- **Score risk OK/LOW/MEDIUM/HIGH**
- **Audit your own skills pre-publish**
- **Explain findings in plain language**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/agent-sentinel/main/agent_sentinel.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python agent_sentinel.py self-test     # prove it works end-to-end
python agent_sentinel.py scan --help   # scan subcommand
```

## Use cases

1. Vet a skill folder before install
1. Flag over-broad permission requests
1. Score risk OK/LOW/MEDIUM/HIGH
1. Audit your own skills pre-publish
1. Explain findings in plain language

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Installing blind | You see the risk before granting machine access. |
| Reading SKILL.md by hand | Patterns are detected automatically across the folder. |
| ClawHub audit only | Offline, private, repeatable anytime. |

## FAQ (SEO / AEO)

**Q: What does `scan` do?**  
A: Inspects a skill folder and flags risky permission patterns offline.

**Q: Does it upload my skill?**  
A: No. Fully local, no telemetry, no network.

**Q: What risk levels exist?**  
A: OK / LOW / MEDIUM / HIGH plus actionable findings.

**Q: Should I trust ClawHub's own audit?**  
A: Use both — sentinel is your private, offline safety net.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test agent-sentinel
        run: python agent_sentinel.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/agent-sentinel)
