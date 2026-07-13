# Native / heavy dependency CI pitfalls (from job-hunt-copilot build)

## @huggingface/transformers (transformers.js)
- Huge package (~hundreds of MB) + pulls native `onnxruntime-node` → native build.
- Symptom in CI: `npm ci` times out or the run fails with `Lint, Typecheck, Test failure`.
- Fix applied:
  1. Remove from `dependencies`. Either make it `optionalDependencies` OR don't declare it.
  2. Load via dynamic `import('@huggingface/transformers')` inside `try/catch`.
  3. On catch → fall back to a dependency-free embedder (LocalEmbedder: TF-weighted bag-of-words + cosine). The pipeline still does real vector RAG, just simpler vectors.
  4. Add `src/huggingface.d.ts`: `declare module '@huggingface/transformers';` so `tsc` (with `skipLibCheck`) stays green — its shipped `.d.ts` references unresolved `@utils`/`@static` modules.
  5. Document opt-in: `npm i @huggingface/transformers` enables real MiniLM embeddings.
- The model is also NOT downloaded at install — only at runtime, and needs network. CI
  never has it, so the fallback path is what runs in CI. Good.

## better-sqlite3 — "Could not locate the bindings file"
- Symptom: `Error: Could not locate the bindings file. Tried: .../build/better_sqlite3.node`
- Cause: installed version has no prebuilt binary for the running Node major (Node 22 here),
  and `npm install` didn't compile one.
- Fix: pin a version that ships a prebuilt for your Node (here `better-sqlite3@^12.11.1`).
  Then `rm -rf node_modules/better-sqlite3 package-lock.json` and `npm install`.
- If a full `npm install` hangs (re-resolving a large optional dep), `pkill -f "npm install"`
  then install without the heavy dep first.

## General rule
- Heavy/native deps: keep them OPTIONAL + runtime-tried + graceful fallback. CI must never
  depend on them being installed or built.
- Always regenerate `package-lock.json` after dep changes; `npm ci` in CI uses it.
