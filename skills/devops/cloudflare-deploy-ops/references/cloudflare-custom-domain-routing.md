# Custom domain routing via the Cloudflare MCP

The Cloudflare MCP server exposes `route_create` / `route_list` / `route_update` /
`route_delete` — these map a host pattern in a DNS **zone** to a Worker. This is how
`app.sproutern.com` was attached to the `sproutern` worker.

## When this applies
- The site is deployed to Workers and you want a real domain (not just `*.workers.dev`).
- The domain's zone **already exists** in the Cloudflare account (very common — the domain
  may already resolve to Cloudflare IPs even if nothing is routed yet). In that case you do
  NOT migrate DNS; you only attach a route.

## Step-by-step
1. **Get the Zone ID.** `zones_list` MCP is broken server-side in
   `@cloudflare/mcp-server-cloudflare@0.2.0` (`Error: "[object Object]" is not valid JSON`),
   and `wrangler dns` isn't a subcommand in v4. Read the wrangler OAuth token and call the
   REST API directly:
   ```js
   const fs = require('fs'), path = require('path');
   const token = fs.readFileSync(
     path.join(process.env.APPDATA, 'xdg.config', '.wrangler', 'config', 'default.toml'), 'utf8')
     .match(/oauth_token\s*=\s*"([^"]+)"/)[1];
   // GET https://api.cloudflare.com/client/v4/zones?name=example.com
   // header: Authorization: Bearer <token>
   // → result[0].id is the zone id; result[0].account.id should match the deploy account
   ```
2. `route_list` with `{ zoneId }` → see what's already routed (avoid duplicates).
3. `route_create` with `{ zoneId, pattern: "app.example.com/*", scriptName: "<worker>" }`.
   Pass BOTH `arguments` AND `input` mirrors (see the non-standard envelope pitfall in the
   SKILL.md — these route tools read `request.params.input`):
   ```json
   { "jsonrpc":"2.0","id":11,"method":"tools/call",
     "params":{ "name":"route_create",
       "arguments":{ "zoneId":"Z","pattern":"app.example.com/*","scriptName":"sproutern" },
       "input":     { "zoneId":"Z","pattern":"app.example.com/*","scriptName":"sproutern" } } }
   ```
   Returns `{ "id":"<routeId>", "pattern":"app.example.com/*", "script":"sproutern", ... }`.
4. **Wait ~30s** for Cloudflare to propagate, then `curl -I https://app.example.com` → 200.
5. After routing, BOTH the custom domain and the original `*.workers.dev` URL serve the site.

## Rollback
`route_delete` with `{ zoneId, routeId }`. A route is fully reversible and does NOT touch DNS
records — safe to add/remove without breaking the underlying domain.

## Gotcha — what was serving the domain before
Before routing, `app.sproutern.com` resolved to Cloudflare IPs but returned
"Site not found · GitHub Pages" (the zone existed, no worker route). A route attaches the
worker; if a subdomain is already served by something else (GitHub Pages / Vercel behind
Cloudflare proxy), a route for that specific subdomain overrides it for the worker. Always
`curl` the target before + after to confirm the change.
