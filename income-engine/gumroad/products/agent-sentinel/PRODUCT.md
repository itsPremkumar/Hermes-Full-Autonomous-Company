# Agent Sentinel — Security Audit Toolkit for AI Skills — PRODUCT

**Product ID:** prem-agent-sentinel
**Title:** Agent Sentinel — Security Audit Toolkit for AI Skills
**Price:** $14
**Category:** Developer Tools / Security
**Tagline:** Vet any OpenClaw/Hermes skill for risky permissions before you install it. Batch-scan, CI-gate, zero dependencies.

## What buyers get (premium bundle)
- `agent_sentinel.py` — the CLI scanner (Python 3.8+, stdlib-only, offline)
- `batch_scan.py` — bulk-scan an entire skills directory in one command
- `ci_gate.sh` — CI pipeline script that exits 1 on HIGH-risk findings
- `sample_skills/` — 5 test skill folders (safe, medium, rogue) to learn the scanner
- `report_template.json` — structured JSON output format for CI consumption
- `LICENSE` (MIT)

## Who it's for
Anyone running OpenClaw, Hermes, or any agent runtime where third-party skills
can request capabilities (shell, exec, network, file access):
- Solo builders installing community skills
- Teams curating an internal skill registry
- CI pipelines that gate deployments on security audit pass

## The problem it solves
ClawHub's own docs tell you to "vet every skill before installing" and check its
security report. But there's no local tool for it — until now. Agent Sentinel is
the offline, private, zero-trust scanner you run yourself: no upload, no telemetry.

## Quick start
```bash
pip install .                     # or just copy agent_sentinel.py
python agent_sentinel.py scan ./some-skill
python agent_sentinel.py scan-all ./skills/ --json > report.json
python agent_sentinel.py ci-check ./skills/  # exit code 1 on HIGH
```

## What it flags

| Risk Level | Pattern | Example |
|-----------|---------|---------|
| HIGH | Simple-named skill requesting shell/exec | `weather/exec/*`, `hello/shell:rw` |
| MEDIUM | Any shell/exec capability requested | `image-gen/exec/*` |
| HIGH | Hardcoded secrets in skill files | `api_key = "sk-..."` in plaintext |
| LOW | No human approval gate for privileged actions | Skill auto-grants `shell:rw` |
| LOW | Network egress without stated reason | `network:connect` with no comment |

## Compliance
MIT licensed. No tracking, no network calls, no telemetry. Runs fully offline.
Free core version available on ClawHub: clawhub.ai/skills/skills/agent-sentinel
