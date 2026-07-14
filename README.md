# Hermes-Full-Autonomous-Company

**Single source of truth** for the autonomous AI company run by Paperclip + Hermes Agent + OpenClaw on a zero-cash budget.

> Mission: from zero investment, build and operate a small, real, sustainable business using free/open-source tooling, disciplined automation, and continuous learning. No guarantees of passive income — revenue comes from solving real problems people pay for.

## What this repo contains

| Path | Purpose |
|---|---|
| `CONSTITUTION.md` | **Master operating prompt v2.0** — the supreme manual. Also the Hermes `SOUL.md`. |
| `agents/` | Agent configs: `hermes/SOUL.md`, plus `openclaw/`, `coding-agents/` |
| `skills/` | Hermes' reviewed `SKILL.md` files (proven reusable patterns) |
| `prompts/` | Prompt library (versioned). `executive-master-operating-prompt-v2.0.md` is current; `archive/` holds superseded drafts |
| `tools/` | `approved.md` (validated tools + how to run) · `rejected.md` (tried & dropped, with reason) |
| `knowledge-base/` | `lessons-learned.md` · `benchmarks.md` |
| `business/` | `marketing/` `finance/` `product/` `customer-support/` |
| `infra/` | deployment, security, monitoring notes · **`openclaw-control-guide.md`** (how to run/command OpenClaw — the chat/phone front-door) |
| `products/` | the actual digital products |
| `income-engine/` | zero-cost asset generator + publish scripts |
| `finance/` | `revenue-ledger.csv`, `burn-guard.py`, `burn-policy.json` |
| `digital-products/` | 8 ready-to-list products (Video Scripts, Agent Playbook, Remotion Pack, Monetization Kit, Cold Outreach, Job-Board Guide, Pricing Templates, 30-Day Launch Plan) |
| `hermes-paperclip-adapter/` | the CEO↔Paperclip bridge (source only; `node_modules` excluded) |
| `COMPANY_PLAN.md` | living master plan |
| `company-status.json` | last-known Paperclip status snapshot |
| `changelog.md` | full version history |

## Operating rules (summary)

1. **GitHub is the source of truth.** If it isn't committed, it isn't done.
2. **Money has a human in the loop.** Budget caps + approval gates are non-negotiable (see `CONSTITUTION.md` §0).
3. **Free & open-source first.** Validate an existing OSS solution before building.
4. **Memory-discipline on this low-RAM machine.** Close tools after use; never leave idle heavy processes.
5. **Self-improvement = better skills/docs, not unsupervised self-editing** of the Charter.

## Stack (verified, running)

- **Paperclip** — org chart, budgets, governance, ticketing (7 agents: CEO, CFO, COO, CMO, Head of Product, QA, Engineer)
- **Hermes Agent** — executive/growth (local model default; OmniRoute→OpenRouter for escalation)
- **OpenClaw** — comms + computer-use · see `infra/openclaw-control-guide.md` for full control/usage docs |
- **hermes-paperclip-adapter** — bridges Hermes into Paperclip
- **Automated-Video-Generator** — Remotion product line

## Getting started

```bash
git clone https://github.com/itsPremkumar/Hermes-Full-Autonomous-Company.git
# Read CONSTITUTION.md first — it is the operating manual.
# The live company runs via Paperclip on localhost:3100 (see ~/.paperclip).
```

See `CONSTITUTION.md` for the full architecture, policies, and the End-Goal Loop template used per project.

