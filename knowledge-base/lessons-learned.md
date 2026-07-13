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

## The content funnel is the sales engine, not the products
A digital product (prompt pack, playbook, template) does not sell on autopilot. It sells because a
top-of-funnel SEO article + community posts point qualified readers at a $0-cost asset that does a
job they hate. The agent's highest-leverage non-human-gated work is *producing that funnel content*
(`revenue/blog/*.md`, Medium drafts, Moltbook posts) consistently, then packaging existing internal
assets into priced products.

### Lesson
- When no `tasks.md`/issue exists, the most reliably useful agent-safe task is to draft another
  funnel article that links to an existing product in `digital-products/` or `income-engine/gumroad/products/`.
- Keep every funnel post ending with the "free on GitHub / paid bundle" split so the funnel converts.
- Never write the listing or move money — those stay human-gated.
