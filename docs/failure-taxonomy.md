# Failure Taxonomy

Every failure is categorized on sight. Each category has a recovery strategy. The autonomy
loop logs the category; the recovery is mandatory, not optional.

| Category | Example | Recovery strategy |
|---|---|---|
| Model Error | Hallucinated output, malformed JSON, off-topic | Retry with tighter prompt; if 2 fails → consult second model (§5) |
| Tool Error | CLI exits non-zero, missing binary, bad args | Check tools/approved.md run steps; reinstall if unverified; else move to rejected.md |
| Network Error | GitHub push fails, API timeout | Exponential backoff (max 3); if persists, defer to next tick, notify |
| Dependency Error | Breaking change in Paperclip API | Pin version; check dependency-graph.md; patch adapter; re-run smoke test |
| Memory Error | RAM < 300MB, OOM kill | Kill non-essential procs; save checkpoint; defer heavy work (CONSTITUTION §6) |
| Logic Error | Wrong file edited, regressed feature | `git revert` to last good commit; document in lessons-learned.md |
| User Error | Human gave contradictory instruction | Stop; clarify via the human gate (§0.6) |
| Unknown | Unclassified crash | Capture logs to autonomy-loop.log; escalate to human with context |

## Confidence gate (paired with this taxonomy)
Before any significant action, the agent estimates confidence 0–100%:
- **≥ 90%** → proceed, still commit + push.
- **75–89%** → proceed + run a validation step (test/build/doc check).
- **50–74%** → consult a second model before shipping.
- **< 50%** → escalate to human (§0.6). Never guess on irreversible/costly/legal steps.

Implemented in autonomy-loop.py (`CONFIDENCE` constant + human-gate already present).
