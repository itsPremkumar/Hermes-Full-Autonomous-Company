# 🔍 GOAL PROMPT — RESEARCH NEW END-TO-END AI MONEY AUTOMATION IDEAS

Paste-ready `/goal draft` (Section 1) + activation (Section 2).
Purpose: autonomously RESEARCH and DOCUMENT fresh, complete, end-to-end,
100%-free AI automation money-making ideas — not build them, find + validate them.

================================================================
## SECTION 1 — PASTE THIS AS A SLASH COMMAND
================================================================

/goal draft Research and document COMPLETE end-to-end AI automation money-making ideas that are (a) fully automatable end-to-end, (b) buildable on 100% free/open-source tooling, (c) validated by real 2026 market data (not speculation). Work inside the Hermes-Full-Autonomous-Company repo at C:\one\paperclip-company.

Process the research in 5 phases and write findings to research/ as you go:

PHASE 1 — Source scan (use web-research + arxiv + your own 100 learned skills index at Hermes-Full-Autonomous-Company/skills/SKILLS_INDEX.md):
  - Scan current (2026) trends: agentic commerce, AI services demand, no-code automation niches, underserved SMB pain points.
  - Cross-reference against the existing 31 ClawHub skills + 100 learned skills to find capability gaps = opportunity.

PHASE 2 — Idea generation:
  - Produce 20 candidate ideas, each scored on: (1) automatable end-to-end?, (2) free-tool feasibility?, (3) validated demand (cite source+number)?, (4) margin %, (5) time-to-first-dollar.
  - Reject any idea needing paid APIs, manual fulfillment, or unproven demand.

PHASE 3 — Deep validation (for the top 10):
  - For each: find 1+ real pricing data point (Fiverr/Upwork gig price, SaaS tier, freelance rate), 1+ demand signal (search trend, marketplace listing count, growth %), 1+ free-tool stack that delivers it (name the actual OSS: n8n, Stirling-PDF, Listmonk, Chatwoot, your ClawHub skills).
  - Cite every claim with a URL or repo path.

PHASE 4 — Blueprint each top idea into a reusable pipeline shape:
  - Reuse the proven structure from money/pipeline1..12 (data dict + build_package + self-test + n8n workflow spec).
  - Write each as money/pipelineN_ideaname.py so it drops into run_all.py later.
  - Include: intake (free), delivery (free self-hosted), payment (UPI/marketplace), acquisition (Moltbook/X).

PHASE 5 — Synthesize:
  - Write research/MONEY_IDEAS_2026.md: ranked table of all ideas with scores, validated data, free stacks, and a 90-day rollout plan.
  - Update money/MONEY_AUTOMATION_IDEAS.md if any idea beats an existing one.
  - Emit a Moltbook draft (revenue/moltbook/post-research-ideas.json) summarizing the top 3.

VERIFICATION the judge must check before DONE:
  - research/ has MONEY_IDEAS_2026.md with >=10 validated ideas, each with a cited data point + a named free tool stack.
  - >=3 pipelineN_ideaname.py files exist, each passing `python money/pipelineN_ideaname.py self-test`.
  - Every demand/price claim has a URL or repo citation (no unsourced assertions).
  - Moltbook draft exists.

STOP only if web access fails entirely (then note the block and pause).

================================================================
## SECTION 2 — AFTER DRAFT RETURNS A CONTRACT, PASTE:
================================================================

/goal <paste the exact contract text Hermes returned in Section 1>

================================================================
## ONE-TIME PREREQ (research can run long):
================================================================

hermes config set agent.goal_max_turns 200

================================================================
## WHAT THIS GOAL DELIVERS (end state):
================================================================

  research/MONEY_IDEAS_2026.md
    └─ ranked table: 20 ideas scored, top 10 deep-validated with citations
    └─ free-tool stack named for each
    └─ 90-day rollout plan
  money/pipeline13_*.py ... pipelineN_*.py   (drop-in ready, self-test passing)
  revenue/moltbook/post-research-ideas.json  (promo draft)

================================================================
## HUMAN GATES (minimal — research is mostly autonomous):
================================================================

  Gate 1: none required to RESEARCH. (You only act if you later choose to BUILD an idea.)
  If you want, after research: set a second /goal to BUILD the top idea using
  the pipelineN_*.py scaffold this research produced.

================================================================
## NOTES
================================================================

- This goal is SAFE to run fully autonomously — it only reads + writes files,
  no accounts, no payment, no external posting (the Moltbook draft is queued,
  not auto-posted unless your scheduler is on).
- It reuses your existing verified tooling (web-research skill, arxiv, the
  100-skill index) so findings are grounded, not hallucinated.
- Output feeds directly into the existing money system: a new idea = a new
  pipeline = a new row in INCOME_DASHBOARD.md.
