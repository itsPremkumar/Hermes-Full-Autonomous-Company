# agent-caps — Agent Capability Manifest Toolkit

A **zero-dependency** command-line tool that lets AI agents (Hermes, OpenClaw,
Paperclip-style) declare, validate, and cross-check their capabilities as
machine-readable manifests — so agents can be **swapped safely** without breaking the OS.

This is the runnable implementation of the *Agent Marketplace* standard interface
defined in `agents/registry.md` (Name / Version / Capabilities / Dependencies /
Memory / Tools / API / Status).

## Why this exists
The reviewer's "agent marketplace" point is correct: every agent should follow a
standard interface so it can be replaced. But a standard only matters if something
**enforces** it. `agent-caps` is that enforcement — pure Python stdlib, no install,
runs on a low-RAM laptop.

## Install
No dependencies. Copy `agent_caps.py` anywhere or `pip install` (optional).
Requires Python 3.8+.

```bash
python agent_caps.py --help
```

## Commands
```bash
# Validate a manifest against the schema
python agent_caps.py validate path/to/agent-manifest.json

# Generate a manifest scaffold from a project directory
python agent_caps.py scaffold ./my-agent --name MyAgent

# Cross-check dependencies across multiple agents
python agent_caps.py check-deps hermes.json openclaw.json

# Print the JSON schema (for other tooling / agents)
python agent_caps.py schema
```

## Exit codes
- `0` OK
- `1` validation error (or dependency warning)
- `2` usage / file error

## Example manifest
```json
{
  "name": "Hermes",
  "version": "1.0",
  "capabilities": ["executive reasoning", "planning", "documentation"],
  "dependencies": ["Paperclip API", "git CLI"],
  "memory_requirements": "256MB",
  "tools": ["terminal", "file", "browser"],
  "api": "hermes_local / hermes_gateway",
  "status": "active"
}
```

## Tests
```bash
python test_agent_caps.py   # 12 stdlib-only checks, all must pass
```

## License
MIT — part of Hermes-Full-Autonomous-Company.
