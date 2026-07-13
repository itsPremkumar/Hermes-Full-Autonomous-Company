# Cloudflare MCP server (`@cloudflare/mcp-server-cloudflare`)

## Package
`@cloudflare/mcp-server-cloudflare` (Cloudflare official). ESM, bin `dist/index.js`.

## CRITICAL — it needs a subcommand
`npx @cloudflare/mcp-server-cloudflare` with **no subcommand** throws:
`Error: Unknown command: undefined. Expected 'init' or 'run'.`
You MUST pass `run [account_id]` (or `init [account_id]` to re-auth):
```
npx -y @cloudflare/mcp-server-cloudflare@latest run <ACCOUNT_ID>
```

## Auth — reuses `wrangler login` automatically (no token needed)
The server reads auth from (in order):
1. `process.env.CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID`, OR
2. Falls back to the local wrangler config via `getAuthTokens()` ->
   `%APPDATA%\xdg.config\.wrangler\config\default.toml`
   (keys: `oauth_token`, `refresh_token`, `scopes`, `expiration_time`).

So if the user already ran `npx wrangler login` (OAuth in browser), the MCP server authenticates
with **zero extra setup**. On start you'll see:
`[DEBUG ...] Config loaded: {"accountId":"✓","apiToken":"✓"}`
If the token is expired it auto-refreshes via the `refresh_token`.

Passing `run <ACCOUNT_ID>` explicitly also sets `config.accountId` and the server skips the
"missing account id" throw.

## Tools it exposes (89 at v0.2.0)
`worker_list`, `worker_get`, `worker_put`, `worker_delete`, `worker_deploy`,
`kv_get/put/delete/list`, `r2_list_buckets/put_object/...`, `d1_query/list_databases`,
`do_*`, `queue_*`, `ai_inference/ai_list_models/...`, `analytics_get`,
`workers_analytics_search`, etc. Enough to read full deployment details of any Worker.

## Verified handshake (Windows, Hermes)
- `cmd.exe /c npx -y @cloudflare/mcp-server-cloudflare@latest run <ACCOUNT_ID>`
- `initialize` -> `INIT OK. server: cloudflare 1.0.0`
- `tools/list` -> count=89
- `tools/call worker_list` -> returns live Workers JSON (e.g. `sproutern`,
  `sproutern-server-blog`, `-tools`, `-games`, `-companies`, `-misc`) with `has_assets`,
  `modified_on`, `compatibility_date`, `handlers`, `named_handlers` (Durable Objects).

## Note on Vercel
There is **no Vercel MCP** usable from Hermes (the Vercel MCP is OpenCode-only and cannot run in
Hermes). To get Vercel deployment details, use the authenticated Vercel CLI instead
(`npx vercel whoami` / `vercel inspect` / `vercel ls`). Don't confuse a Cloudflare-deployed
project with a Vercel one.
