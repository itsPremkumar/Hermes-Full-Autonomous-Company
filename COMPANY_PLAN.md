# PREM AUTONOMOUS CO — MASTER COMPANY PLAN

> Zero-investment, fully-autonomous AI-agent company. Self-hosted on Windows, free LLM tier,
> local Postgres. Revenue model: sell autonomous agent-labor + the open-source product it builds.

_This file is the LIVING master plan. It is the authoritative source for strategy, org, and
roadmap state. Agents update it on each heartbeat when state changes; the board reviews it via
the linked work product on issue [PRE-13](/PRE/issues/PRE-13). Last updated: 2026-07-12 ·
Owner: Premkumar M · Model: tencent/hy3:free (OpenRouter free tier)_

---

## 0. Living-plan governance
- **Authoritative source:** this file (`C:/one/paperclip-company/COMPANY_PLAN.md`).
- **Living issue:** [PRE-13](/PRE/issues/PRE-13) — any change to strategy/roadmap/org is
  proposed here and recorded in this file by the responsible agent.
- **Update cadence:** agents refresh their epic's status row whenever an issue moves
  (in_progress → done, blocker, etc.); the "Last updated" line and section 6 snapshot are
  kept current. Watchdog's `company-report.md` is a derived mirror, not the source of truth.
- **Board visibility:** the authoritative plan is published directly on its owner issue
  [PRE-13](/PRE/issues/PRE-13) as an artifact work product (attachment-backed, `text/markdown`) so reviewers
  without workspace access can read it. PRE-13 (assignee: Hermes CEO) is the only authorized publisher of its own
  reviewable mirror, because the publishing agent must be the issue's assignee — a prior CFO attempt hit 403s for
  this reason. The workspace file (`C:/one/paperclip-company/COMPANY_PLAN.md`) stays canonical; the artifact is a
  derived board-visible copy. Duplicate publish follow-ups (PRE-44, PRE-47, PRE-48) were consolidated into this
  PRE-13 publish.
- **Disposition rule:** this plan is never "done"; it evolves. PRE-13 is left open as the
  long-lived owner of the plan.

## 1. Mission
Build and operate a self-running company that (a) ships the **Automated-Video-Generator (AVG)**
open-source product and (b) sells autonomous agent-labor services, with **no upfront capital**.
The agents do the work; the human steers strategy and owns the accounts.

## 2. Operating principles (zero-investment constraints)
- **No paid APIs for the company's own operation.** Product fulfillment uses AVG's free pipeline
  (Remotion + Edge-TTS + Pexels/Pixabay/Openverse CC media). Agent reasoning uses OpenRouter free tier.
- **Free-only GTM channels:** Naukri, LinkedIn, Wellfound, RemoteAI, YC Work at a Startup, GitHub,
  dev.to, Product Hunt (organic). No ad spend, ever.
- **Every run is inspectable.** Agents record work products + dispositions; watchdog logs health.
- **Human-in-the-loop only where legally/financially required:** publishing pages, sending outreach
  from personal accounts, binding contracts, payments. Agents draft; human ships.

## 3. Organization (C-suite)
| Agent | Role | Mandate | Reports to |
|-------|------|---------|------------|
| Hermes CEO | ceo | Strategy, roadmap, cross-agent coordination, fundraising-readiness | (owner) |
| Hermes CTO | cto | Product engineering of AVG, infra, code quality | CEO |
| Hermes CMO | cmo | Brand, GTM, pricing, outreach drafts, content | CEO |
| Hermes COO | coo | Delivery ops, SLA, client workflows, process | CEO |
| Hermes CFO | cfo | Unit economics, pricing guardrails, revenue tracking, burn=$0 watch | CEO |
| Hermes Head of Product | product | Roadmap execution, specs, user feedback loop | CTO |
| Hermes QA | qa | Test plans, release gates, regression checks | CTO |

(Reflection Coach is a built-in reviewer, left paused by design.)

## 4. Product: Automated-Video-Generator (AVG)
- **Repo:** `C:/one/Automated-Video-Generator` (GitHub: itsPremkumar/Automated-Video-Generator, MIT).
- **What it is:** self-hosted AI text-to-video (script → narrated stock-footage video). No API key.
- **Product strategy:** 3 tracks
  1. **OSS gravity** — keep AVG best-in-class free so it funnels users to paid managed runs.
  2. **Managed video service** — clients send scripts, agents generate videos via AVG (free to run).
  3. **Agent-labor marketplace** — package AVG + other agent teams as subscriptions (see pricing sheet).

## 5. Revenue model (the company must make money)
1. Packaged agent subscriptions ($49–$499/mo) — content, ops, support, lead-gen, engineering.
2. One-time builds ($990–$4,900) — custom agent/automation setup.
3. Reseller/affiliate (20–30% recurring).
4. Managed video generation per the AVG product.
5. Open-source credibility → consulting/onboarding.
See `revenue/` folder for the generated asset kits (pricing, catalog, outreach, launch plan).

## 6. Roadmap (current snapshot — tracked as Paperclip issues)
Statuses are live as of 2026-07-12. Test/probe issues (PRE-20…PRE-25, PRE-1/2/10) are excluded
from epics; they are harness/QA probes, not product work.

**Epic A — Product foundation (CTO/HoP/QA)**
- [PRE-14](/PRE/issues/PRE-14) · in_progress · AVG foundation: green CI + clean typecheck + run docs
- [PRE-7](/PRE/issues/PRE-7) · in_progress · Produce & publish 3 sample videos
- [PRE-3](/PRE/issues/PRE-3) · done · Product analysis & zero-investment monetization plan
- [PRE-4](/PRE/issues/PRE-4) · done · Company kickoff: scaffold autonomous operations

**Epic B — Product features (CTO/HoP)**
- [PRE-15](/PRE/issues/PRE-15) · in_progress · AVG features: subtitle burn-in + batch queue spec
- [PRE-16](/PRE/issues/PRE-16) · in_progress · AVG release gate: test plan + smoke check

**Epic C — GTM (CMO/CFO)**
- [PRE-17](/PRE/issues/PRE-17) · in_progress · GTM: publish pricing + launch-plan execution
- [PRE-12](/PRE/issues/PRE-12) · in_progress · Implement & publish monetization assets
- [PRE-11](/PRE/issues/PRE-11) · in_progress · Monitor job-board outreach + follow up leads
- [PRE-9](/PRE/issues/PRE-9) · done · Revenue engine: monetization assets
- [PRE-8](/PRE/issues/PRE-8) · done · Direct outreach on free job boards
- [PRE-5](/PRE/issues/PRE-5) · in_review · Showcase repo / LinkedIn page for agent offerings
- [PRE-6](/PRE/issues/PRE-6) · in_review · Agent-labor service + pricing tiers

**Epic D — Ops & delivery (COO)**
- [PRE-18](/PRE/issues/PRE-18) · in_progress · Ops: client intake + delivery SLA playbook

**Epic E — Finance (CFO)**
- [PRE-19](/PRE/issues/PRE-19) · in_progress · Finance: revenue ledger + burn=$0 guard
- [PRE-13](/PRE/issues/PRE-13) · in_progress · COMPANY_PLAN is the living master plan (this issue)

## 7. Continuous operation
- **Heartbeat** enabled on every agent → agents self-dispatch assigned issues.
- **Watchdog** (Task Scheduler, every 5 min + on boot) keeps server alive, re-auths, nudges idle
  agents, writes `company-report.md`.
- **Owner cadence:** weekly 5-min review of `company-report.md` + GitHub; approve/publish agent drafts.

## 8. Definition of success (90 days)
- AVG: CI green, 1 sample video gallery live, 50 GitHub stars.
- Revenue: 5 subscribers + 1 build = ~$245–$1,240/mo, burn $0.
- Org: 7 agents healthy, heartbeat-driven, watchdog green.

---
This plan is itself a living issue ([PRE-13](/PRE/issues/PRE-13)). Agents update it as the company evolves.
