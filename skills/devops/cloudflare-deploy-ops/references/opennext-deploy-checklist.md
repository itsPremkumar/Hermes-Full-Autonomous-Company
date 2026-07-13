# OpenNext → Cloudflare deploy checklist

Condensed from the `sproutern-cloudflar` repo (Next.js 16 + OpenNext + Cloudflare Workers).

## Required files in repo
- `wrangler.jsonc` (root) — main worker: `main: .open-next/worker.js`, `assets.directory: .open-next/assets`, `compatibility_flags: ["nodejs_compat"]`, `services: [{binding: WORKER_SELF_REFERENCE, service: <name>}]`.
- `open-next.config.ts` — `defineCloudflareConfig({...})`, optionally `functions` for route-split Workers.
- `next.config.ts` — must call `initOpenNextCloudflareForDev()` and often sets `typescript.ignoreBuildErrors: true`.
- `cloudflare/wrangler.*.jsonc` — per-split-worker configs (public/blog/tools/games/companies/misc). Public worker binds to each sub-worker via `services[].binding` → `sproutern-server-<x>`.

## Build command
`npm run build:cloudflare` → runs `next build --webpack` + `opennextjs-cloudflare build --skipNextBuild` + route-group/feed generation. Output: `.open-next/`.

## Required env vars (at build time)
Public Firebase keys from `.env.local` are read by `next build`:
- `NEXT_PUBLIC_FIREBASE_API_KEY`, `NEXT_PUBLIC_FIREBASE_PROJECT_ID`, `NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN`, `NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET`, `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`, `NEXT_PUBLIC_FIREBASE_APP_ID`, `NEXT_PUBLIC_FIREBASE_VAPID_KEY`.
- `SERVICE_ACCOUNT_KEY` — base64-encoded Firebase admin JSON (server routes / dynamic sitemap data).

If `.env.local` already has real values, the build will compile. Verify presence:
`grep -c "NEXT_PUBLIC_FIREBASE_API_KEY=.\{10,\}" .env.local`

## Deploy command
`npm run deploy` → `scripts/deploy-cloudflare-free.mjs` loops `wrangler deploy --config <each cloudflare/wrangler.*.jsonc>`.

## Auth (choose one)
- Headless: `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` exported.
- Interactive: `npx wrangler login` (browser), persists to `~/.wrangler/config.json`.

## Post-deploy
- `npm run preview` for local Worker test.
- `wrangler tail` to stream logs.
- Verify `*.workers.dev` or custom domain responds 200.
