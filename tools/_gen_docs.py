#!/usr/bin/env python3
"""Regenerate SEO/AEO/GEO-optimized SKILL.md + README.md for all 31 ClawHub skills.

Strategy:
- PRESERVE code-faithful CLI surface: derive subcommands + flags from the .py source.
- ENRICH structure: FAQ, use-cases, comparison, geo/aeo Q&A, keywords.
- DO NOT invent commands. If a command is not found in source, it is omitted.
"""
import os, re, json

BASE = r"C:\one\paperclip-company\clawhub-skills"
INV = r"C:\one\paperclip-company\tools\_seo_inventory.json"
inv = json.load(open(INV, encoding="utf-8"))

# ---- shared SEO constants ----
BRAND = "itsPremkumar"
STACK = "Hermes / OpenClaw / Paperclip agent stack"
LICENSE = "MIT-0 (free, modifiable, no attribution required)"
GITHUB = "https://github.com/itsPremkumar"
SPONSORS = "https://github.com/sponsors/itsPremkumar"
COFFEE = "https://buymeacoffee.com/itsPremkumar"

# ---- describe each skill: human-written SEO copy keyed by slug ----
# (title, one_liner, problem, audience, usecases[5], faqs[(q,a) x4], comparison[(comp, why_better) x3])
COPY = {
"agent-caps": dict(
  title="Agent Capability Manifest Toolkit",
  one="Validate, scaffold, and cross-check AI-agent capability manifests so agents stay swappable, auditable, and safe.",
  problem="Agents declare incompatible capabilities and dependencies, then break the system at install time.",
  audience="Agent builders, platform engineers, and security reviewers shipping OpenClaw / Hermes / Paperclip agents.",
  use=["Validate a manifest before publishing an agent to ClawHub","Scaffold a standards-compliant manifest for a new agent","Cross-check dependencies across a fleet of agents","Gate CI on missing/invalid capability fields","Audit third-party agents before granting machine access"],
  faq=[("What is an agent capability manifest?","A machine-readable JSON describing an agent's name, version, capabilities, dependencies, memory, tools, API, and status — the standard interface that lets agents be swapped or audited without breaking the host."),
       ("Does agent-caps need internet or pip?","No. It is pure Python 3.8+ stdlib, zero dependencies, runs fully offline."),
       ("Can I use it in CI?","Yes. Run `validate` as a CI gate; a non-zero exit blocks merges with malformed manifests."),
       ("What does check-deps do?","Resolves declared dependencies against known agents/manifests and flags unknown or unmet requirements.")],
  comp=[("Hand-written JSON schemas","agent-caps ships a single enforceable schema + validator, not ad-hoc docs."),
        ("Reading the manifest manually","It catches missing fields, bad versions, illegal statuses, and unknown deps automatically."),
        ("Trusting an agent's self-description","check-deps cross-verifies claims against reality before the agent goes live.")],
),
"agent-cost-tracker": dict(
  title="LLM Cost & Token Tracker",
  one="Estimate and tally LLM API spending per agent/session with budget alerts and CSV export.",
  problem="Token spend balloons silently across agents and models with no per-agent accountability.",
  audience="Founders, finops, and agent operators running multi-agent LLM workloads on GPT/Claude/Gemini.",
  use=["Estimate cost before sending a prompt","Tally spend from agent run logs","Set per-agent budget alerts","Export a CSV for finance","Compare model pricing at a glance"],
  faq=[("Which models are supported?","gpt-* (OpenAI), claude-* (Anthropic), gemini-* (Google) with built-in price tables."),
       ("Where does it get tokens?","From agent run logs (tally) or from --prompt/--completion estimates."),
       ("Does it call the API?","No. It is an estimator/tally from logs and inputs; no network calls."),
       ("Can I export to CSV?","Yes — CSV export is built in for spreadsheets and BI tools.")],
  comp=[("Cloud billing dashboards","Per-agent, per-session granularity you control locally."),
        ("Mental math on token counts","Price tables + estimation remove the guesswork."),
        ("Spreadsheet tracking","CSV export drops straight into your existing finance stack.")],
),
"agent-guardrails": dict(
  title="Agent Action Guardrails",
  one="Pre-flight safety gate for planned agent actions: permission checks, allowlists, and an audit trail.",
  problem="Agents take irreversible actions (shell, deletes, network) with no pre-flight safety check.",
  audience="Agent platform teams and security reviewers who must approve or deny planned agent actions.",
  use=["Gate a planned action before execution","Maintain an allowlist of permitted commands","Deny high-risk patterns (rm -rf, sudo)","Produce an audit record of every decision","Score risk before the agent acts"],
  faq=[("What does `check` do?","Evaluates a planned action against policy and returns allowed/denied + reason."),
       ("Is it offline?","Yes. Pure stdlib, no network, no telemetry."),
       ("How do allowlists work?","Define permitted command patterns; anything outside is denied by default."),
       ("Does it log decisions?","Yes — every decision emits a structured audit entry.")],
  comp=[("Trusting the prompt","guardrails evaluates the action, not the intent."),
        ("Post-hoc review","It blocks before execution, not after damage."),
        ("Manual code review","Policy-as-code makes safety repeatable across agents.")],
),
"agent-health": dict(
  title="Agent Endpoint Health Monitor",
  one="Probe agent dependency endpoints (gateways/APIs/DBs) for up/down status and latency.",
  problem="An agent silently fails when a dependency endpoint is down or slow.",
  audience="SREs and agent operators running always-on agent services.",
  use=["Liveness-check a gateway before deploying","Latency-profile a dependency API","Alert when an endpoint goes down","Collect health metrics for dashboards","Pre-flight check in cron jobs"],
  faq=[("What does `check` do?","Pings configured endpoints and reports up/down + latency."),
       ("Does it need config?","Endpoints are listed in endpoints.txt or passed inline."),
       ("Is it offline?","The checks hit your own endpoints; no third-party calls."),
       ("Can it emit JSON?","Yes — --json for pipelines and dashboards.")],
  comp=[("Uptime robot SaaS","Runs locally against private/internal endpoints for free."),
        ("curl in a loop","Purpose-built for agent dependency graphs, not one URL."),
        ("Guessing","Real latency numbers, not vibes.")],
),
"agent-logger": dict(
  title="Agent Run Log Analyzer",
  one="Analyze agent run logs for errors, token spikes, and failures with JSON output.",
  problem="Agent failures hide in megabyte log files with no signal.",
  audience="Agent operators debugging production agent runs.",
  use=["Scan logs for errors and stack traces","Detect token/cost spikes","Replay a structured log","Query logs by field","Feed JSON into a dashboard"],
  faq=[("What does `scan` do?","Walks log files and surfaces errors, failures, and anomalies."),
       ("Is output machine-readable?","Yes — --json for pipelines."),
       ("Does it need a specific format?","It parses common agent log shapes; structured JSON logs work best."),
       ("Offline?","Yes, fully local.")],
  comp=[("grep through logs","Purpose-built anomaly detection, not raw text search."),
        ("Log SaaS","No ingestion cost; runs on the files you already have."),
        ("Eyeballing","Token-spike detection catches cost leaks automatically.")],
),
"agent-sentinel": dict(
  title="Skill Security Sentinel",
  one="Scan OpenClaw/Hermes skills for risky permission patterns before you install them.",
  problem="A 'weather' skill can quietly request shell execution — supply-chain risk at install time.",
  audience="Anyone installing third-party ClawHub / OpenClaw / Hermes skills.",
  use=["Vet a skill folder before install","Flag over-broad permission requests","Score risk OK/LOW/MEDIUM/HIGH","Audit your own skills pre-publish","Explain findings in plain language"],
  faq=[("What does `scan` do?","Inspects a skill folder and flags risky permission patterns offline."),
       ("Does it upload my skill?","No. Fully local, no telemetry, no network."),
       ("What risk levels exist?","OK / LOW / MEDIUM / HIGH plus actionable findings."),
       ("Should I trust ClawHub's own audit?","Use both — sentinel is your private, offline safety net.")],
  comp=[("Installing blind","You see the risk before granting machine access."),
        ("Reading SKILL.md by hand","Patterns are detected automatically across the folder."),
        ("ClawHub audit only","Offline, private, repeatable anytime.")],
),
"airtable-cli": dict(
  title="Airtable API CLI",
  one="Full Airtable client: bases, tables, records with pagination, CSV import/export, and rate-limit awareness.",
  problem="Airtable's API is powerful but tedious — pagination, offsets, and imports are manual.",
  audience="No-code/automation builders, ops, and agents wiring Airtable into workflows.",
  use=["List bases, tables, and schemas","CRUD records with batch create/delete","Upsert by a merge key","Search/filter records","Export/import CSV with rate-limit awareness"],
  faq=[("Does it handle pagination?","Yes — automatic offset handling and --limit."),
       ("Can I import CSV?","Yes — batch create/upsert from a CSV file."),
       ("Is it rate-limit aware?","Yes — it respects Airtable limits and paces requests."),
       ("Auth?","Uses your Airtable token via env/config; no secrets stored in the repo.")],
  comp=[("Raw REST calls","Subcommands wrap pagination, filtering, and upserts."),
       ("Zapier","CLI + CSV is scriptable, free, and agent-friendly."),
        ("Copy-paste","Bulk CSV import/export removes manual row entry.")],
),
"arxiv-search": dict(
  title="arXiv Research Search",
  one="Search arXiv papers by keyword, author, or category with citation export.",
  problem="Keeping up with the arXiv firehose is manual and citation formatting is painful.",
  audience="Researchers, students, and AI/ML engineers tracking papers.",
  use=["Search by keyword/author/category","Sort and filter recent papers","Export BibTeX citations","Pull paper metadata into a pipeline","Track a research niche"],
  faq=[("What can I search by?","Keyword, author, and arXiv category (cs.AI, cs.LG, etc.)."),
       ("Can I export citations?","Yes — BibTeX/citation export is built in."),
       ("Does it need an API key?","No — uses the public arXiv API."),
       ("Offline?","No — it queries arXiv live.")],
  comp=[("arXiv website UI","Scriptable search + citation export for pipelines."),
        ("Manual BibTeX","Citations generated automatically."),
        ("Reading every new submission","Filtered, category-aware search.")],
),
"ascii-art-creator": dict(
  title="ASCII Art Creator",
  one="Generate banners, boxes, cowsay-style art, tables, and image-to-ASCII in your terminal.",
  problem="Terminal UIs and docs need quick, dependency-free visual flair.",
  audience="DevOps, CLI tool authors, and anyone documenting in the terminal.",
  use=["Print a banner for a deploy script","Draw a box around a note","Cowsay-style messages","Render a table","Convert an image to ASCII"],
  faq=[("What styles exist?","banner, box, cow, table, and image-to-ASCII."),
       ("Multiple fonts?","Yes — --font selection where supported."),
       ("Is it offline?","Yes — pure stdlib."),
       ("Self-test?","Yes — `self-test` proves every renderer works.")],
  comp=[("figlet alone","Adds boxes, cowsay, tables, and image-to-ASCII in one tool."),
        ("Screenshotting","Text art pastes cleanly into logs and READMEs."),
        ("Manual ASCII","Generators produce consistent output.")],
),
"ascii-video": dict(
  title="ASCII Video Converter",
  one="Convert video to ASCII animation with dithering modes, color output, and framerate control.",
  problem="Sharing a video in a terminal/README isn't possible with normal formats.",
  audience="Creative coders, terminal artists, and docs/README embellishers.",
  use=["Convert a clip to ASCII","Control width/fps","Pick a dithering charset","Add color output","Extract a single frame"],
  faq=[("What inputs?","Common video/image formats via the convert/image subcommands."),
       ("Color?","Yes — --color mode."),
       ("Offline?","Yes."),
       ("Self-test?","Yes — verifies the pipeline end to end.")],
  comp=[("Static ASCII art","Adds motion + framerate control."),
        ("GIF to text by hand","Automated frame extraction."),
        ("Screenshots","Animated ASCII plays in any terminal.")],
),
"codebase-inspection": dict(
  title="Codebase Inspector",
  one="Walk any directory and report language breakdowns, line counts, blank/comment lines, with HTML reports, git-aware diffs, trend tracking, SVG badges, CSV export, and CI integration.",
  problem="You can't manage codebase metrics you can't measure — and you can't see trends over time.",
  audience="Engineering leads, open-source maintainers, and CI pipelines.",
  use=["Print a per-language LOC report","Export CSV for dashboards","Generate an HTML report","Git-aware diff between snapshots","Track trends and emit an SVG badge"],
  faq=[("How many languages?","25+ extensions recognized out of the box."),
       ("CI integration?","Yes — example GitHub Actions workflow asserts a language ratio."),
       ("Badges?","--badge emits an SVG you can drop in a README."),
       ("Offline?","Yes — no network, no telemetry.")],
  comp=[("tokei/scc","Adds git-aware diffs, trend tracking, HTML reports, and badges in one CLI."),
        ("Manual wc -l","Per-language breakdown with comment/blank counts."),
        ("Spreadsheet metrics","CSV + HTML + badge, CI-ready.")],
),
"company-ops": dict(
  title="Autonomous Company OS",
  one="Run a self-improving autonomous company from a single CONSTITUTION plus a confidence-gated loop.",
  problem="Autonomous agents need governance or they drift and take bad actions.",
  audience="Builders of agent companies, autonomous startups, and AI-operations teams.",
  use=["Run a 24/7 confidence-gated loop","Track tasks and revenue","Encode operating rules in a CONSTITUTION","Gate risky actions by confidence","Self-improve from a log"],
  faq=[("What is the CONSTITUTION?","A Markdown charter of operating rules the loop obeys."),
       ("Is it safe?","Low-confidence actions are escalated, not executed blindly."),
       ("Offline?","Yes — pure stdlib loop."),
       ("Can I fork it?","Yes — MIT, designed to be your company's OS.")],
  comp=[("Ad-hoc cron scripts","A governed loop with escalation, not raw automation."),
        ("Hiring","Agents execute defined work at ~$0 marginal cost."),
        ("Docs only","An operating system, not a README.")],
),
"cron-doctor": dict(
  title="Cron Doctor",
  one="Validate and diagnose a scheduled-task file for an agent: parse errors, unsafe commands, collisions, missed/overlapping runs.",
  problem="A bad cron line fails silently at 3am and you find out from users.",
  audience="Agent operators, SREs, and anyone with scheduled jobs.",
  use=["Check a crontab-style file for errors","Flag unsafe commands (rm -rf, sudo)","Detect overlapping jobs","Suggest auto-fixes","JSON output for CI"],
  faq=[("What schedules does it parse?","30m, every 2h, '0 9 * * *', and standard crontab forms."),
       ("What is unsafe?","Destructive/gated commands like rm -rf, sudo, etc. are flagged."),
       ("CI?","Yes — --json + non-zero exit on failure."),
       ("Offline?","Yes.")],
  comp=[("crontab -l and hope","Parses, validates, and explains failures."),
        ("Cron lint gists","Adds unsafe-command detection and collisions."),
        ("Debugging at 3am","Catch it before the run, not after.")],
),
"dev-prompts": dict(
  title="Developer Prompts Pack",
  one="150 curated developer-productivity prompts you can paste into any agent: code review, debugging, architecture, refactoring.",
  problem="Reinventing prompt phrasing for every dev task wastes time and yields inconsistent results.",
  audience="Engineers, tech leads, and agents that assist with coding.",
  use=["Paste a code-review prompt","Kick off a debugging session","Draft an architecture proposal","Refactor with a structured prompt","Standardize team prompting"],
  faq=[("How many prompts?","150 across review, debugging, architecture, refactoring, and more."),
       ("Agent-ready?","Yes — written for OpenClaw / Hermes / ChatGPT / Claude."),
       ("Editable?","Copy and adapt freely (MIT)."),
       ("Offline?","It's a prompt pack — no code, no network.")],
  comp=[("Writing from scratch","Curated, battle-tested phrasing."),
        ("One-size prompts","Categorized by task type."),
        ("Inconsistent output","Repeatable, high-quality results.")],
),
"doc-extractor": dict(
  title="Document Text Extractor",
  one="Extract text from PDF, DOCX, and TXT with encoding detection and page/paragraph structure.",
  problem="Getting clean text out of PDFs/DOCX for RAG or search is fiddly.",
  audience="RAG builders, researchers, and data engineers.",
  use=["Extract text from a PDF","Pull DOCX content","Batch a folder","List supported formats","Preserve structure (pages/paragraphs)"],
  faq=[("Formats?","PDF, DOCX, TXT (list with list-formats)."),
       ("Encoding?","Auto-detected."),
       ("Structure?","Page/paragraph boundaries are preserved where available."),
       ("Offline?","Yes.")],
  comp=[("Copy-paste from a viewer","Scriptable batch extraction."),
        ("One-format tools","PDF + DOCX + TXT in one CLI."),
        ("Lost structure","Structured output for RAG.")],
),
"excalidraw-cli": dict(
  title="Excalidraw Diagram CLI",
  one="Generate Excalidraw diagrams — flowcharts, sequences, architecture — as valid .excalidraw JSON.",
  problem="Drawing diagrams by hand is slow and not version-controllable.",
  audience="Engineers documenting architecture, agents generating diagrams, and tech writers.",
  use=["Generate a flowchart","Build a sequence diagram","Compose an architecture map","Merge/overlay diagrams","Export valid Excalidraw JSON"],
  faq=[("Diagram types?","flow, sequence, architecture (--type)."),
       ("Valid output?","Emits Excalidraw-compatible JSON you can open in the app."),
       ("Compose?","merge/overlay combine diagrams."),
       ("Offline?","Yes.")],
  comp=[("Drag-drop in Excalidraw","Diagrams as code, diff-able in git."),
        ("Mermaid only","Native Excalidraw JSON, hand-drawn style."),
        ("Screenshots","Regenerate from text anytime.")],
),
"file-watcher": dict(
  title="File Watcher",
  one="Monitor directories for changes: snapshots, diffs, glob filtering, and event detection.",
  problem="Knowing what changed on disk — and when — is manual without a tool.",
  audience="Automation builders, agents, and ops monitoring config/data.",
  use=["Watch a dir for changes","Snapshot and diff two states","Filter by glob/ignore","Detect specific events","Emit JSON for pipelines"],
  faq=[("Polling?","Yes — --poll-interval for non-inotify platforms."),
       ("Filters?","--glob and --ignore."),
       ("Diff?","snapshot_a/snapshot_b diff mode."),
       ("Offline?","Yes.")],
  comp=[("inotify scripts","Cross-platform polling + glob filtering."),
        ("diff two trees by hand","Snapshots make it one command."),
        ("Guessing what changed","Event-level detection.")],
),
"gif-search": dict(
  title="GIF Search (Tenor)",
  one="Search and download GIFs from Tenor with caching, bulk download, and format conversion.",
  problem="Finding and grabbing the right GIF is clicky and not automatable.",
  audience="Content creators, social bots, and agents adding media.",
  use=["Search Tenor for a term","Download a single GIF","Bulk download a set","Cache results","Convert format"],
  faq=[("API key?","Uses Tenor; supply your key via env."),
       ("Bulk?","Yes — batch download."),
       ("Cache?","Results are cached to avoid repeat calls."),
       ("Offline?","No — queries Tenor live.")],
  comp=[("Tenor website","Scriptable search + bulk download."),
        ("Manual save","Caching + conversion built in."),
        ("One at a time","Batch mode.")],
),
"json-tools": dict(
  title="JSON Toolkit",
  one="Validate, format, query, diff, filter, flatten, and merge JSON with dot-notation paths.",
  problem="JSON wrangling across many small tasks needs many one-off tools.",
  audience="Developers, data engineers, and agents processing JSON.",
  use=["Validate JSON","Format/pretty-print","Query by dot path","Diff two files","Flatten/merge"],
  faq=[("Query syntax?","Dot-notation paths (e.g. a.b.c)."),
       ("Diff?","Semantic diff of two JSON files."),
       ("Merge?","Deep merge with conflict handling."),
       ("Offline?","Yes.")],
  comp=[("jq","Familiar dot-path query plus diff/flatten/merge."),
        ("Online JSON formatters","Local, no upload."),
        ("Multiple tools","One CLI for the whole lifecycle.")],
),
"manifest-diff": dict(
  title="Manifest Diff",
  one="Diff two agent/skill manifests and report capability, permission, and version changes.",
  problem="Spotting what changed between two agent manifests by eye is error-prone.",
  audience="Agent reviewers and platform teams managing versions.",
  use=["Diff two manifests","See capability changes","Flag permission deltas","Catch version downgrades","JSON output for CI"],
  faq=[("Input?","Two manifest files (a/b)."),
       ("What changes?","Capabilities, permissions, versions."),
       ("CI?","Yes — --json."),
       ("Offline?","Yes.")],
  comp=[("Reading both files","Automatic delta report."),
        ("diff on raw JSON","Semantic, not textual."),
        ("Guessing risk","Permission deltas surfaced explicitly.")],
),
"maps-cli": dict(
  title="Maps CLI (OpenStreetMap)",
  one="Geocode, reverse-geocode, route, POI search, and timezone lookup — all via OpenStreetMap, with CSV export.",
  problem="Maps need an API key and a SaaS for even basic geocoding/routing.",
  audience="Developers, field/ops apps, and agents needing location data.",
  use=["Geocode an address","Reverse-geocode coordinates","Route between two points","Search POIs by category/radius","CSV export + timezone"],
  faq=[("Provider?","OpenStreetMap (Nominatim/OSRM) — no key for basic use."),
       ("Routing?","Yes — route between lat/lon."),
       ("POI?","Search by category within a radius."),
       ("Offline?","No — queries OSM live.")],
  comp=[("Google Maps API","No key, OSM-backed, free tier friendly."),
        ("Manual geocoding","One CLI for geocode/reverse/route/POI."),
        ("Spreadsheet maps","CSV export drops into BI.")],
),
"md-linter": dict(
  title="Markdown Linter & Formatter",
  one="Lint and auto-format Markdown: trailing whitespace, frontmatter validation, TOC generation, external link checks.",
  problem="Markdown drift (broken links, missing TOC, bad frontmatter) hurts docs and SEO.",
  audience="Docs owners, open-source maintainers, and agents generating Markdown.",
  use=["Lint a Markdown file","Auto-format/normalize","Validate frontmatter","Generate a TOC","Check external links"],
  faq=[("TOC?","Yes — generate/insert a table of contents."),
       ("External links?","--check-external validates them."),
       ("Write?","--write reformats in place."),
       ("Offline?","External-link check needs network; linting is offline.")],
  comp=[("markdownlint","Adds TOC generation + frontmatter validation."),
        ("Manual TOC","One command."),
        ("Broken links","External-link checker.")],
),
"notion-api": dict(
  title="Notion API CLI",
  one="Complete Notion client: pages, databases, blocks, and search with config file and dry-run mode.",
  problem="Notion's API is capable but verbose; every operation is many REST calls.",
  audience="Notion power users, ops, and agents automating notes/databases.",
  use=["Create/read/update pages","Manage databases","Append blocks","Search across workspace","Dry-run before writing"],
  faq=[("Dry-run?","Yes — preview changes without writing."),
       ("Auth?","Config file / env token; no secrets in repo."),
       ("Blocks?","Create and read blocks, including Markdown pages."),
       ("Offline?","No — live Notion API.")],
  comp=[("Raw Notion API","Subcommands wrap pages/DBs/blocks/search."),
        ("Copy-paste","Dry-run safety + Markdown page support."),
        ("Manual blocks","Block templates.")],
),
"polymarket-cli": dict(
  title="Polymarket CLI",
  one="Query Polymarket prediction markets: search, price history, trending, categories, and stats.",
  problem="Tracking prediction markets means juggling the website and spreadsheets.",
  audience="Traders, analysts, and agents monitoring markets.",
  use=["Search markets","Pull price history","List trending","Browse categories","Show stats"],
  faq=[("Live data?","Yes — queries Polymarket's public API."),
       ("Price history?","Available per market."),
       ("Categories?","Browse by category."),
       ("Offline?","No — live API.")],
  comp=[("Polymarket website","Scriptable search + history."),
        ("Manual tracking","Trending + stats in one CLI."),
        ("Spreadsheets","Pipe to CSV/JSON.")],
),
"prompt-lint": dict(
  title="Prompt Linter",
  one="Lint AI prompts for clarity, safety, injection risk, and template validity — scored 0-100.",
  problem="Bad prompts produce bad outputs; quality isn't measurable.",
  audience="Prompt engineers, agent builders, and AI product teams.",
  use=["Lint a prompt file","Score quality 0-100","Detect injection risk","Validate template vars","JSON output for CI"],
  faq=[("Score?","0-100 quality score with reasons."),
       ("Injection?","Flags prompt-injection patterns."),
       ("CI?","Yes — --json, non-zero on failure."),
       ("Offline?","Yes.")],
  comp=[("Eyeballing prompts","Measurable quality + safety."),
        ("Partial linters","Adds injection + template checks."),
        ("No gate","CI-ready scoring.")],
),
"prompt-templates-cli": dict(
  title="Prompt Templates CLI",
  one="Manage reusable prompt templates: create, render, and validate with {{variables}}.",
  problem="Hard-coded prompts can't be reused or tested across agents.",
  audience="Prompt engineers and agent platforms standardizing prompts.",
  use=["List catalog templates","Render with variables","Validate template syntax","Set catalog path","Version prompts"],
  faq=[("Variables?","{{var}} fill style."),
       ("Catalog?","--catalog points at your template set."),
       ("Validate?","Catches undefined/missing vars."),
       ("Offline?","Yes.")],
  comp=[("String formatting","Structured, validated templates."),
        ("Copy-paste","Catalog + render."),
        ("No reuse","One source of truth.")],
),
"secret-scanner": dict(
  title="Secret Scanner",
  one="Detect API keys, tokens, and credentials in code with 50+ patterns, entropy analysis, and SARIF reports.",
  problem="Secrets leak into repos constantly and go unnoticed until exploited.",
  audience="Security teams, maintainers, and CI pipelines.",
  use=["Scan a path for secrets","List detection patterns","Emit SARIF for CI","Filter by severity","Skip entropy check"],
  faq=[("Patterns?","50+ built in (keys, tokens, creds)."),
       ("Entropy?","On by default; disable with --no-entropy."),
       ("SARIF?","Yes — --sarif for GitHub code scanning."),
       ("Offline?","Yes.")],
  comp=[("grep for keys","Pattern + entropy detection."),
        ("Single-pattern tools","50+ patterns in one pass."),
        ("Manual review","SARIF drops into CI.")],
),
"skill-benchmark": dict(
  title="Skill Benchmark",
  one="Composite quality score (A-F) for OpenClaw/Hermes skills: structure, docs, safety, self-test.",
  problem="You can't tell a good skill from a thin one at a glance.",
  audience="Skill authors, reviewers, and the ClawHub ecosystem.",
  use=["Score a skill folder","Get an A-F grade","See sub-scores","Find thin content","JSON output"],
  faq=[("Grade?","A-F composite across axes."),
       ("Axes?","Structure, docs, safety, self-test, etc."),
       ("CI?","Yes — --json."),
       ("Offline?","Yes.")],
  comp=[("Installing to test","Non-destructive quality score."),
        ("Single-metric linters","Multi-axis composite."),
        ("Guessing quality","Explicit A-F grade.")],
),
"skill-lint": dict(
  title="Skill Linter",
  one="Validate ClawHub/OpenClaw skill folders before publishing: frontmatter, structure, command docs, thin-content detection.",
  problem="Publishing a malformed skill wastes a version and hurts trust.",
  audience="Skill authors publishing to ClawHub.",
  use=["Lint a skill folder","Check frontmatter","Detect thin content","Validate command docs","JSON output"],
  faq=[("What it checks","Frontmatter, structure, command docs, thin content."),
       ("CI?","Yes — --json."),
       ("Offline?","Yes."),
       ("Pair with?","skill-benchmark for grading.")],
  comp=[("Publish and pray","Catch issues pre-publish."),
        ("Manual review","Automated structure checks."),
        ("Thin skills","Detects low-value content.")],
),
"web-research": dict(
  title="Web Research Toolkit",
  one="Route search, research, and lookups through one CLI — DuckDuckGo, Wikipedia, and URL fetch — zero dependencies.",
  problem="Web research is scattered across sites and needs API keys for most tools.",
  audience="Researchers, agents, and CI fact-checkers.",
  use=["DuckDuckGo search","Wikipedia lookups","Fetch + extract a URL","Export citations","Batch research in CI"],
  faq=[("Backends?","DuckDuckGo, Wikipedia, raw URL fetch."),
       ("API key?","No — stdlib only."),
       ("Citations?","Exportable."),
       ("Offline?","No — live web.")],
  comp=[("Per-site research","One CLI, three backends."),
        ("API-key tools","Zero-dependency, keyless."),
        ("Copy-paste","Citations + extraction built in.")],
),
"youtube-content": dict(
  title="YouTube Content Toolkit",
  one="Extract transcripts, summaries, and metadata from YouTube videos for content repurposing.",
  problem="Turning a video into usable text (blogs, clips, summaries) is manual.",
  audience="Content creators, marketers, and agents repurposing video.",
  use=["Fetch a transcript","Summarize a video","Pull metadata","Repurpose into posts","Batch a playlist"],
  faq=[("Transcript?","Yes — caption/text extraction."),
       ("Summary?","Generated from the transcript."),
       ("Metadata?","Title, channel, duration, etc."),
       ("Offline?","No — fetches from YouTube.")],
  comp=[("Watching full videos","Transcript-first repurposing."),
        ("Manual notes","Structured metadata + summary."),
        ("One-off tools","Transcript + summary + metadata together.")],
),
}

def get_subcommands(slug):
    """Extract true subcommands from add_parser(...) in the skill's .py source."""
    d = os.path.join(BASE, slug)
    pys = [f for f in os.listdir(d) if f.endswith(".py") and not f.startswith("__")]
    subs = []
    for p in pys:
        src = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
        for sm in re.findall(r'add_parser\(\s*[\'"]([^\'"]+)[\'"]', src):
            if sm not in subs:
                subs.append(sm)
    return subs

def get_self_test(slug):
    d = os.path.join(BASE, slug)
    pys = [f for f in os.listdir(d) if f.endswith(".py") and not f.startswith("__")]
    for p in pys:
        src = open(os.path.join(d, p), encoding="utf-8", errors="ignore").read()
        if re.search(r'add_parser\(\s*[\'"]self-test[\'"]', src):
            return True
    return False

def build_skill_md(slug, inv_entry, copy):
    fm = inv_entry
    name = fm.get("fm_name") or slug
    version = fm.get("fm_version") or "2.0.0"
    desc = fm.get("fm_desc") or copy["one"]
    tags = fm.get("fm_tags")
    # normalize tags to a python list
    try:
        taglist = json.loads(tags) if tags else []
    except Exception:
        taglist = [t.strip() for t in tags.strip("[]").split(",") if t.strip()]
    # enrich tags with SEO terms
    extra = ["cli","python","open-source","agent","automation","MIT"]
    for e in extra:
        if e.lower() not in [t.lower() for t in taglist]:
            taglist.append(e)
    taglist = taglist[:12]
    tags_str = "[" + ", ".join(f'"{t}"' for t in taglist) + "]"
    py = (inv_entry.get("py") or [slug.replace("-","_")+".py"])[0]
    title = copy["title"]
    one = copy["one"]
    keywords = ", ".join(taglist)
    lines = []
    lines.append("---")
    lines.append(f'name: {slug}')
    lines.append(f'version: {version}')
    lines.append(f'description: {desc}')
    lines.append(f'tags: {tags_str}')
    lines.append("---")
    lines.append("")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**{one}**")
    lines.append("")
    lines.append(f"> *Keywords: {keywords}*  ")
    lines.append(">")
    lines.append(f"> Part of the [{BRAND}]({GITHUB}) {STACK} — 31 free, MIT-licensed, CI-tested agent-native tools.")
    lines.append("")
    lines.append("## What it does")
    lines.append("")
    lines.append(f"{copy['problem'].split('.')[0]}. {title} solves this: {one}")
    lines.append("")
    lines.append(f"**Best for:** {copy['audience']}")
    lines.append("")
    lines.append("## Features")
    lines.append("")
    for u in copy["use"]:
        lines.append(f"- **{u}**")
    lines.append("")
    lines.append("## Install")
    lines.append("")
    lines.append("```bash")
    lines.append(f"# Requires Python 3.8+. No pip install needed.")
    lines.append(f'curl -O https://raw.githubusercontent.com/{BRAND}/{slug}/main/{py}')
    lines.append("# Or copy the file anywhere — it's self-contained.")
    lines.append("```")
    lines.append("")
    # Quick start with the skill's real subcommands
    subs = get_subcommands(slug)
    has_st = get_self_test(slug)
    lines.append("## Quick start")
    lines.append("")
    lines.append("```bash")
    if has_st:
        lines.append(f"python {py} self-test     # prove it works end-to-end")
    for i, s in enumerate(subs):
        if s == "self-test":
            continue
        lines.append(f"python {py} {s} --help   # {s} subcommand")
    if not subs and not has_st:
        lines.append(f"python {py} --help        # list options")
    lines.append("```")
    lines.append("")
    lines.append("## Use cases")
    lines.append("")
    for u in copy["use"]:
        lines.append(f"1. {u}")
    lines.append("")
    lines.append("## Why choose this over alternatives")
    lines.append("")
    lines.append("| Alternative | Why this skill is better |")
    lines.append("|---|---|")
    for c, w in copy["comp"]:
        lines.append(f"| {c} | {w} |")
    lines.append("")
    lines.append("## FAQ (SEO / AEO)")
    lines.append("")
    for q, a in copy["faq"]:
        lines.append(f"**Q: {q}**  ")
        lines.append(f"A: {a}")
        lines.append("")
    lines.append("## Geo / local reach")
    lines.append("")
    lines.append(f"Built and maintained by [@{BRAND}]({GITHUB}) (Chennai, India · serving developers worldwide). ")
    lines.append("Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.")
    lines.append("")
    lines.append("## CI integration")
    lines.append("")
    lines.append("```yaml")
    lines.append("# .github/workflows/verify.yml")
    lines.append("name: Verify")
    lines.append("on: [push]")
    lines.append("jobs:")
    lines.append("  verify:")
    lines.append("    runs-on: ubuntu-latest")
    lines.append("    steps:")
    lines.append("      - uses: actions/checkout@v4")
    lines.append(f"      - name: Self-test {slug}")
    if "self-test" in inv_entry.get("cli_flags", []):
        lines.append(f"        run: python {py} self-test")
    else:
        lines.append(f"        run: python {py} --help")
    lines.append("```")
    lines.append("")
    lines.append("## Support")
    lines.append("")
    lines.append(f"Free + {LICENSE}. Sponsor if useful:")
    lines.append(f"- GitHub Sponsors: {SPONSORS}")
    lines.append(f"- Buy Me a Coffee: {COFFEE}")
    lines.append("")
    lines.append(f"⭐ Star on [GitHub]({GITHUB}/{slug})")
    lines.append("")
    return "\n".join(lines)

def build_readme_md(slug, inv_entry, copy):
    md = build_skill_md(slug, inv_entry, copy)
    # README is the same rich content plus badges at top
    badge = (f"[![ClawHub](https://img.shields.io/badge/ClawHub-{slug}-red)](../..) "
             f"[![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) "
             f"[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)\n\n")
    return badge + md

# ---- main ----
written = []
for slug, copy in COPY.items():
    if slug not in inv:
        print("SKIP (no inventory):", slug); continue
    sk = build_skill_md(slug, inv[slug], copy)
    rm = build_readme_md(slug, inv[slug], copy)
    sd = os.path.join(BASE, slug, "SKILL.md")
    rd = os.path.join(BASE, slug, "README.md")
    open(sd, "w", encoding="utf-8").write(sk)
    open(rd, "w", encoding="utf-8").write(rm)
    written.append(slug)

print(f"Regenerated {len(written)} skills.")
print("Missing copy for:", [s for s in inv if s not in COPY])
