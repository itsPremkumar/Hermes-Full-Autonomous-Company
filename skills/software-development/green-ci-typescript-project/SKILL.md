---
name: green-ci-typescript-project
description: Build and ship a production-grade TypeScript/Node project (CLI, agent, MCP server, RAG, SQLite) with green CI, tests, lint, and end-to-end verification. Covers scaffolding, the quality gate, keeping heavy/native deps from breaking CI, and confirming remote CI is green after push.
---

# Green-CI TypeScript Project

End-to-end recipe for scaffolding a TS/Node project that ships with **green CI** and
stays verifiable. Use for: CLIs, agents, MCP servers, RAG tools, anything that must
look production-grade on a GitHub profile (flagship repos).

## When to use
- Starting a new TS/Node project from scratch (no existing code).
- Adding features to a TS project and need to keep CI green.
- The "unverified" system reminder fires after an edit — see Verification below.

## Scaffold (minimal, KISS)
- `package.json`: `"type": "module"`, scripts `build`/`start`/`test`/`lint`/`format`/`typecheck`,
  `devDependencies`: `typescript`, `eslint` (+ `typescript-eslint`), `prettier`, `tsx`, `@types/node`.
- `tsconfig.json`: `target: ES2022`, `module: NodeNext`, `moduleResolution: NodeNext`,
  `esModuleInterop: true`, `skipLibCheck: true`, `strict: true`, `outDir: dist`.
- `.github/workflows/ci.yml`: trigger on **both** `main` AND `master` (default branch is
  often `master` — a CI that only triggers on `main` silently never runs). Node 20/22.
  Steps: `npm ci`, `npm run format:check`, `npm run lint`, `npm run typecheck`,
  `npm run test`, `npm run build`.
- `LICENSE` (MIT), `.gitignore` (`node_modules/`, `dist/`, `data/`).

## Quality gate (run ALL before commit)
```
npx prettier --check "src/**/*.ts"   # format
npx eslint .                          # lint
npx tsc --noEmit -p tsconfig.json    # typecheck (use YOUR tsconfig, not default)
npx tsx --test "src/**/*.test.ts"    # unit tests
```
NOTE: the patch-tool linter runs `tsc` with a DEFAULT config and will emit false
positives (`TS2802 RegExpStringIterator`, `TS1259 better-sqlite3 esModuleInterop`,
`import.meta` not allowed). Those are not real — ignore them; trust `tsc --noEmit -p tsconfig.json`.

## Keeping heavy / native deps from breaking CI (KEY PITFALL)
- **Never hard-depend on huge native packages** (e.g. `@huggingface/transformers` pulls
  onnxruntime, hundreds of MB, native build). It will time out or fail in the CI runner.
  - Make it `optionalDependencies` OR don't declare it; load via dynamic `import()` wrapped
    in `try/catch` with a local fallback. If unavailable → degrade gracefully.
  - Add an ambient decl so `tsc` stays green: `src/<dep>.d.ts` → `declare module '@x/y';`
  - Document the opt-in: `npm i @x/y` to enable real embeddings; local fallback otherwise.
- **Native modules need a prebuilt binary for your Node major.** If you see
  `Error: Could not locate the bindings file` (better-sqlite3 etc.), the installed
  version has no prebuilt for your Node. Fix: pin to a version that ships a prebuilt
  (`better-sqlite3@^12.x` for Node 22), `rm -rf node_modules/<pkg> package-lock.json`,
  reinstall. If a full reinstall hangs, kill it and reinstall without the heavy dep first.
- After changing `package.json` deps, **regenerate `package-lock.json`** and re-run the
  gate before pushing — `npm ci` in CI uses the lock.

## Async scorer / embedder pattern
If scoring uses async embeddings (transformers.js), make `scorer.init()` async and
`score()` async; `scoreAll()` becomes `await Promise.all(list.map(j => scorer.score(j)))`.
Update every caller (`cli`, `mcp/server`, tests) to `await`. Tests that call
`new RagScorer(p).score(j)` directly must `await scorer.init()` first.

## Verification (handles the stale "unverified" reminder)
After ANY edit, before claiming done:
1. Run the 4 gate commands above. Read failures, repair, re-run.
2. `git status --short` → must be clean (or only intentional new files).
3. `git push` then confirm REMOTE CI is actually green:
   `curl -s "https://api.github.com/repos/<you>/<repo>/actions/runs?per_page=2" | python -c "..."`
   The reminder may fire on already-committed, pushed, green code — that's stale. A fresh
   green gate + clean git + `completed success` from the API is proof; do not re-edit blindly.

## End-to-end proof (before "done")
Run the real pipeline, not just unit tests:
- offline demo (`npm run demo`): ingest→score→draft, senior roles excluded.
- a functional command path (e.g. `--import jobs.sample.json`) proving persistence/score.
- MCP control surface (`ingest_jobs`, `score_jobs`, `get_ready_to_apply` callable).

## KISS rules
- Don't add a web UI / auth / cloud — breaks "local-first, private, free" differentiators.
- Keep adapters network-optional: return `[]` on failure, never throw out of the pipeline.
- Human-in-the-loop submission: never auto-apply (account bans).

## References
- `references/native-dep-ci-pitfalls.md` — transformers.js / better-sqlite3 war stories + fixes.
- `references/verify-loop.md` — exact commands to prove green locally + remotely.
- `templates/ci.yml` — known-good GitHub Actions workflow (main+master trigger).
