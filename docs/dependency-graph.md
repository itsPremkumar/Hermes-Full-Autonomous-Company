# Dependency Graph

Projects are NOT isolated. Before changing any node, check its dependents. The AI must
understand dependencies before editing. This is the living map.

```
Hermes-Full-Autonomous-Company (root / OS)
│
├── CONSTITUTION.md .................... governs ALL behavior (dep: nothing; depended-by: everything)
├── Paperclip server .................. the company runtime (dep: Postgres; depended-by: all agents)
│     ├── Hermes adapter .............. CEO bridge (dep: Paperclip API, Hermes)
│     ├── OpenClaw adapter ............ comms/computer-use (dep: Paperclip API)
│     └── Coding agents ............... Claude/Codex/Gemini (dep: Paperclip API)
│
├── income-engine/ .................... generates the products (dep: CONSTITUTION, templates)
│     └── gumroad/products/* .......... upload-ready packages (dep: income-engine; BLOCKED by: Gumroad account = human)
│
├── digital-products/ ................. 8 catalog products (dep: income-engine output)
│
├── revenue/ .......................... sales pages, funnels, blog (dep: digital-products, Gumroad URLs=human)
│
├── hermes-paperclip-adapter/ ......... source (dep: Paperclip API schema)
│
├── autonomy-loop.py .................. 24/7 cron brain (dep: GitHub, Paperclip issues, git CLI)
│
└── prompts/ ......................... prompt library (dep: CONSTITUTION §7; mirror: Hermes-Prompt-Library)

External runtime deps:
  Postgres (embedded) ── Paperclip
  OmniRoute→OpenRouter ── model escalation (dep: OPENROUTER_API_KEY in env, NEVER committed)
  OpenClaw gateway :18789 ── computer-use
```

## Rule
A change to any box propagates to its children. E.g. changing the Paperclip API schema
needs a matching change in `hermes-paperclip-adapter` AND a re-test of the autonomy loop.
Never edit a leaf without re-validating its parent's integration status in
tools/repo-index.md.
