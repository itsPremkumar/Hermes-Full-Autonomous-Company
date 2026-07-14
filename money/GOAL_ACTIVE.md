# 🎯 ACTIVE GOAL — Zero-to-Revenue Autonomous Money System

> Durable, machine-readable contract embodied by the `money-goal-keeper` cron
> (created 2026-07-14). This is the standing goal for the money-earning
> automation project. The cron runs it turn-after-turn, self-verifies with
> real command output, and PAUSES at the 3 human gates below.

## Objective
Advance the Hermes-Full-Autonomous-Company money engine from its current
healthy state (15 pipelines / 62 packages, all priced, self-test OK) toward
first recurring revenue — without breaking what already works.

## Standing invariants (never violate)
- `python run_all.py self-test` MUST keep returning:
  `self-test: OK — 15 pipelines, 62 packages, all priced`
- All shell/terminal commands MUST be bounded (timeout, `|| true`) — the host
  has ~6 GB RAM with frequently <200 MB free; unbounded commands fork-fail
  (EAGAIN) and stall the loop.
- Prefer `wmic.exe` over `/proc` for Windows process inspection.
- Keep everything stdlib-only / zero external cost.

## Per-tick acceptance checks (verify with REAL output, not claims)
1. **Engine health:** `run_all.py self-test` → 15 pipelines / 62 packages OK.
2. **Dashboard current:** `INCOME_DASHBOARD.md` dated today, counts match.
3. **Listings complete:** every `*_packs` dir under `money/` has a matching
   `listings/<name>/` with platform-ready copy (Fiverr/Upwork/Gumroad).
4. **Acquisition loop:** Moltbook scheduler fired in the last 24h (check
   `cronjob` for `Moltbook post scheduler` last_status=ok); affiliate +
   cold-email drivers present and referenced from a schedule.
5. **Stale docs fixed:** README.md / GO_LIVE_CHECKLIST.md numbers match
   reality (15 pipelines, 62 packages) — not the old "12 / 50".
6. **Cron fleet:** all 16 money crons show last_status != "error". If a cron
   errored with `APIConnectionError`, do NOT edit the job — it self-heals on
   the next tick; just log it. If it errored with a real code fault, repair
   the underlying script and report the fix.

## Repair rules (auto, within budget)
- If check #3 fails: regenerate missing listings via `generate_listings.py`,
  then re-verify.
- If check #5 fails: regenerate the doc from live data (don't hand-edit
  numbers that can drift).
- If a NEW pipeline (#16+) is warranted by research, follow the proven shape
  (data dict + build_package + self-test + --list + --out) and wire it into
  run_all.py; bump the self-test invariant accordingly.

## The 3 HUMAN GATES — loop PAUSES here, prints a 3-action checklist, waits
1. **Account gate** — create Fiverr/Upwork accounts (ID verification).
2. **Payment gate** — link PayPal/Stripe (bank, tax).
3. **First-gig gate** — first gig ready to publish; you click Publish.

After each gate the user runs `hermes chat -q "/goal resume"` (or replies in
chat) and the loop continues.

## Turn budget
Respect `agent.goal_max_turns` (set to 120). On budget exhaustion, report
status and stop — do NOT loop forever.

## Stop condition (goal "achieved")
First recurring revenue confirmed (a published gig with a paid order, or a
subscription signup) AND all invariants green. At that point print the
revenue proof and mark the goal complete.
