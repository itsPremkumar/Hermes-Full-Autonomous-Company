#!/usr/bin/env node
/**
 * mcp-ops-probe.cjs — reusable Cloudflare MCP probe (parameterized).
 *
 * Runs the MCP operations a deployed Worker actually needs, against the LIVE
 * account, and prints them. No secret values are printed.
 *
 * Usage:
 *   ACCOUNT_ID=xxxx WORKER=sproutern ZONE_ID=zzzz node mcp-ops-probe.cjs [op]
 *   op ∈ workers | versions | bindings | secrets | routes   (default: all)
 *
 * Handles the NON-STANDARD argument envelope of @cloudflare/mcp-server-cloudflare@0.2.0:
 *   - worker_*  tools read request.params.arguments
 *   - version_list / service_binding_list / secret_list / route_list read request.params.input
 *   - the SDK validates params.name + params.arguments, so we send BOTH mirrors.
 * `env_var_list` is intentionally excluded — it is BROKEN server-side in this version.
 *
 * Spawn note: on MSYS/Windows, child spawn can't resolve bare `npx`; wrap with
 * `cmd.exe /c "npx ..."` as a single command string.
 */
const { spawn } = require('child_process');

const ACCOUNT_ID = process.env.ACCOUNT_ID || 'REPLACE_ME';
const WORKER     = process.env.WORKER     || 'sproutern';
const ZONE_ID    = process.env.ZONE_ID    || 'REPLACE_ME';

const OPS = {
  workers:  { tool: 'worker_list',           args: {} },
  versions: { tool: 'version_list',          args: { scriptName: WORKER } },
  bindings: { tool: 'service_binding_list',  args: { scriptName: WORKER } },
  secrets:  { tool: 'secret_list',           args: { scriptName: WORKER } },
  routes:   { tool: 'route_list',            args: { zoneId: ZONE_ID } },
};

function runOps(names) {
  return new Promise((resolve) => {
    const cmd = 'npx ' + ['-y', '@cloudflare/mcp-server-cloudflare@latest', 'run', ACCOUNT_ID]
      .map((a) => (a.includes(' ') ? '"' + a + '"' : a)).join(' ');
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
          names.forEach((n, idx) => send({
            jsonrpc: '2.0', id: 10 + idx, method: 'tools/call',
            params: { name: OPS[n].tool, arguments: OPS[n].args, input: OPS[n].args },
          }));
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
    console.error('Unknown op:', n, '— use one of', Object.keys(OPS).join(', '));
    process.exit(1);
  }
  const results = await runOps(names);
  for (const n of names) {
    console.log('\n########## ' + n + ' (' + WORKER + ') ##########');
    console.log(pretty(results[n] || '(no result)'));
  }
})();
