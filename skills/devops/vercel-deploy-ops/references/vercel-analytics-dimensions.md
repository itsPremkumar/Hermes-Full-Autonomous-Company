# Vercel Web Analytics via CLI — dimension names that actually work

`vercel metrics` reads the same Web Analytics the Vercel MCP does NOT expose (MCP is
OpenCode-only / OAuth; the CLI is the Hermes path). On the **free/Hobby** plan some
dimensions return empty even though the flag is accepted. Confirmed on sproutern
(2026-07-11, CLI v55, team `prems-projects-27978e99`):

## Metrics
- Pageviews: `vercel.analytics_pageview.count`
- Speed Insights (field data, 7d): `vercel.speed_insights.lcp_ms|fcp_ms|ttfb_ms|inp_ms|cls`
  (use `--since 7d`; values print on a separate line after the header — capture both)

## `--group-by` dimensions — WORKS
- `request_path` (top pages)
- `country` (ISO codes: IN, SG, US, ZA, CN)
- `device_type` only returns `desktop` reliably; mobile/tablet fold into `os`/`browser`

## `--group-by` dimensions — EMPTY / unsupported on free plan
- `os`, `operating_system` -> blank
- `referrer`, `referrer_host`, `referrer_hostname` -> blank
  (referrer/OS breakdown needs the paid plan or the dashboard)

## Command shape
```bash
vercel metrics vercel.analytics_pageview.count \
  --since 30d --project <name> --prod --scope <team-slug> \
  --group-by request_path --limit 10
# Speed:
vercel metrics vercel.speed_insights.lcp_ms --since 7d --project <name> --prod --scope <slug>
```
- `--project <name>` + `--prod` + `--scope <team>` are all required (no defaults).
- Total: same metric with no `--group-by` -> first numeric line is the sum.
- If output shows only the header and no value, the dimension returned empty (free-plan
  limit) -> fall back to `request_path`/`country`/`device_type`.

## Firebase-in-global-bundle case (sproutern 2026-07-11)
Symptom: homepage HTML has `<script src="/_next/static/chunks/firebase-*.js" async>`.
Two distinct cases:
1. **Static import in a globally-rendered module** (e.g. `notification-provider` in
   `layout.tsx` statically imports `firebase-messaging`, which had
   `import { db } from './firebase'` + `import {...} from 'firebase/firestore'`).
   Fix: make EVERY firebase entry dynamic inside the async fns that use it:
   `const { db, auth } = await import('./firebase');`
   `const { doc, setDoc, serverTimestamp } = await import('firebase/firestore');`
   Keep only `import type { FirebaseApp } from 'firebase/app'` etc. (erased at compile).
   Verify: `grep -nE "^import .* from 'firebase|(./firebase)'" src/lib/firebase-messaging.ts`
   -> only `import type` lines remain.
2. **`async` preload from a deferred dynamic import** (e.g. `analytics-provider` does
   `import('@/lib/firebase')` inside a 3s-delayed effect). Next auto-adds the chunk as
   `<script async>` -- NON-blocking, does NOT hurt LCP. Leave it; it's correct deferral.
   If the chunk hash is identical before/after your edit, your edit didn't touch this
   path (it's driven by the deferred importer, not the module you changed).

Chunk-hash trick: a changed chunk gets a NEW hash. If `firebase-<hash>.js` is identical
before and after your edit, your edit didn't alter that chunk's contents.
