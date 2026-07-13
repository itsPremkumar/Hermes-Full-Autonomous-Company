# Next.js ISR & route-segment-config pitfalls (Vercel deploy)

## 1. `export const revalidate` / `dynamic` is INVALID in a `'use client'` page file
**Symptom:** `vercel ls` shows the new deploy as `● Error` with the build step at `[0ms]`
(infra hides the real error on Hobby). The build fails almost instantly — NOT a slow compile.

**Cause:** Route segment config exports (`revalidate`, `dynamic`, `dynamicParams`) are read
from a **server-component** module. Putting `export const revalidate = N` after the
`'use client';` directive in a page file makes Next.js reject the build.

**Fix:** Keep `revalidate` only in **server-component** pages (those that import from `next`
at the top and have no `'use client'`). Client-component route shells are already static by
default, so they don't need (and can't take) `revalidate`.

```ts
// server component - revalidate works
import { Metadata } from 'next';
export const revalidate = 300;   // ISR: prerender + revalidate every 5 min
export default function Page() { ... }

// 'use client' - causes deploy ERROR (0ms build)
'use client';
export const revalidate = 300;   // INVALID HERE
```

**Verify after deploy (the real proof ISR works):**
```
curl -sI "https://www.<site>.com/tools/<page>?v=<ts>" | grep -iE "x-vercel-cache|cache-control"
# first hit:  X-Vercel-Cache: PRERENDER   (served prerendered shell, no SSR cold start)
# later hits: X-Vercel-Cache: HIT
# Cache-Control: public, max-age=300, stale-while-revalidate=3600   (matches revalidate=300)
```

**Where it helps most:** high-traffic *server-component* pages. In sproutern,
`/tools/gpa-converter` (#1 page, ~10.6% of traffic) got `revalidate=300` -> its TTFB/LCP
cold-start is eliminated. Client tools (`exam-countdown`, `date-calculator`) were reverted.

## 2. `vercel metrics` dimension gotchas
- **`--aggregation unique` for pageviews:** requires `--group-by unique/visitor_id`, and that
  dimension is **NOT supported** for `analytics_pageview` -> error
  `"unique" in query groupBy is not a supported dimension`. Use pageview sums or the dashboard.
- **`--group-by device_type` returns only `desktop`** for many sites — mobile/tablet fold into
  OS/browser breakdowns. Estimate mobile share via `os_name` (Android + iOS) and `browser_name`
  (Chrome Mobile + Mobile Safari + Chrome Webview).
- **`vercel metrics schema --project X` errors** (`unknown option: --project`). Schema listing
  isn't per-project; run metric queries directly with `--project <name> --prod --scope <slug>`.
- **Speed Insights metric names:** `vercel.speed_insights.lcp_ms` (not `.lcp`), `.fcp_ms`,
  `.cls`, `.inp_ms`, `.ttfb_ms`. Hobby plan limits field data to **7 days**.

## 3. Deploy-error triage when logs are hidden (Hobby)
Hobby blocks build logs on errored deploys (`vercel logs` -> "Logs are unavailable because
deployment ... ended in ERROR"; `vercel inspect` shows only `status ● Error` + `[0ms]` build).
Triage by elimination:
- 0ms build = a **config/parse error**, not a compile. Likely a bad route-segment export (see 1),
  a bad `next.config` value, or an unsupported export in a client file.
- Diff the last good deploy's commit vs the failing one; the delta is your suspect.
- Revert the suspect, redeploy. If READY, diagnosis confirmed.
