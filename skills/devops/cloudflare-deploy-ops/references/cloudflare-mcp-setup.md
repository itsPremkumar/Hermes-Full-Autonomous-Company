# Cloudflare MCP server setup & auth

Package: `@cloudflare/mcp-server-cloudflare` (ESM; bin `mcp-server-cloudflare` → `dist/index.js`).
Verified working version: `0.2.0`.

## Why it works without a separate API token
The server's `run` branch reads auth in this order:
1. `process.env.CLOUDFLARE_API_TOKEN` + `process.env.CLOUDFLARE_ACCOUNT_ID` (if set), OR
2. Falls back to the local wrangler OAuth token via `getAuthTokens()`, which reads
   `%APPDATA%\xdg.config\.wrangler\config\default.toml` (holds `oauth_token`, `refresh_token`,
   `scopes`, `expiration_time`). It auto-refreshes an expired access token.

So after the user runs `npx wrangler login` once in a browser, the MCP server is already
authenticated — no `CLOUDFLARE_API_TOKEN` needed.

## .mcp.json shape
```json
{
  "mcpServers": {
    "cloudflare": {
      "command": "npx",
      "args": ["-y", "@cloudflare/mcp-server-cloudflare@latest", "run", "<accountId>"]
    }
  }
}
```
- `<accountId>` comes from `npx wrangler whoami` (the "Account ID" column).
- The bare package name (no `run`) throws: `Unknown command: undefined. Expected 'init' or 'run'.`

## Verifying the connection (probe without an MCP client)
Spawn the server, send JSON-RPC over stdio, read the result. On Windows, spawn via
`cmd.exe /c npx …` (npx isn't on the child's PATH otherwise → `spawn npx ENOENT`).
```js
const { spawn } = require('child_process');
const proc = spawn('cmd.exe', ['/c', 'npx -y @cloudflare/mcp-server-cloudflare@latest run <accountId>'],
  { cwd: '<project>', stdio: ['pipe','pipe','pipe'], windowsHide: true });
let buf = '';
proc.stdout.on('data', d => {
  buf += d; let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const line = buf.slice(0,i).trim(); buf = buf.slice(i+1); if (!line) continue;
    const m = JSON.parse(line);
    if (m.id === 1 && m.result) proc.stdin.write(JSON.stringify({jsonrpc:'2.0',id:2,method:'tools/list',params:{}})+'\n');
    if (m.id === 2 && m.result && m.result.tools) console.log('tools:', m.result.tools.length, m.result.tools.map(t=>t.name).slice(0,10));
  }
});
proc.on('error', e => console.error('spawn err', e.message));
proc.stdin.write(JSON.stringify({jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2024-11-05',capabilities:{},clientInfo:{name:'probe',version:'1.0'}}})+'\n');
setTimeout(()=>{ console.log('DONE'); proc.kill(); process.exit(0); }, 12000);
```
Expected: stderr shows `[auth] Config loaded: {"accountId":"✓","apiToken":"✓"}`,
then `tools/list` returns ~89 tools.

## Tool surface (subset)
worker_list, worker_get, worker_put, worker_delete, worker_deploy,
kv_get/put/delete/list, r2_*, d1_*, do_*, queue_*, ai_inference/ai_list_models/ai_embeddings,
analytics_get, workers_analytics_search.

## To fetch live deployment details
Call `worker_list` (no args) → returns array of deployed Workers with
`id`, `has_assets`, `modified_on`, `compatibility_date`, `handlers`, `compatibility_flags`,
`etag`, `last_deployed_from`. Then `worker_get` with `{name}` for detail.
