# Benchmarks

Track these metrics over time (trends guide improvements — roadmap V5). The autonomy loop
appends a row each tick. Source of truth for self-optimization.

## Metrics to record
- `build_time_s` — seconds for the last build/test run
- `ram_free_mb` — free RAM at tick start (hardware constraint §6)
- `cpu_pct` — rough CPU load
- `success_rate` — tasks completed / tasks attempted (rolling 7 days)
- `failure_rate` — by category (see failure-taxonomy.md)
- `revenue` — from revenue-ledger.csv (USD; human-reported until Gumroad live)
- `automation_coverage` — % of recurring tasks handled without human (target ↑)

## Log (newest last)
| Date | build_s | ram_mb | success | failures | revenue | auto_cov |
|---|---|---|---|---|---|---|
| 2026-07-13 | — | 644 | init | 0 | 0 | low (server restart, cred fix) |

## Rule
A metric that regresses for 3 consecutive ticks triggers a review (lessons-learned.md).
Revenue is NEVER fabricated (§0.3) — only real ledger entries count.
