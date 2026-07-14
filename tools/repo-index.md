# Repository Index

A searchable catalog of repositories this company depends on. More useful than bookmarks.
Keep integration status current. Add new repos via the §4 validation gate.

| Repo | Purpose | License | Maintenance | Integration | Owner | Notes |
|---|---|---|---|---|---|---|
| itsPremkumar/Hermes-Full-Autonomous-Company | **This OS** — single source of truth | MIT | active | core | itsPremkumar | CONSTITUTION lives here |
| itsPremkumar/Hermes-Prompt-Library | Versioned prompts (mirror of /prompts) | MIT | active | core | itsPremkumar | archive/ holds superseded |
| itsPremkumar/Automated-Video-Generator | Remotion video product line (AVG) | MIT | active | product | itsPremkumar | PRs PRE-14..16 |
| paperclipai/paperclip | The company runtime (org/budgets/ticketing) | OSS | active | runtime | Paperclip | embedded Postgres; not forked into this repo |
| hermes-agent (Nous) | Executive agent | OSS | active | runtime | Nous | hermes_local/gateway |
| openclaw | Comms + computer-use | OSS | active | runtime | OpenClaw | gateway :18789 |

## Rule
Before depending on a NEW repo: search GitHub, compare ≥3 mature solutions (§"Never
Reinvent"), validate (§4), then add a row here with integration status. Deprecated repos
stay listed (struck-through) for traceability — never silently dropped.

---

## Our Product Repositories (split from this OS for distribution)

Each product ships in its own public repo so it can be installed, forked, and sold
independently of the company OS. Source of truth for the OS remains this repo; these are
the publishable slices.

| Repo | What it is | Key files | Live / Status |
|---|---|---|---|
| [prem-agent-caps](https://github.com/itsPremkumar/prem-agent-caps) | AI Agent Capability Manifest Toolkit — validate/scaffold/check-deps agent manifests (Python stdlib, zero deps) | `agent_caps.py`, `test_agent_caps.py`, `README.md` | Published on ClawHub as `agent-caps` |
| [clawhub-agent-caps-skill](https://github.com/itsPremkumar/clawhub-agent-caps-skill) | ClawHub skill packaging for agent-caps (the published skill source) | `SKILL.md`, `agent_caps.py`, `examples/` | Live on ClawHub: clawhub.ai/itspremkumar/skills/agent-caps |
| [moltbook-poster](https://github.com/itsPremkumar/moltbook-poster) | Post agent-native announcements to Moltbook via REST API (stdlib, no deps) | `moltbook.py`, `post-agent-caps.json` | Agent claimed + first post live (201) |
| [ai-affiliate-engine](https://github.com/itsPremkumar/ai-affiliate-engine) | Zero-cost SEO/affiliate content engine for AI-native products | `affiliate-engine.py`, `topics.json` | Draft generator working; affiliate IDs human-gated |
| [ai-product-packs](https://github.com/itsPremkumar/ai-product-packs) | Curated AI/agent digital product packs (Gumroad-ready, $14–$47) | 7 product packs w/ `PRODUCT.md` + `LISTING.txt` | Ready to publish on Gumroad (human-gated) |
| [agent-sentinel](https://github.com/itsPremkumar/agent-sentinel) | Scan OpenClaw/Hermes skills for risky permission patterns (stdlib, offline) | `agent_sentinel.py`, `SKILL.md` | Live on ClawHub: clawhub.ai/itspremkumar/skills/agent-sentinel |
| [dev-prompts-pack](https://github.com/itsPremkumar/dev-prompts-pack) | 150 curated developer-productivity prompts (ClawHub skill source) | `PROMPTS.md`, `SKILL.md` | Live on ClawHub: clawhub.ai/itspremkumar/skills/dev-prompts |
| [company-ops](https://github.com/itsPremkumar/company-ops) | Autonomous AI company OS (CONSTITUTION + confidence-gated loop) | `CONSTITUTION.md`, `autonomy-loop.py`, `SKILL.md` | Live on ClawHub: clawhub.ai/itspremkumar/skills/company-ops |
| [agent-cost-tracker](https://github.com/itsPremkumar/agent-cost-tracker) | LLM token/cost estimator from agent logs (gpt/claude/gemini) | `agent_cost_tracker.py`, `SKILL.md` | Live on ClawHub: clawhub.ai/itspremkumar/skills/agent-cost-tracker |
| [skill-lint](https://github.com/itsPremkumar/skill-lint) | Validate ClawHub/OpenClaw skill folders before publishing | `skill_lint.py`, `SKILL.md` | Live on ClawHub: clawhub.ai/itspremkumar/skills/skill-lint |
| [prompt-lint](https://github.com/itsPremkumar/prompt-lint) | Lint prompts/SKILL.md for quality (score 0-100) | `prompt_lint.py`, `SKILL.md` | Live on ClawHub: clawhub.ai/itspremkumar/skills/prompt-lint |
| [agent-health](https://github.com/itsPremkumar/agent-health) | Probe agent dependency endpoints for up/down + latency | `agent_health.py`, `endpoints.txt`, `SKILL.md` | Live on ClawHub: clawhub.ai/itspremkumar/skills/agent-health |
| [agent-logger](https://github.com/itsPremkumar/agent-logger) | Analyze agent run logs for errors/token spikes | `agent_logger.py`, `SKILL.md`, `ci/` | Live on ClawHub: clawhub.ai/itspremkumar/skills/agent-logger |
| [manifest-diff](https://github.com/itsPremkumar/manifest-diff) | Diff two agent capability manifests | `manifest_diff.py`, `SKILL.md`, `ci/` | Live on ClawHub: clawhub.ai/itspremkumar/skills/manifest-diff |
| [cron-doctor](https://github.com/itsPremkumar/cron-doctor) | Validate/diagnose agent scheduled-task files | `cron_doctor.py`, `SKILL.md`, `ci/` | Live on ClawHub: clawhub.ai/itspremkumar/skills/cron-doctor |
| [prompt-templates-cli](https://github.com/itsPremkumar/prompt-templates-cli) | Render parameterized prompt templates from a catalog | `prompt_templates_cli.py`, `SKILL.md`, `ci/` | Live on ClawHub: clawhub.ai/itspremkumar/skills/prompt-templates-cli |
| [agent-guardrails](https://github.com/itsPremkumar/agent-guardrails) | Pre-flight safety check for planned agent actions | `agent_guardrails.py`, `SKILL.md`, `ci/` | Live on ClawHub: clawhub.ai/itspremkumar/skills/agent-guardrails |
| [skill-benchmark](https://github.com/itsPremkumar/skill-benchmark) | Composite quality score (A-F) for OpenClaw/Hermes skills | `skill_benchmark.py`, `SKILL.md`, `ci/` | Live on ClawHub: clawhub.ai/itspremkumar/skills/skill-benchmark |
| [money-engine](https://github.com/itsPremkumar/money-engine) | **Core zero-cost income engine** — affiliate/SEO content, Gumroad products, Fiverr/POD/newsletter pipelines (Hermes + OpenClaw) | `build.py`, `config.json`, `BLUEPRINT-AI-BUSINESS.md`, `gumroad/` `fiverr/` `pod/` `newsletter/` `content/` | Public; drafts-only, human-gated approval per money rules |
| [openclaw-control-guide](https://github.com/itsPremkumar/openclaw-control-guide) | Complete, verified guide to running/commanding OpenClaw as the chat/phone front-door | `README.md` | Public; mirrored into this repo at `infra/openclaw-control-guide.md` |

> **Verified 2026-07-14 (authenticated GitHub API):** all `itsPremkumar/*` repos listed above are live on GitHub. Count = 23 product/tool repos + this OS repo + 2 runtime repos (paperclipai/paperclip, hermes-agent) + openclaw. The previously-claimed "31 product repos" figure was **inaccurate** — the true live count is 23. Each product repo carries a CI/CD pipeline (`.github/workflows/ci.yml`) per the 7-axis "verify from all perspectives" workflow.
> **Local-only (NOT published — secret-bearing):** `tour` (Next.js tour-booking app, contains a real `.env`; do not push). `money-engine` was local-only until 2026-07-14, now published above.
> Moltbook key is never exported. All published repos are MIT, free, and secret-free.
> Every product carries a professional CI/CD pipeline: `.github/workflows/ci.yml` runs the
> 7-axis portfolio harness `ci/verify_product.py` (structure / frontmatter / compile /
> self-test / security / docs / deploy-ready) on Python 3.8 AND 3.11, plus a
> `ci/ci_check.py` deploy-check. This is the "verify from all perspectives" workflow.
> Marketing rule: every product announced on Moltbook (one per autonomy tick).
> Total live ClawHub skills: 31 (agent-caps, agent-sentinel, dev-prompts, company-ops,
> agent-cost-tracker, skill-lint, prompt-lint, agent-health, agent-logger, manifest-diff,
> cron-doctor, prompt-templates-cli, agent-guardrails, skill-benchmark, airtable-cli,
> arxiv-search, ascii-art-creator, ascii-video, codebase-inspection, doc-extractor,
> excalidraw-cli, file-watcher, gif-search, json-tools, maps-cli, md-linter,
> notion-api, polymarket-cli, secret-scanner, web-research, youtube-content).
> ClawHub skill README carries a donation ask (GitHub Sponsors / Buy Me a Coffee — fill
> your links).
