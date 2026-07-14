# 🤖 Autonomous AI Agent Operations Playbook — Run a Whole Company on Agents

*The exact playbook we use to run Prem Autonomous Co — a real business where AI agents do the actual work (not just chat). Zero headcount, zero burn. Handed to you as a complete operations manual plus four ready-to-fill templates so you can stand up your own agent-run company this week.*

---

## 🧭 What This Is

A complete, battle-tested operations playbook for running a business using autonomous AI agents. We wrote this while building Prem Autonomous Co on the **Paperclip + Hermes + OpenClaw** stack — a zero-budget autonomous company. It covers architecture, tooling, workflow automation, revenue ops, and scaling.

---

## 📚 The 5 Chapters

### Chapter 1 — Agent Architecture
- How to structure agent roles (CTO, Engineer, CMO, Operator, Sentinel…).
- Agent-to-agent communication protocols.
- Task assignment and dependency management.
- Heartbeat loops and autonomous operation cycles (the tick that keeps the company alive).

### Chapter 2 — Tooling Stack
- Paperclip platform setup (issue pipeline + artifacts).
- OpenRouter free-tier configuration.
- Hermes adapter integration.
- Cost monitoring — the **$0 burn** configuration that keeps the lights on at zero budget.

### Chapter 3 — Workflow Automation
- Issue pipeline: `todo → in_progress → review → done`.
- Automatic artifact generation.
- API-based work-product management.
- Continuous development loops (the autonomy tick).

### Chapter 4 — Revenue Operations
- Service catalog design.
- Zero-investment pricing strategies (tiered, quota-bounded offers).
- Automated delivery pipelines.
- Customer onboarding workflows.

### Chapter 5 — Scaling
- Multi-agent orchestration.
- Queue management at volume.
- Quality-control automation.
- Growth loops that compound without headcount.

---

## 🎁 Bonus — 4 Ready-to-Use Templates (shipped in this folder)

| File | What it does |
|------|--------------|
| `AGENTS.md` | Drop-in agent instructions file — roles, heartbeat protocol, safety guards. |
| `.env.example` | Environment config template (no secrets — placeholders only). |
| `issue-template.json` | Standardized issue format for the pipeline. |
| `heartbeat-config.yaml` | Autonomous loop configuration — cadence, RAM guard, fail-safe. |

Copy these into your repo, swap the placeholders, and your agents inherit the same operating system we run in production.

---

## 🛡️ Guardrails We Learned the Hard Way

- **Bounded quotas over "unlimited."** Every offer and every agent task needs a hard cap. Unlimited is how you get abused.
- **Heartbeat must be idempotent.** A tick that re-runs safely after a crash is worth more than a clever one that doesn't.
- **$0 burn is a discipline, not a luck.** Free-tier models + cached creds + lightweight ticks. Measure RAM every tick (see `heartbeat-config.yaml`).
- **Never commit secrets.** Scan `.env`, OpenRouter keys, and credentials before every push. The `.env.example` ships empty by design.
- **Human-gated money stays human-gated.** The loop packages and drafts; a real person approves publish, payouts, and spend.

---

> Built from the live operations of Prem Autonomous Co. Marginal cost to deliver: zero — it's a file. Charge for the *operating system*, not the production.

*Free version of the chapter outline lives on GitHub. This pack is the filled-in, template-equipped operator kit — same system, cleaned up and ready to deploy.*
