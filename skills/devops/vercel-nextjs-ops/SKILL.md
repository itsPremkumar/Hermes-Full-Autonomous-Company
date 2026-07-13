---
name: vercel-nextjs-ops
description: Deploy, verify, and performance-tune Vercel-hosted Next.js (App Router) apps. Covers fixing build errors (ssr:false-in-Server-Component, revalidate-in-client-component), confirming ISR/code-splitting live, pulling Vercel analytics/speed data when the MCP OAuth can't be driven, and verifying changes with typecheck + live curl probes. Use whenever you edit a Vercel-deployed Next.js project and must prove the change works in production.
---

# Vercel + Next.js (App Router) Ops

## When to use
- You edited a Next.js app that deploys to Vercel and must verify the change.
- A Vercel deploy errored and you need the real cause (Hobby hides build logs).
- You must pull Vercel analytics / Speed Insights but the `mcp.vercel.com` MCP can't be driven (OAuth browser flow blocked in this session).
- Performance work: ISR, code-splitting, lazy-loading, CLS, LCP.

## Setup / access
- **Vercel CLI is the workhorse.** Authenticated CLI (`vercel` / `vercel ls` / `vercel metrics`) exposes the same account data the MCP wraps — PLUS Web Analytics + Speed Insights the MCP does NOT expose.
- **MCP OAuth cannot run in this Hermes session** (browser not signed in; OpenCode-only). Do NOT block on it. Use the CLI. Same team/scope.
- Team scope flag for all commands: `--scope <team-slug-or-id>` (e.g. `prems-projects-27978e99`). Project flag: `--project <name>`.

## Standard post-edit verification procedure
After ANY code edit, before claiming done, present a compact table:
| Check | Command | Result |
| TypeScript | `./node_modules/.bin/tsc --noEmit` (background) | exit 0 |
| ESLint | `./node_modules/.bin/eslint <files>` | exit 0 |
| Git state | `git status --short <files>` | clean |
| Live | `curl -I <prod-url>` | expected header |
A Hermes hook may also demand this ("[System: You edited code … unverified]") — answer it with fresh evidence, not a restatement.

## Deploy + verify loop
- Large projects: `tsc --noEmit` takes ~5 min; foreground terminal clamps at 60s → **always run typecheck in background** (`terminal(background=true, notify_on_complete=true)`) and read `/tmp/tsc_*.log`. The `wait`/`process` tools also clamp at 60s — poll the log file directly with a short `sleep 55` loop instead.
- **Vercel build is the real validator.** Local `next build` may FAIL in this env for reasons unrelated to your code: Next 16 defaults to Turbopack but a `webpack` config with no `turbopack` block throws a config-conflict error; the webpack path OOMs on 600MB+ dep trees. If local build can't run, push and let Vercel build — its READY status IS the proof.
- Builds take 7–12 min on Hobby. Watch with a background poller that greps `vercel ls <project>` for the newest deploy id and exits on `Ready`/`Error`. (See `scripts/watch_deploy.sh`.)
- Hobby hides build logs on error (`Logs are unavailable because deployment … ended in ERROR`). The build error surfaces as a **0ms build step** only via `vercel inspect` (also minimal on Hobby). Diagnose from the code, not the log.

## Live verification probes (no browser needed)
- **Cache-bust curl** to defeat CDN caching when re-checking a header: `curl -sI "https://site/path?v=$(date +%s%N)"`.
- **ISR confirmed:** first hit `X-Vercel-Cache: PRERENDER`, second `HIT`; `Cache-Control: public, max-age=<N>, stale-while-revalidate=<M>` matches `revalidate=N`.
- **CORS origin reflection:** `curl -sI -H "Origin: https://evil.example.net" <site>/api/embed` → header must equal that origin, NOT `*`.
- **Code-split confirmed:** fetch the page HTML, list its `/_next/static/chunks/*.js`, then grep each chunk for a UNIQUE string from the component you lazy-loaded (e.g. `ExitIntentPopup`'s copy "Interview Prep Kit"). If absent from all initial chunks → it's in a separate lazy chunk. (The component *name* appearing in `layout-*.js` is just the dynamic() reference — not the implementation.)
- **Global-vendor bloat:** grep the homepage's `vendor-*.js` for a lib (e.g. `RadarChart`). If present, that lib loads on EVERY page. Isolate it (see gotchas).

## Free-plan (Hobby) optimization playbook
When the user runs Vercel **FREE/Hobby permanently** (no Pro, no edge functions), the
optimization universe shrinks. Encode this so you NEVER suggest paid upgrades and ONLY
do what helps on Hobby.

**What HELPS on free (do these):**
- **ISR to mask cold-start TTFB** — the ONLY real LCP lever on Hobby. Add
  `export const revalidate = 86400` to Server-Component pages (static tools/calculators).
  Repeat visitors + Vercel CDN get pre-rendered HTML, skipping the cold server render.
  Verify: `X-Vercel-Cache: HIT`/`PRERENDER`. (Note: `Cache-Control` may show a smaller
  `max-age` than your `revalidate` — Vercel's edge applies its own floor; caching is still
  active, which is what matters.)
- **GEO / structured data** — the biggest *free* growth lever (more AI-search citations =
  more organic traffic). Close schema gaps (see GEO audit). Metadata is usually already
  covered; JSON-LD schema is the usual gap.
- **Asset hygiene** — confirm images are small (`next/image`, no `unoptimized`). Usually
  already fine; not the LCP culprit if largest asset < ~200KB.

**What does NOT help on free (do NOT attempt — wastes effort / risks regressions):**
- Vercel Pro / edge functions / Observability Plus — ruled out by plan.
- Shrinking framework (739KB) / vendor (1.25MB) chunks — inherent to Next.js + shadcn;
  unsafe to cut without a rewrite. ISR + code-splitting is the ceiling.
- Per-route profiling — needs Pro.

**Workflow:** user says "free plan only / do everything" → do ISR rollout (safe, scripted,
guarded against dynamic-request APIs: skip pages using cookies()/headers()/searchParams/
useSearchParams) + GEO schema gap, verify live, report. Do NOT re-list Pro as a recommendation.

## Next.js App Router GOTCHAS (cause real deploy errors — know these)
See `references/nextjs-app-router-gotchas.md` for full detail + repro. The two that burned real cycles:
1. **`export const revalidate` / `dynamic` route-segment config is INVALID in a `'use client'` file.** Build fails at 0ms with no useful log. Must live in a Server Component.
2. **`next/dynamic(..., { ssr: false })` is FORBIDDEN inside a Server Component** (Next 15/16). `layout.tsx` is a Server Component (renders `<html>`, exports `metadata`). Build errors. Fix: drop `ssr: false` — keep `dynamic()` for code-splitting; the `'use client'` widget still hydrates fine.
3. **Default `splitChunks` hoists all `node_modules` into one global `vendor` chunk loaded on every page** — even libs a page doesn't use (recharts landed on the homepage this way). Fix: add an explicit `cacheGroups` entry (higher priority than the catch-all `vendor`) AND `next/dynamic` the import.

## GEO / structured-data audits (AI-search visibility)
AI engines (ChatGPT/Gemini/Perplexia) cite pages with JSON-LD + clean extractable content.
Do NOT start by adding schema — AUDIT first. Full technique + the `speakable` trap + the
"don't build a parallel JSON-LD component" lesson: `references/geo-structured-data-audit.md`.
Key moves:
- **Coverage gap:** `grep -rl "getPageSEO\|getPageSchema" src/app` vs `ls src/app/tools` via
  `comm -23` → pages with NO metadata AND no schema. (sproutern: 78/100 tool pages uncovered.)
- **⚠️ FALSE-ALARM TRAP (burned a cycle):** metadata/schema for a CLIENT-component page
  lives in its sibling `layout.tsx`, NOT in `page.tsx`. A naive `grep page.tsx` for
  `export const metadata` / `application/ld+json` will report a huge "gap" that DOESN'T
  exist. ALWAYS scan BOTH `page.tsx` AND `layout.tsx` (and any `seo-utils` helper the
  layout calls, e.g. `generateMetadata`). Correct check: count files with the marker under
  the tool dir (`grep -rl "application/ld+json" src/app/tools --include=*.tsx`), then diff
  against the page list. sproutern: real gap was schema 26/100, NOT metadata (metadata was
  100/100 via layouts).
- **Client-page rule:** `export const metadata` / JSON-LD `<script>` is FORBIDDEN in a
  `'use client'` page file. For client pages, put metadata in the folder's `layout.tsx`
  (layouts may export `metadata`/`generateMetadata`) and put the JSON-LD `<script>` inside
  that `layout.tsx` JSX (inject before `return children;` or `return <>{children}</>`).
- **`speakable` trap:** global JSON-LD may name `cssSelector: ['.faq-answer',...]` but if 0
  pages render those classes, the signal is dead. Grep to confirm; reuse the existing AEO
  component instead of inventing markup.
- **Parallel-component trap:** if a centralized SEO module (`complete-page-seo.ts`) already
  owns schema, extend IT — don't add a `<ToolJsonLd>` helper (duplicate/conflicting `@graph`).
- **Scale gate:** closing a 78-page gap = writing real per-tool titles/descriptions. Use
  `clarify` to pick scope; guessed mass-metadata can hurt GEO. Quality > coverage.
- **Sitemap gap may be INTENTIONAL noindex, not a bug.** Fewer sitemap URLs than route dirs
  is often a deliberate `NOINDEX_*_SLUGS` policy ("thin pages excluded until content added").
  Before "fixing" it, `grep -rn "noindex\|shouldIndexPath" src/lib/seo src/app`. The real win
  is to EARN indexation: add unique editorial content (reusable `<ToolEditorial slug>` +
  a `Record<slug,{intro,useCases,faqs}>` data file wired into each tool's layout), THEN clear
  the noindex set. Full scripted rollout (handles client/server pages, 'use client' line-1
  rule, idempotent guard) + live verify: `references/thin-page-indexing.md`.
- **Verify coverage at scale:** `scripts/verify_freeplan.sh <base-url> <tool-slugs-file>`
  prints which tool pages return `X-Vercel-Cache: HIT` and which emit `"@type":"WebApplication"`.

### Ads / CLS finding (Vercel Hobby + ad network)
- **Ad review mode:** if `NEXT_PUBLIC_ADSENSE_REVIEW_MODE` is unset, `process.env.X !== 'false'`
  defaults to TRUE → ad placeholder components `return null` → **ads do NOT render on prod**
  (CLS reservation / monetization both inert). Check this before "fixing" CLS — the slots may
  simply be off. Verify with `vercel env ls <project> --scope <team>` + `grep` the code path.
- **CLS reservation is safe + additive:** giving an ad placeholder a reserved `min-height`
  (per slot: 280px/600px) stops Ezoic iframe injection from shifting layout. It engages
  automatically when ads go live; harmless while in review mode.

## Pulling Vercel data via CLI (MCP replacement)
See `references/vercel-metrics-probes.md`. Key commands:
- Pageviews: `vercel metrics vercel.analytics_pageview.count --since 30d --project X --prod --scope T`
- Top paths: `… --group-by request_path --limit 10`
- Speed: `vercel metrics vercel.speed_insights.lcp_ms --since 7d --project X --prod --scope T` (also fcp_ms, ttfb_ms, inp_ms, cls)
- Note: `referrer` / `operating_system` dimensions are NOT exposed on the free plan's Web Analytics.

## Verification gate (Hermes hook)
When you see "[System: You edited code … Verification status: unverified", run fresh lint + typecheck (background) + live probe, then a table. This hook re-fires on stale turns where you only ran verification — answer each time with NEW evidence; do not claim "already verified" without re-running.

## Support files in this skill
- `references/nextjs-app-router-gotchas.md` — revalidate-in-client, ssr:false-in-Server-Component, global-vendor bloat; full repro + fixes.
- `references/vercel-metrics-probes.md` — exact CLI commands for pageviews/speed/headers (MCP replacement).
- `references/geo-structured-data-audit.md` — coverage-gap grep recipe, `speakable` trap, parallel-component trap, GEO scale gate, ad review-mode/CLS notes.
- `references/thin-page-indexing.md` — turn intentionally-noindexed thin tool pages into indexable ones: diagnose intentional noindex, build reusable `<ToolEditorial>` + content data file, scripted per-tool wiring (client+server pages), clear noindex set, verify sitemap/robots live.
- `scripts/watch_deploy.sh <project> [scope]` — polls `vercel ls` until the newest deploy is Ready/Error (use instead of the 60s-clamped `wait`/`process` tools).
- `scripts/verify_freeplan.sh <base-url> <slugs-file>` — for each tool slug: checks `X-Vercel-Cache: HIT/PRERENDER` (ISR) AND `"@type":"WebApplication"` schema presence; prints PASS/FAIL + counts. Use after an ISR + GEO-schema rollout to prove coverage at scale.
