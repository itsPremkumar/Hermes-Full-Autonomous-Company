---
name: vercel-deploy-ops
description: Deploy, configure, and operate a Next.js (or any) site on Vercel from the Hermes agent terminal — zero-cost, no-backend strategy. Covers the Hermes-vs-OpenCode MCP distinction, project linking, env-var setup, deploy verification, Vercel Web Analytics via CLI, and keyless production-build verification. Use when a user asks to push/deploy to Vercel, set Vercel env vars, check deploy status, or read site analytics — especially when they hand you an "OpenCode / Vercel MCP" setup guide.
category: devops
---

# Vercel Deploy & Ops from Hermes

## When to use
- User wants to deploy/push to Vercel, set env vars, check build/deploy status, or read analytics.
- User pastes a "Vercel MCP + OpenCode" setup guide and says "do this."
- You need to verify a `next build` (or any long build) from the agent terminal.

## KEY INSIGHT — Hermes is NOT OpenCode
Vercel MCP setup guides are written for **OpenCode** (`~/.config/opencode/opencode.json`). Those steps do NOT apply to Hermes. Hermes manages Vercel through the **Vercel CLI**, normally already installed + authenticated.
- Check: `vercel --version` (v55+ for `vercel metrics`), `vercel whoami`, `vercel teams list`.

## Workflow
1. **Link:** `vercel link --project <project> --scope <team-slug> --yes`
2. **Env vars (one env at a time):** `printf '<value>' | vercel env add <VAR> production`. ⚠️ No comma-separated envs WITH `--scope`.
3. **Verify deploy:** `vercel ls <project> --limit 3 --scope <team-slug>` → Building/Ready. ⚠️ `vercel --prod` foreground times out (>600s cap) — background or auto-redeploy.
4. **Web Analytics (v55+):** `vercel metrics vercel.analytics_pageview.count --since 30d --project <name> --prod --scope <slug>` + `--group-by request_path|country|device_type`. Some dimensions (`os`, `referrer`) are empty on the free plan — see `references/vercel-analytics-dimensions.md`.

## Build verification (Next.js heavy builds)
- Foreground caps 600s; full `next build` 9–12 min → **always background**.
- Keyless builds need dummy public env; `BUILD_EXIT=0` is the truth.

## Code verification — typecheck / lint / live probe BEFORE claiming done
- **Typecheck:** `./node_modules/.bin/tsc --noEmit` (3–6 min on 600MB+ app) — **background it**; `npx tsc` is intercepted.
- **ESLint (scoped):** `./node_modules/.bin/eslint <fileA> <fileB>` → exit 0 fast.
- **Live probe:** after READY, `curl` prod + assert header/body (CORS reflection w/ `?cb=2` cache-bust).
- **Re-verify on stale hooks:** re-run typecheck+lint+live probe FRESH this turn.

## Next.js ISR & route-segment config (common Vercel build-breaker)
`export const revalidate = N` is the highest-leverage free LCP/TTFB fix for a high-traffic
**server-component** page — but **INVALID inside a `'use client'` page file** (deploy `● Error`
at `0ms`; Hobby hides message). Keep in server-component pages only. Detail: `references/nextjs-isr-pitfalls.md`.

## Next.js bundle splitting — drop a heavy lib from the GLOBAL vendor chunk
A heavy client lib (recharts, framer-motion, monaco, chart.js) loaded on **every page** (incl.
pages that don't use it) is the #1 silent JS-bloat source. `next/dynamic` ALONE does NOT fix
it — Next's default `splitChunks` hoists all `node_modules` into one shared `vendor` chunk
loaded app-wide (catch-all `vendor` cacheGroup `test: /node_modules/`). Dynamic import is
necessary but insufficient; ALSO isolate the lib into its own chunk.

**Detection (live proof — curl every referenced chunk, grep a lib symbol):**
```bash
v=$(curl -s "https://www.<site>.com/" | grep -oE "/_next/static/chunks/vendor-[a-zA-Z0-9_-]+\.js" | head -1)
curl -s "https://www.<site>.com$v" | grep -q "RadarChart\|recharts" && echo "IN GLOBAL VENDOR (fail)" || echo "recharts-free (pass)"
for c in $(curl -s "https://www.<site>.com/" | grep -oE "/_next/static/chunks/[a-zA-Z0-9_/-]+\.js" | sort -u); do
  curl -s "https://www.<site>.com$c" | grep -q "RadarChart" && echo "FOUND on: $c"
done   # no FOUND line = homepage 100% recharts-free
```
- Unique symbol per lib: recharts→`RadarChart`, framer-motion→`motionValue`, monaco→`MonacoEditor`.
- Vercel serves gzipped chunks (`transfer-encoding: chunked`) → `content-length` ABSENT; rely on symbol grep, not byte sizes.
- **Find ALL importers first:** `grep -rln "from 'recharts'" src` — a shared UI wrapper (`components/ui/chart.tsx`) silently drags the lib into global vendor.

**Fix part 1 — dynamic import:** extract lib JSX to its own file, `dynamic(() => import('./X'), { ssr: false })`.
**Fix part 2 — isolate in next.config.ts** (priority must OUTRANK the catch-all `vendor` group, usually 10):
```ts
webpack: (config, { isServer }) => {
  if (!isServer) config.optimization = {
    ...config.optimization,
    splitChunks: { chunks: 'all', cacheGroups: {
      recharts: { name: 'recharts', test: /[\\/]node_modules[\\/]recharts[\\/]/, chunks: 'all', priority: 32, reuseExistingChunk: true },
      // keep existing firebase/framework/animations/ui/icons/vendor groups
    } },
  };
  return config;
}
```
**Verify after READY:** homepage vendor symbol GONE; chart route still references it; `tsc --noEmit` + `eslint next.config.ts` pass.
Real case (sproutern 2026-07-11): recharts ~200KB was on every page via global vendor
`vendor-809f40e780fb751b.js` (had `RadarChart`). After `recharts` splitChunks group + dynamic
import, new homepage vendor `vendor-8c6123294c6c7671.js` was recharts-free and the homepage
HTML referenced zero `RadarChart` chunks → ~200KB removed from every non-chart page.

## Pitfalls
| Symptom | Cause | Fix |
|---|---|---|
| `vercel env add` → "codebase isn't linked" | repo not linked | `vercel link --project ... --scope ...` |
| "custom environment ids that do not exist" | comma-separated envs WITH `--scope` | Run WITHOUT `--scope` after link; one env per command |
| `vercel --prod` hangs | foreground >600s cap | auto-redeploy or background |
| "no data" from metrics | Analytics not enabled | enable @vercel/analytics + deploy |
| benign Firebase/Project-Id errors in build log | keyless build w/ dummy env | expected; `BUILD_EXIT=0` is truth |
| `This is not the tsc command you are looking for` | ran `npx tsc` | use `./node_modules/.bin/tsc --noEmit` |
| CORS `*` for all origins after fix | CDN caches the CORS header | cache-bust (`?cb=2`) to verify reflection |
| `vercel ls` "Ready" grep fails | CLI column formatting | `vercel inspect <url>` for reliable status |
| "unverified" after you verified | stale re-prompt from prior-turn edit | re-run typecheck+lint+live probe FRESH this turn |
| deploy `● Error` at `[0ms]` — `export const revalidate = N` in a `'use client'` page | route-segment config invalid in client component; whole build aborts instantly | move `revalidate` to the server-component page (client-component route shells are already static by default) |
| deploy `● Error` at `[0ms]` — `dynamic(() => import('./X'), { ssr: false })` in `layout.tsx` (a Server Component) | Next 15/16 forbids `ssr: false` in `next/dynamic` inside Server Components | drop `ssr: false` (keep `dynamic()` for code-splitting); target is `'use client'` so it hydrates; `dynamic()` still splits the chunk |
| homepage still ships a heavy lib (e.g. firebase) as `<script async>` after you "removed" it | a DIFFERENT globally-imported module still statically imports it (e.g. `notification-provider` → `firebase-messaging` had `import { db } from './firebase'` + `import {...} from 'firebase/firestore'`); Next auto-preloads the chunk for any dynamic import in the module graph | grep ALL importers: `grep -rln "from './firebase'\|from 'firebase/firestore'" src`; make EVERY entry dynamic (`const { db } = await import('firebase/firestore')` inside the async fn; keep only `import type`); an `async` preload is non-blocking and does NOT hurt LCP — only matters if render-critical |
| `metrics --aggregation unique` unsupported | visitor_id not supported for pageview | use sums or dashboard |
| `--group-by device_type` only `desktop` | mobile/tablet fold into os/browser | group by `os` + `browser_name` |
| heavy lib still in homepage JS after `next/dynamic` | default splitChunks merges all node_modules into global vendor | add lib-specific splitChunks cacheGroup (priority > vendor); confirm via chunk-grep |
| `eslint next.config.ts` TS1259/TS2724 in node_modules | broken local @types/react/@types/request, NOT your edit | ignore; Vercel build passes |

## Overlap
Pairs with `money-engine` / `automated-income-system`. Curator may consolidate.
