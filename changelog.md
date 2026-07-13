# Changelog

## 2026-07-13 — Repository bootstrap + prompt consolidation (v2.0)
- Created `Hermes-Full-Autonomous-Company` as the single source of truth on GitHub.
- Pushed the real, running company from `/c/one/paperclip-company`: 8 digital products, income engine, finance ledger, `hermes-paperclip-adapter` source, COMPANY_PLAN, status snapshot.
- Consolidated six overlapping prompt drafts into **`CONSTITUTION.md` (Master Operating Prompt v2.0)**:
  - Adopted the reality-matched structure of `hermes-master-operating-prompt.md` (Paperclip + OpenClaw + budget caps + human-in-the-loop).
  - Dropped fictional stack assumptions (n8n, Mem0, CrewAI, AutoGen, standalone OmniRouter) that don't run here.
  - Removed dependence on unverified "Claude Fable 5 leaked prompts"; mandated officially-published prompt guidance instead.
  - Added explicit low-RAM / memory-discipline section (this machine is memory-starved).
  - Kept the good parts: GitHub-as-truth, tool validation, End-Goal Loops, self-improvement loop, decision framework.
- Archived the five superseded drafts in `prompts/archive/` (v0.1–v0.5, v1.0).
- Added `tools/approved.md` and `tools/rejected.md` documenting what actually runs vs. what was considered.
- Added this changelog and README index.

## Prior (local-only, pre-GitHub)
- Paperclip company stood up with 7 agents; 8 digital products generated via income engine; finance ledger + burn guard implemented (all local at `/c/one/paperclip-company`, not yet on GitHub until this commit).
