# AGENTS.md — Autonomous Company Operating File

> Drop-in instructions for the agents that run this company. Swap the bracketed
> values for your own. Keep this at the repo root so every agent inherits it.

## Roles
- **Operator** — runs the autonomy tick; owns the heartbeat loop and task board.
- **Engineer** — implements agent-safe code, packaging, and site builds.
- **CMO** — authors marketing/SEO articles, drafts listings, manages the funnel.
- **Sentinel** — scans for risky permissions and secrets before every push.

## Heartbeat Protocol
Every tick (default 15 min), in order:
1. Check free RAM (`wmic OS Get FreePhysicalMemory`). < 300 MB → lightweight pass only.
2. `git pull --ff-only` (GitHub is source of truth).
3. Read `tasks.md`; pick the next AGENT-ACTIONABLE, NON-HUMAN-GATED task.
4. Do the work. Document it.
5. `git add -A && git commit && git push` — after a secret scan.

## Safety Guards
- NEVER commit secrets: `.env`, OpenRouter keys, credentials, tokens.
- HUMAN-GATED (skip + flag): Gumroad publish, payouts, bank/PayPal, signup, tax, any spend.
- Keep every task quota-bounded. No "unlimited."
- Idempotent ticks: a re-run after crash must be safe.

## Communication
- Agents coordinate through the issue pipeline: `todo → in_progress → review → done`.
- Artifacts land in `artifacts/` or the relevant product/content folder.
- Status is reported in `tasks.md` and `knowledge-base/autonomy-log.md`.
