# Experiment Framework

Every improvement is treated as an experiment. Fill the template, run it, record the
result, then KEEP or REVERT. This is how the OS self-optimizes (roadmap V5).

## Template
```
### EXP-<n>: <title>
- Hypothesis: <what we believe will improve X>
- Implementation: <what changed, link to commit/PR>
- Metrics: <which benchmarks.md fields; target>
- Result: <actual numbers after N runs>
- Decision: KEEP | REVERT (with reason)
- Date: <YYYY-MM-DD>
```

## Log
### EXP-001: Consolidate 6 prompt drafts into CONSTITUTION v2.0
- Hypothesis: One reality-matched constitution reduces agent confusion vs 5 overlapping drafts.
- Implementation: CONSTITUTION.md v2.0 (commit f6103ea), archived drafts in prompts/archive.
- Metrics: prompt-file count (6→1 current), agent re-work tickets.
- Result: Single source of behavior; drafts archived, not deleted.
- Decision: KEEP.

### EXP-002: Move GitHub credential to GCM (single identity)
- Hypothesis: Removing x-access-token entry stops the account-picker modal on every push.
- Implementation: stored itsPremkumar in GCM, erased x-access-token (see turn notes).
- Metrics: push prompts per session (was ∞, now 0).
- Result: 0 modals; silent push verified.
- Decision: KEEP.

### EXP-003: 24/7 cron autonomy loop (every 30m)
- Hypothesis: A scheduled loop advances the company without manual chat driving.
- Implementation: autonomy-loop.py + cron job 522e9817c283.
- Metrics: ticks/day, tasks completed, commits pushed.
- Result: <pending — measure after 1 week in benchmarks.md.
- Decision: KEEP (pending data).
