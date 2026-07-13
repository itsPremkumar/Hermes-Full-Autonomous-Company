# Vercel metrics probes (CLI = MCP replacement when OAuth is blocked)

MCP `mcp.vercel.com` needs an OAuth browser flow that can't run in the Hermes session
(OpenCode-only). The authenticated Vercel CLI exposes the same account data and ALSO
Web Analytics + Speed Insights the MCP lacks. Always pass `--scope <team>` and
`--project <name>`.

## Pageviews / traffic
```
vercel metrics vercel.analytics_pageview.count --since 30d --project X --prod --scope T
vercel metrics vercel.analytics_pageview.count --since 30d --project X --prod --scope T --group-by request_path --limit 10
vercel metrics vercel.analytics_pageview.count --since 30d --project X --prod --scope T --group-by country --limit 6
vercel metrics vercel.analytics_pageview.count --since 30d --project X --prod --scope T --group-by device_type --limit 5
```
- Total sits on the line matching `^\s+[0-9]` (e.g. `  4,699  26.0  ...`).
- Per-metric avg/max: `vercel metrics` prints header then a value line; capture with
  `grep -E "^\s*[0-9]"`.

## Speed Insights (Core Web Vitals) — 7d field data
```
for m in lcp_ms fcp_ms ttfb_ms inp_ms cls; do
  v=$(vercel metrics vercel.speed_insights.$m --since 7d --project X --prod --scope T 2>&1 | grep -E "^\s*[0-9]" | head -1)
  echo "$m = $v"
done
```
Thresholds: LCP <2.5s good, FCP <1.8s, TTFB <800ms, INP <200ms, CLS <0.1.

## Dimensions NOT exposed on free Web Analytics
- `referrer` / `referrer_host` and `operating_system` return empty on the free plan.
- If you got them once, it was likely a cache fluke — don't rely on them.

## Security / headers (live HTTP)
```
curl -sI https://www.<site>.com | grep -iE "strict-transport|x-frame|x-content|content-security|access-control|HTTP/"
```
- CORS `*` on a static PAGE is Vercel's default CDN header (harmless). The real check is
  the API route: `curl -sI -H "Origin: https://evil.example.net" <site>/api/embed` →
  must return that exact origin, NOT `*`.
