# AI Agent Capability Manifest Toolkit — PRODUCT

**Product ID:** prem-agent-caps
**Title:** AI Agent Capability Manifest Toolkit (agent-caps)
**Price:** $14
**Category:** Developer Tools / AI Agents
**Tagline:** Make your AI agents swappable & safe — validate, scaffold, and cross-check agent capability manifests with zero dependencies.

## What buyers get
- `agent_caps.py` — the runnable CLI (zero dependencies, Python 3.8+)
- `test_agent_caps.py` — 12-check test suite (proof it works)
- `README.md` — usage + examples
- `examples/hermes.json`, `examples/openclaw.json` — real manifests for two popular agents
- `LICENSE` (MIT)

## Who it's for
Builders running multi-agent stacks (Hermes, OpenClaw, AutoGen, CrewAI, Paperclip):
anyone who needs agents to declare capabilities in a standard, machine-checkable way
so they can be swapped or audited without breaking the system.

## The problem it solves
Most "agent marketplaces" are docs, not enforcement. agent-caps turns the standard
interface into a validator: catch missing fields, bad versions, illegal statuses, and
unknown dependencies *before* an agent goes live.

## Quick start
```bash
python agent_caps.py scaffold ./my-agent --name MyAgent
python agent_caps.py validate ./my-agent/agent-manifest.json
```

## Compliance
MIT licensed. No tracking, no network calls, no telemetry. Runs fully offline.

> Note: this is a developer tool, not a get-rich scheme. It saves real integration
> time; it does not generate income by itself.
