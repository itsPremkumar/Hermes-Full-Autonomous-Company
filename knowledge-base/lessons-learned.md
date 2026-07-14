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

## The "11-agent income stack" framing converts better than product lists
On 2026-07-13 a new funnel article (`revenue/blog/autonomous-ai-business-stack-2026.md`)
framed the catalog as an 11-role agent stack (Researcher→Optimizer) with a 30-day
launch table that isolates the single human-gated step (marketplace listing). This
"operating model, not a course" angle reads higher-value than a bare product list
and naturally routes readers to existing products (playbook, script packs, kits).

### Lesson
- When drafting funnel content with no `tasks.md`, lead with a reusable mental model
  (stack / system / workflow) and embed a table that separates autonomous from
  human-gated steps — it pre-qualifies readers and keeps the guardrail story explicit.
- Always end funnel posts with internal links to 2+ existing `revenue/blog/*.md`
  articles so the cluster interlinks and compounds SEO.
- Never write the listing or move money — those stay human-gated.

## Faceless-content-channel framing is a strong new funnel angle
On 2026-07-13 a new funnel article (`revenue/blog/faceless-ai-content-channel.md`)
opened a content niche the catalog was missing top-of-funnel for: building a
faceless AI YouTube/Shorts channel at $0. The angle works because it maps
directly onto two existing products (50 Viral Scripts, Remotion templates) plus
the 30-Day Launch Plan and Agent Playbook — turning "how to" content into a
product demo without naming it as one.

### Lesson
- When drafting funnel content with no `tasks.md`, a "build X with AI at $0"
  lifestyle/creator angle reaches a wider audience than the pure "AI agents for
  business" angle, and still routes readers to the same paid kits.
- Lead with a 4-step repeatable system, state the honest limits, then link 3–4
  concrete existing products. End with the GitHub-free / paid-split CTA.
- Prefer relative links (`../../digital-products/...`) so the files render on
  GitHub and in the local store without path fixes.

## Skill-security is an underserved funnel niche (2026-07-13 tick)
A new funnel article (`revenue/blog/ai-agent-skill-security-checklist.md`) opened
a content angle the catalog had no top-of-funnel for: vetting third-party agent
skills (shell/network/file capabilities) before installing them, then automating
the audit with an offline CLI scanner. It maps directly onto the **Agent Sentinel**
product (`income-engine/gumroad/products/agent-sentinel/`, $14, status ready) and
the free `secret-scanner` / `skill-lint` skills already in `clawhub-skills/`.

### Lesson
- Security/ops-adjacent "before you install X" framing is high-intent: readers
  are one bad skill away from a leaked `.env` or runaway API spend, so the pain is
  immediate and the paid tool (offline, stdlib-only, CI-gate) is an obvious yes.
- Tie each funnel article to a *specific ready product ID* (not just a category)
  so the funnel has a concrete destination and the post ages well.
- The article should be runnable on the same constrained box the company runs on
  (no deps, no network) — demonstrate that constraint as proof, not an apology.

## income-engine generators were never run (2026-07-14 tick)
On this tick, `revenue/blog/` had 7 hand-written funnel articles but the
`income-engine/content/` and `income-engine/gumroad/products/` output streams were
**empty** — the two existing generators (`generate_blog.py`, `generate_gumroad.py`)
had never been executed, even though the catalog lists 11 ready products and 5 blog
niches were configured.

### What I did (agent-safe)
- Ran `python income-engine/generate_blog.py` → it populated 5 affiliate guides into
  `income-engine/content/` (idempotent via `.used_blog.json`). The generator works
  with stdlib only; no pip.
- Wrote a new original SEO funnel article
  (`revenue/blog/2026-07-14-zero-budget-ai-automation-agency.md`) — no affiliate
  tokens, ROI-framed, links to the existing "AI agency stack" angle (compounds the
  cluster).
- Created a real `tasks.md` board mirror so future ticks have structured work and do
  not silently fall back to self-improve. Human-gated items (Gumroad publish,
  payouts, signups) are explicitly flagged, not executed.

### Lesson
- **Generators ≠ output.** Having a pipeline script is not the same as having run it.
  On a fresh tick, `git status` the known output dirs (`income-engine/content`,
  `income-engine/gumroad/products`, `revenue/blog`) before assuming work is done.
- The `generate_gumroad.py` ideas (n8n pack, ROI calculator, proposal template) do
  **not** match the 11 catalog products — a future tick should extend or replace its
  `PRODUCT_IDEAS` to emit one folder per real catalog product so the 11 ready items
  actually get Gumroad-ready listings (still human-gated to publish).
- Path gotcha re-confirmed: write_file with `/c/one/...` produced `C:\c\one\...`.
  Always use `C:\one\...` absolute Windows paths in this environment.
