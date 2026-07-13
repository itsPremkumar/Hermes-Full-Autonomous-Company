# AI Kernel — Runtime Specification

The "AI Kernel" is the runtime substrate every task flows through. This company does NOT
build a bespoke kernel from scratch — it *composes existing components* into one. This
document is the canonical map of Kernel subsystem → real implementation. If you add a
new tool, record it here.

```
AI Kernel (composed, not invented)
│
├── Scheduler ............ Hermes cron "Company Autonomy Loop" (every 30m, forever)
│                          + Paperclip heartbeats (30s) for agent routines
├── Task Queue ........... Paperclip issues board (PRE-*) + tasks.md mirror
├── Context Manager ...... Hermes session memory (SQLite/FTS5) + CONSTITUTION §0
├── Memory Manager ....... GitHub (permanent) + Hermes skills + knowledge-base/
├── Workflow Engine ...... Paperclip routines + autonomy-loop.py + n8n-style scripts
├── Plugin Manager ....... Paperclip adapters (hermes_local, openclaw_gateway, coding CLIs)
├── Tool Manager ......... tools/approved.md + tools/rejected.md (validation gate §4)
├── Recovery Manager ...... checkpoints/ + changelog rollback notes + git history
├── GitHub Sync .......... git CLI (itspremkumar) — single source of truth
├── Knowledge Manager ..... knowledge-base/ (lessons, benchmarks, graph, experiments)
└── Monitoring Manager .... infra/monitoring + autonomy-loop.log + revenue-ledger.csv
```

## Invariant
Every action enters through this kernel. No agent writes directly to production state
without: (a) a task in the queue, (b) a confidence score ≥ threshold (see
docs/failure-taxonomy.md + autonomy-loop confidence gate), (c) a commit to GitHub.

## Why compose, not build
The reviewer's point #1 is correct in spirit but the original drafts "invented" a kernel
(n8n/Mem0/CrewAI) we don't run. The robust move is to *map the kernel onto what is
actually running* and keep it model-agnostic so any piece can be swapped.
