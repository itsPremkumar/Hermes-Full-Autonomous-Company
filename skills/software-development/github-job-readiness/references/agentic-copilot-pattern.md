# Agentic Job-Hunt Copilot — Build Pattern

A repeatable shape for a **salary-moving portfolio project**: an agentic job-hunt
copilot that ingests free boards, scores fit with local RAG, drafts cover letters,
and persists state — all local-first, human-in-the-loop on submission.

## Why this class of project moves offers
Demonstrates the 2026 paid skills without buzzwords: **agentic AI orchestration,
real RAG (embeddings + cosine), local LLM integration, MCP, SQLite, green CI.**

## Architecture (verified working)
```
src/
  types.ts        domain models
  config.ts       provider (local|ollama|openai), useRag, minFitScore
  store.ts        JobStore/ProfileStore interfaces (in-memory impl)
  sqliteStore.ts  SQLite impl — PERSISTENCE across runs
  llm.ts          LocalLLM | OllamaLLM | OpenAiLLM (isLocal flag)
  ingest.ts       RemoteOK JSON adapter (fragile) + ManualAdapter
  scorer.ts       lexical FitScorer (legacy)
  ragScorer.ts    LocalEmbedder + RagScorer (cosine over dense vectors)
  coverLetter.ts  template (local) or real LLM (ollama/openai)
  agent.ts        ingest -> score -> draft -> track loop
  mcp/server.ts   MCP stdio server (agent-controllable)
  cli.ts          run | status | import
```

## Real offline RAG (no model download, no deps)
`LocalEmbedder` builds a fixed-width vocabulary from the candidate profile, embeds
each text as a **TF-weighted bag-of-words vector**, L2-normalizes it, and ranks by
**cosine similarity**. Genuine vector retrieval (dense vectors + cosine), runs fully
offline. Swap `EmbedFn` for a real model (Ollama / transformers.js) without touching
the scorer. Advertise honestly as "local-embedding RAG (TF-weighted)", not a
transformer embedding — reviewers will ask.

## Persistence (SQLite)
`better-sqlite3` behind the `JobStore` interface.
- **MUST `mkdirSync(dirname(dbPath), {recursive:true})` before `new Database()`** or
  it throws "Cannot open database because the directory does not exist".
- Install `@types/better-sqlite3` (tsc needs the .d.ts). Prebuilt binary installs on
  Windows with no native build tools.
- Different CLI subcommands should reuse ONE db path (e.g. `./data/jobs.db`) so
  `--status` sees what `--run` ingested. Demo can use a separate `demo.db`.

## Offline LLM (Ollama)
`OllamaLLM` POSTs to `http://localhost:11434/api/chat`. Free, private, no API key.
Falls back to the template letter on any error. `coverLetter.generate` checks
`llm.isLocal` — template when true, real generation otherwise (with `|| template`
guard on empty response).

## Ingestion reality (IMPORTANT — saves a wasted session)
**Live job boards are NOT reachable from the agent sandbox:**
- RemoteOK API → HTTP 302 (redirect/blocked); `fetch` adapter doesn't follow.
- Wellfound → 403 (DataDome anti-bot).
- Naukri / LinkedIn / RemoteAI → JS-rendered, unscrapable via Jina/DDG here.

So the copilot cannot *auto-pull* live jobs inside the agent environment. Practical
flow:
1. Build an `--import` CLI command that reads a JSON file (array OR NDJSON) and runs
   score+draft on it.
2. The USER pastes real listings they found (or a screenshot) into `jobs.import.json`;
   the agent formats them and runs the pipeline.
3. Copilot scores, drafts cover letters, shows top fits; **user clicks Apply** on the
   free board. No bot, no ban.

Verify board reachability with `curl -sI -L <url>` BEFORE assuming live ingest works —
don't loop on a 302/403.

## CI / publish
- Trigger on `[main, master]` (default branch may be `master` → `[main]` alone yields
  0 runs).
- After push, confirm via API: `curl .../actions/runs` → `runs: 1, conclusion:
  success`. Confirm repo exists (200, not 404) before claiming "published".
- Device-code `gh` flow must run in the USER's terminal (agent shell kills background
  interactive auth). Download official `gh` Windows zip — NOT `npm i -g github-cli`.
