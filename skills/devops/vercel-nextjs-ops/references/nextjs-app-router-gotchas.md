# Next.js App Router — gotchas that break Vercel deploys

Three issues cost real deploy cycles this session. All produce a Hobby build error
with NO useful log (the build step shows `[0ms]`). Diagnose from the code, not the log.

## 1. `revalidate` / `dynamic` route config is invalid in a `'use client'` file
- **Symptom:** deploy errors, build step `[0ms]`, `vercel inspect` shows nothing useful.
- **Why:** `export const revalidate = 300` and `export const dynamic = 'force-static'`
  are ROUTE SEGMENT CONFIG — read from the *module*, but only valid in Server Components.
- **Repro that failed:**
  ```tsx
  'use client';
  export const revalidate = 300; // ❌ build error
  export default function DateCalculatorPage() { ... }
  ```
- **Fix:** put `revalidate` only in Server Component page files. Existing correct usages
  in the repo: `src/app/page.tsx`, `src/app/blog/[slug]/page.tsx`.
- **Client-component pages:** their shell is already static; ISR belongs on the
  server-module page. For a client page, don't add `revalidate` — instead dynamic-import
  the heavy child (see #3).

## 2. `next/dynamic(..., { ssr: false })` forbidden in a Server Component
- **Symptom:** deploy errors after adding `dynamic(Comp, { ssr: false })` in `layout.tsx`.
- **Why:** Next 15/16 disallows `ssr: false` inside `next/dynamic` when the file is a
  Server Component. `layout.tsx` IS a Server Component (it renders `<html>` and exports
  `metadata`), so this throws at build.
- **Repro that failed:**
  ```tsx
  // layout.tsx (Server Component)
  const ShareWidget = dynamic(() => import('.../ShareWidget'), { ssr: false }); // ❌
  ```
- **Fix:** drop `ssr: false`. `dynamic()` alone still code-splits the component. The
  widget is already `'use client'`, so it hydrates correctly even when SSR'd:
  ```tsx
  const ShareWidget = dynamic(() => import('.../ShareWidget').then(m => m.ShareWidget));
  ```
- **Confirm safe:** ensure the widget has no module-level `window`/`document` access
  (outside useEffect). If it does, wrap it in a tiny `'use client'` wrapper that does
  the `dynamic(..., { ssr: false })` — that wrapper is a client component, so ssr:false
  is allowed there.

## 3. Default `splitChunks` hoists libs into one global `vendor` chunk (page-agnostic)
- **Symptom:** a heavy lib (recharts ~200KB) loads on EVERY page including the homepage
  that doesn't use it → bloats initial JS, hurts LCP.
- **Why:** the catch-all `vendor` cacheGroup (`test: /node_modules/`) grabs everything,
  and `chunks: 'all'` + `reuseExistingChunk` merges it into the global chunk.
- **Fix (two parts):**
  1. `next/dynamic` the import so it's not a static dependency of the route entry.
  2. Add an explicit `cacheGroups` entry with priority ABOVE the catch-all vendor:
     ```js
     recharts: {
       name: 'recharts',
       test: /[\\/]node_modules[\\/]recharts[\\/]/,
       chunks: 'all',
       priority: 32, // > vendor(10), < firebase(40)
       reuseExistingChunk: true,
     },
     ```
- **Verify live:** `curl` the homepage, find its `vendor-*.js`, grep for `RadarChart`.
  Before fix: present. After fix: absent → homepage no longer downloads recharts.

## Local build cannot run in this env (do NOT treat as a code error)
- Next 16 defaults to Turbopack; if `next.config.ts` only has `webpack` (no `turbopack`
  block), `next build` errors: "using Turbopack, with a `webpack` config and no
  `turbopack` config". Pass `--webpack` to match Vercel.
- The `--webpack` path OOMs (exit 134 / SIGABRT / V8 heap crash) on 600MB+ dep trees.
- **Conclusion:** Vercel is the real build validator. Push and watch the deploy.
