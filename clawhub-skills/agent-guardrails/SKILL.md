---
name: agent-guardrails
version: 2.0.0
description: Enforce safety guardrails on agent actions: permission gates, allowlists, audit
tags: ["guardrails", "safety", "agent", "cli", "security", "policy", "python", "open-source", "automation", "MIT"]
---

# Agent Action Guardrails

**Pre-flight safety gate for planned agent actions: permission checks, allowlists, and an audit trail.**

> *Keywords: guardrails, safety, agent, cli, security, policy, python, open-source, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Agents take irreversible actions (shell, deletes, network) with no pre-flight safety check. Agent Action Guardrails solves this: Pre-flight safety gate for planned agent actions: permission checks, allowlists, and an audit trail.

**Best for:** Agent platform teams and security reviewers who must approve or deny planned agent actions.

## Features

- **Gate a planned action before execution**
- **Maintain an allowlist of permitted commands**
- **Deny high-risk patterns (rm -rf, sudo)**
- **Produce an audit record of every decision**
- **Score risk before the agent acts**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/agent-guardrails/main/agent_guardrails.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python agent_guardrails.py self-test     # prove it works end-to-end
python agent_guardrails.py check --help   # check subcommand
```

## Use cases

1. Gate a planned action before execution
1. Maintain an allowlist of permitted commands
1. Deny high-risk patterns (rm -rf, sudo)
1. Produce an audit record of every decision
1. Score risk before the agent acts

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Trusting the prompt | guardrails evaluates the action, not the intent. |
| Post-hoc review | It blocks before execution, not after damage. |
| Manual code review | Policy-as-code makes safety repeatable across agents. |

## FAQ (SEO / AEO)

**Q: What does `check` do?**  
A: Evaluates a planned action against policy and returns allowed/denied + reason.

**Q: Is it offline?**  
A: Yes. Pure stdlib, no network, no telemetry.

**Q: How do allowlists work?**  
A: Define permitted command patterns; anything outside is denied by default.

**Q: Does it log decisions?**  
A: Yes — every decision emits a structured audit entry.

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
      - name: Self-test agent-guardrails
        run: python agent_guardrails.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/agent-guardrails)
