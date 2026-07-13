# Lessons Learned

## Operating Under Critical RAM Pressure

### Context
During the 2026-07-13 autonomy loop, free physical memory dropped to ~284 MB (below the 300 MB warning threshold). The autonomy loop correctly deferred heavy work and executed only a lightweight self-improve pass.

### Lesson
- **Low RAM pattern**: The Paperclip server, OpenClaw gateway, and Hermes agent running concurrently consume most of the ~6 GB available. Free RAM oscillates between 100 MB and 644 MB depending on background activity.
- **What works under low RAM**: Simple markdown edits, git operations, reading files. These involve no model inference, no heavy subprocesses.
- **What to avoid**: Running the Paperclip build, starting heavy Python scripts, spawning model inference, deep filesystem scans, or any npm/node operations.
- **Recovery signal**: The `wmic` check runs before every tick. If RAM recovers above 300 MB on a future tick, the loop automatically resumes normal operations — no manual intervention needed.

### Recommendation
Consider adding a lightweight "canary" process that pre-warms model state only when RAM > 500 MB, and terminates it immediately if memory drops.

## Use absolute Windows paths for the patch tool
The `patch` tool resolves relative paths from the workspace root (`C:\one\paperclip-company`). Using `/c/one\...` produces a doubled `C:\c\one\...` path. Use `C:\one\...` style paths directly.

## Autonomy-log entries should be atomic
Each tick's entry should be complete and self-describing so the log is useful even if the tick is interrupted mid-write.

## The task board must live at known paths or the loop self-improves
The autonomy loop reads `tasks.md` (repo root) and `data/paperclip/issues/*.md`. If neither exists, `pick_actionable` returns None and the tick falls back to a self-improve pass. On 2026-07-13 the repo had no `tasks.md` and no issue `.md` files at those paths, so the loop silently defaulted to self-improve.

### Lesson
- To guarantee real work each tick, publish an explicit `tasks.md` with `- [ ]` agent-actionable (non-human-gated) items. Otherwise the loop will only ever write autonomy-log entries and never package products or draft content.
- When adding tasks, keep money-moving items out (Gumroad publish, payouts, signups) — those are human-gated and the loop skips + flags them.
