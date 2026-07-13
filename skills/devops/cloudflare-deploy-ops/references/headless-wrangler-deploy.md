# Headless wrangler deploy — Windows / agent-terminal gotchas

Two failures hit when deploying OpenNext/Cloudflare Workers from a non-interactive agent shell
(observed on Windows 11 + msys bash, Node 22, wrangler 4.81):

## 1. "stdin is not a tty" (exit 1)
Repo deploy scripts that call `spawnSync(wrangler, [...], { shell: isWindows })` give wrangler a
non-TTY stdin; wrangler aborts before any upload. Symptom log ends with:
```
stdin is not a tty
DEPLOY_EXIT=1
```
`npm run deploy` / `node scripts/deploy-cloudflare-free.mjs` ONLY works in a real interactive
shell. From the agent terminal, **bypass the script and run wrangler directly**.

## 2. "Unable to resolve Cloudflare's API hostname" (IPv6-only DNS)
`curl https://api.cloudflare.com` → HTTP 403 (reachable), but wrangler `fetch` fails. The
sandbox returns only AAAA (IPv6) records for `api.cloudflare.com`; Node can't connect over v6.
Fix: `NODE_OPTIONS="--dns-result-order=ipv4first"`.

## Working headless recipe
```bash
cd /path/to/project
export CI=1
export NODE_OPTIONS="--dns-result-order=ipv4first"
# one worker:
node_modules/.bin/wrangler deploy --config cloudflare/wrangler.public.jsonc
# OR all 6 (run in background — public worker uploads 600+ assets, several minutes):
for c in cloudflare/wrangler.server-blog.jsonc \
         cloudflare/wrangler.server-tools.jsonc \
         cloudflare/wrangler.server-games.jsonc \
         cloudflare/wrangler.server-companies.jsonc \
         cloudflare/wrangler.server-misc.jsonc \
         cloudflare/wrangler.public.jsonc; do
  node_modules/.bin/wrangler deploy --config "$c" || echo "FAILED: $c"
done
```

## Notes / non-obvious points
- Do NOT use `wrangler deploy --yes` (v4.81 → `yargs: Unknown argument: yes`). `CI=1` is the
  correct non-interactive switch.
- Auth: `wrangler login` (browser OAuth, user does it once) OR `CLOUDFLARE_API_TOKEN` +
  `CLOUDFLARE_ACCOUNT_ID` env vars for fully headless.
- Asset upload is diff-based + auto-retries drops. A failed public-worker pass leaves the site
  LIVE (partial assets up). Re-run the same `wrangler deploy --config ...public.jsonc` to top up
  remaining assets; each pass converges to "Uploaded N of N assets".
- Success signature: `Uploaded sproutern (NNN sec)` → `Deployed sproutern triggers` →
  `https://<name>.<subdomain>.workers.dev` → `Current Version ID: <uuid>`.
- Verify after each pass: `curl -sS -m 25 -A "Mozilla/5.0" -o /dev/null -w "%{http_code}" https://<name>.<subdomain>.workers.dev/<route>` (HTTP 200 = good). Ignore curl's `write of NNN bytes` glitch on msys — that's a terminal write artifact, not a site failure.
