# Agentic Job-Hunt Copilot — project recipe

Built this session as a salary-boosting portfolio project for Premkumar M.
Demonstrates: agentic AI orchestration, RAG-lite scoring, MCP server, full-stack
TypeScript, green CI — the skills paid top in 2026.

## Concept
Local-first, agentic copilot: ingest FREE job boards -> RAG-lite fit-score vs.
resume+GitHub -> draft cover letters -> track state. Human submits manually.
NO spam, NO paid boards, NO login.

## Stack / structure (TypeScript, ESM, NodeNext)
```
src/
  types.ts        Job, CandidateProfile, ApplicationStatus
  config.ts       CopilotConfig (llmProvider: 'local'|'openai')
  store.ts        MemoryJobStore (swap for SQLite); jobId() hash helper
  llm.ts          LLM iface + LocalLLM (offline template) + OpenAiLLM (fetch)
  ingest.ts       IngestAdapter; RemoteOkAdapter (JSON API) + ManualAdapter
  scorer.ts       FitScorer: lexical overlap + seniority/salary signals
  coverLetter.ts  template or LLM-generated letter
  agent.ts        loop: ingest -> scoreAll -> draftTop(minScore) -> readyToApply
  mcp/server.ts   MCP stdio server (tools/call) exposing copilot to agents
  cli.ts          arg parser + pipeline run
  demo.ts         offline sample-job demo (no network)
.github/workflows/ci.yml   Node 22: format:check, lint, typecheck, test:unit
```

## Key implementation notes (reusable)
- **Offline LLM fallback:** `LocalLLM` returns templates so CI + private use need
  zero API key. Swap via `llmProvider:'openai'` + key. Don't hardcode `API_KEY=1`
  in scripts (breaks Windows + can't be overridden) — read env in code.
- **RAG-lite scoring:** tokenize profile+resume into term map; score each job by
  overlap + signals (remote +10, AI/ML +12, too-senior -12, salary band +10).
  Caps 0-100. No vector DB needed -> dependency-free, local-first.
- **MCP server:** minimal JSON-RPC over stdio; `tools/list` + `tools/call`.
  No SDK required. Good pattern to expose any tool to agents.

## Build/verify commands (Node 22)
```
npm install
npm run format      # prettier --write
npm run lint        # eslint .
npm run typecheck   # tsc --noEmit -p tsconfig.json
npm run test:unit   # tsx --test "src/**/*.test.ts"
npm run demo        # offline functional proof
```
tsconfig: `target ES2022, module NodeNext, moduleResolution NodeNext`.

## Pitfalls hit & fixed (capture these)
- `tsc` import paths: test in `src/` uses `./x.js`, mcp server in `src/mcp/` uses `../x.js`.
- `as Record<string,unknown>` on a typed object -> use `as unknown as Record<...>`.
- Implicit `any` param in default arrow fn -> annotate `(u: string)`.
- Unused imports cause eslint warnings -> keep imports tight.
- `patch` tool's inline linter may report false-positive TS errors (wrong default
  target). Trust `npx tsc --noEmit -p tsconfig.json` as source of truth.
- The auto-apply agent correctly EXCLUDED a "Senior Staff 10+ yrs" role — seniority
  penalty is the differentiator that makes it a product, not a spam bot.

## Why it moves salary
Shows agentic AI + RAG + MCP (2026 top-paid skills), production-grade (green CI,
tests, typed). Privacy-first/local angle is unique. Easy real beta users from
OSCG/OSCI network -> "used by N" = offer leverage.
