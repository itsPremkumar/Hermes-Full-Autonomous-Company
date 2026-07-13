# Cloudflare MCP — calling tools over stdio (verified recipe)

Server: `@cloudflare/mcp-server-cloudflare@0.2.0`. Invoked as
`npx -y @cloudflare/mcp-server-cloudflare@latest run <accountId>`.
It reuses the `wrangler login` OAuth token (cached at
`%APPDATA%\xdg.config\.wrangler\config\default.toml`), so no API token is needed.

## The envelope quirk (the real gotcha)

The SDK validates `params.name` + `params.arguments`, but several handlers read
`request.params.input`. So for `version_list`, `service_binding_list`, `env_var_list`,
`secret_list` you MUST send BOTH `arguments` and `input`:

```json
{ "jsonrpc":"2.0", "id":11, "method":"tools/call",
  "params": {
    "name": "service_binding_list",
    "arguments": { "scriptName": "sproutern" },
    "input": { "scriptName": "sproutern" }
  }
}
```

If you omit `input` you get:
`Error: Cannot destructure property 'scriptName' of 'request.params.input' as it is undefined.`

`worker_*` tools (`worker_get`, `worker_list`) use the standard `arguments` only — no `input`.

Response shape is wrapped: `result.toolResult.content[].text` (a JSON string), or
`result.toolResult` with `isError:true`. Parse `content[0].text` as JSON.

## `env_var_list` is broken in 0.2.0

Returns `Error: No number after minus sign in JSON at position 1` from the handler itself.
Do NOT debug it — the worker uses build-time `NEXT_PUBLIC_*` vars, not runtime env vars.
`secret_list` correctly returns `[]`.

## Working stdio probe (Windows / MSYS)

Spawn via `cmd.exe /c npx …` — a bare `spawn('npx', …)` fails with ENOENT because the child
does not inherit the MSYS PATH translation. Use `shell:false` + `cmd.exe /c`.

```js
const { spawn } = require('child_process');
const proc = spawn('cmd.exe', ['/c', 'npx -y @cloudflare/mcp-server-cloudflare@latest run a173a22f7ec326ddfc3929761e74a882'], {
  cwd: 'C:/one/sproutern-cloudflar', stdio: ['pipe','pipe','pipe'], windowsHide: true,
});
let buf = '';
proc.stdout.on('data', d => {
  buf += d.toString();
  let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const l = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
    if (!l) continue;
    const m = JSON.parse(l);
    if (m.id === 1 && m.result) {
      proc.stdin.write(JSON.stringify({ jsonrpc:'2.0', id:11, method:'tools/call',
        params:{ name:'service_binding_list', arguments:{scriptName:'sproutern'}, input:{scriptName:'sproutern'} } }) + '\n');
    }
    if (m.id === 11) {
      const t = (m.result.toolResult.content || []).map(c => c.text).join('');
      console.log(t);
      proc.kill(); process.exit(0);
    }
  }
});
proc.stdin.write(JSON.stringify({ jsonrpc:'2.0', id:1, method:'initialize',
  params:{ protocolVersion:'2024-11-05', capabilities:{}, clientInfo:{name:'probe',version:'1'} } }) + '\n');
```

## What this project actually needs from the MCP

Only a slice of the 89 tools is relevant to the deployed Sproutern site:
- `worker_list` / `worker_get` — see the 6 workers (main `sproutern` + 5 split).
- `version_list` / `version_rollback` — deploy history + recovery from a bad deploy.
- `service_binding_list` — verify `BLOG_WORKER`→`sproutern-server-blog` etc. resolve.
- `env_var_*` / `secret_*` — config (note env_var_list is broken; secrets are `[]`).
- `analytics_get` — needs a `zoneId` (custom domain); NOT available on `*.workers.dev`.
- `route_*` / `wfp_*` — only when attaching `app.sproutern.com`.
No KV/R2/D1/Queues/Durable-Objects bindings exist in this project's config.
