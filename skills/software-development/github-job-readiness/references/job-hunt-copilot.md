# job-hunt-copilot — flagship agentic project pattern

A reusable, salary-moving project the user had built this session and published as a flagship.
Capture the *shape* (not the code) so future sessions can scaffold similar high-signal projects.

## Why it moves offers
Demonstrates the 2026 top-paid skills: **agentic AI orchestration + RAG-lite scoring + MCP
server + full-stack TypeScript + green CI**. Privacy-first/local angle differentiates it from
cloud spam tools. Easy to get real beta users from OSCG/OSCI networks → "used by N people" = leverage.

## Architecture shape (KISS, no external deps for core)
- `types.ts` — domain models (Job, CandidateProfile, ApplicationStatus).
- `store.ts` — dependency-free in-memory store (swap for SQLite/LevelDB via same interface).
- `llm.ts` — `LLM` interface + `LocalLLM` (offline, deterministic) + `OpenAiLLM` (fetch-based).
  Local mode lets CI + privacy-first runs work with NO API key.
- `ingest.ts` — free-board adapters (RemoteOK JSON API + manual add). Degrade gracefully;
  never scrape paywalled/login-gated boards.
- `scorer.ts` — legacy lexical `FitScorer` (overlap + seniority/salary signals). Keep as a
  fallback.
- `ragScorer.ts` — **REAL local-embedding RAG** (the upgrade that made it a credible flagship):
  `LocalEmbedder` builds a fixed-width TF-weighted bag-of-words vector over a vocab drawn from
  the candidate profile; score = **cosine similarity** (both vectors L2-normalized) + seniority/
  salary signals. Genuine dense-vector retrieval, 100% offline, no model download — demonstrably
  scores "semantic match 50%" vs the old flat 100. To use a real model later, swap `EmbedFn` for
  Ollama/`transformers.js`; the scorer body is unchanged.
- `sqliteStore.ts` — `SqliteJobStore` implements the same `JobStore`/`ProfileStore` interface as
  the in-memory version; persists jobs/scores/cover letters to a local `.db` so state survives
  across CLI runs (a daily-use tool, not a forgetful demo). Use `better-sqlite3` (prebuilt binary,
  no build tools) + `mkdirSync(dirname(dbPath),{recursive:true})` BEFORE `new Database()` (it won't
  create the parent dir and throws "Cannot open database because the directory does not exist").
  Add `@types/better-sqlite3` for tsc.
- `coverLetter.ts` — template draft in local mode; refine via LLM API (OpenAI) OR a **local
  OllamaLLM** (`ollama pull llama3` → `npm run start -- --llm ollama`) for free, offline, private
  generation. `OllamaLLM` hits `http://localhost:11434/api/chat`; degrade to template on failure.
- `agent.ts` — the agentic loop: ingest → score → draft → track. Human applies manually.
  `useRag` flag picks `RagScorer` vs `FitScorer`. Add a `listJobs()` passthrough + `status` CLI
  command so state is inspectable across runs.
- `mcp/server.ts` — MCP stdio server exposing `ingest_jobs`, `score_jobs`,
  `get_ready_to_apply` (JSON-RPC tools/list + tools/call). Lets other agents control it.
- `cli.ts` + `demo.ts` — one-command run; offline demo with seeded jobs.
- `*.test.ts` — node:test unit tests (scorer, store, cover-letter, full agent run).

## Quality gate (CI on Node 22)
`format:check` (prettier) · `lint` (eslint+typescript-eslint) · `typecheck` (tsc --noEmit) ·
`test:unit` (tsx --test). All must be 0-exit. Keep the same bar as their other flagships.
This project carries 10 unit tests (scorer, RAG embedder/cosine, SQLite persistence across
reopen, cover-letter, full agent run with RAG+SQLite).

## Pitfalls hit & fixed this session
- `tsconfig` `target: ES2022` required for `import.meta` + Map/RegExp iteration; the `patch`
  tool's linter uses a wrong default target and reports false TS2802/TS1343 — trust `tsc -p
  tsconfig.json`, not the inline linter.
- Test files sit in `src/` → import siblings with `./x.js` (not `../x.js`).
- MCP stdio: print `tools/list` handshake on startup, then read lines for `tools/call`.
- Default branch `master` → CI trigger must include `master` or it won't run.

## Publish (free, user-assisted)
`gh repo create <repo> --public --source . --push` after the user runs `gh auth login --web`
in their own terminal. Confirm via API (200, not 404). Add description via GitHub UI (API 401).
