#!/usr/bin/env node
/**
 * cloudflare-mcp-ops.cjs  (KNOWN-GOOD, validated against @cloudflare/mcp-server-cloudflare@0.2.0)
 * ---------------------------------------------------------------------------
 * Runs the Cloudflare MCP operations a deployed Next.js-on-Workers site actually
 * needs, against the LIVE account. Reusable across sessions — no secret values
 * are printed.
 *
 * Usage:
 *   node scripts/cloudflare-mcp-ops.cjs            # runs all required ops
 *   node scripts/cloudflare-mcp-ops.cjs workers
 *   node scripts/cloudflare-mcp-ops.cjs versions
 *   node scripts/cloudflare-mcp-ops.cjs bindings
 *   node scripts/cloudflare-mcp-ops.cjs secrets
 *   node scripts/cloudflare-mcp-ops.cjs routes
 *
 * CRITICAL envelope quirk in @0.2.0 (learned the hard way):
 *   - `worker_*` tools read `request.params.arguments` (standard).
 *   - `version_list` / `service_binding_list` / `secret_list` / `route_list`
 *     read `request.params.input` (NON-standard). But the SDK still VALIDATES
 *     `params.name` + `params.arguments`. So we send BOTH `arguments` AND `input`.
 *   - `env_var_list` is BROKEN server-side (returns a JSON parse error) — excluded.
 *   - `zones_list` is BROKEN server-side ("[object Object]" is not valid JSON) —
 *     get the Zone ID via the wrangler OAuth token + REST /zones?name= API instead.
 *
 * Spawn note: on MSYS/Windows, spawn `cmd.exe /c` with ONE flat command string
 * (`npx -y @cloudflare/mcp-server-cloudflare@latest run <acctId>`). Bare `npx`
 * in a child spawn won't resolve.
 */
const { spawn } = require('child_process');

const ACCOUNT_ID = process.env.ACCOUNT_ID || 'a173a22f7ec326ddfc3929761e74a882';
const WORKER = process.env.WORKER || 'sproutern';
const ZONE_ID = process.env.ZONE_ID || '4b892c02d6f9201b2f3dd584be2a8473';
const MCP_ARGS = ['-y', '@cloudflare/mcp-server-cloudflare@latest', 'run', ACCOUNT_ID];

const OPS = {
  workers:  { tool: 'worker_list',            args: {} },
  versions: { tool: 'version_list',           args: { scriptName: WORKER } },
  bindings: { tool: 'service_binding_list',   args: { scriptName: WORKER } },
  secrets:  { tool: 'secret_list',            args: { scriptName: WORKER } },
  routes:   { tool: 'route_list',             args: { zoneId: ZONE_ID } },
};

function runOps(names) {
  return new Promise((resolve) => {
    const cmd = 'npx ' + MCP_ARGS.map(a => a.includes(' ') ? '"' + a + '"' : a).join(' ');
    const proc = spawn('cmd.exe', ['/c', cmd], {
      cwd: process.cwd(), stdio: ['pipe', 'pipe', 'pipe'], windowsHide: true,
    });
    let buf = '';
    const send = (o) => proc.stdin.write(JSON.stringify(o) + '\n');
    const results = {};
    const pending = new Set(names);

    proc.stdout.on('data', (d) => {
      buf += d.toString();
      let i;
      while ((i = buf.indexOf('\n')) >= 0) {
        const line = buf.slice(0, i).trim();
        buf = buf.slice(i + 1);
        if (!line) continue;
        let m; try { m = JSON.parse(line); } catch { continue; }
        if (m.id === 1 && m.result) {
          names.forEach((n, idx) =>
            send({ jsonrpc: '2.0', id: 10 + idx, method: 'tools/call',
              params: { name: OPS[n].tool, arguments: OPS[n].args, input: OPS[n].args } }));
        } else if (m.id >= 10) {
          const name = names[m.id - 10];
          const r = m.result || {};
          const text = ((r.toolResult && r.toolResult.content) || r.content || [])
            .map((c) => c.text || '').join('');
          results[name] = m.error ? ('ERR ' + JSON.stringify(m.error).slice(0, 200)) : text;
          pending.delete(name);
          if (pending.size === 0) { proc.kill(); resolve(results); }
        }
      }
    });
    proc.stderr.on('data', () => {});
    proc.on('error', () => resolve(results));
    send({ jsonrpc: '2.0', id: 1, method: 'initialize',
      params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'ops', version: '1' } } });
    setTimeout(() => { proc.kill(); resolve(results); }, 28000);
  });
}

function pretty(text) {
  try { return JSON.stringify(JSON.parse(text), null, 1); } catch { return text; }
}

(async () => {
  const arg = process.argv[2];
  const names = arg ? [arg] : Object.keys(OPS);
  for (const n of names) if (!OPS[n]) {
    console.error('Unknown op:', n, '— use one of', Object.keys(OPS).join(', ')); process.exit(1);
  }
  const results = await runOps(names);
  for (const n of names) {
    console.log('\n########## ' + n + ' (' + WORKER + ') ##########');
    console.log(pretty(results[n] || '(no result)'));
  }
})();
