# Discovering real, free money-automation projects on GitHub

Search-engine HTML (DuckDuckGo/Bing) is captcha-blocked for automated fetches,
but GitHub's repo-search API is reachable and returns clean JSON — use it to
FIND projects, then vet each hit before building on it.

## Query pattern
```bash
curl -s "https://api.github.com/search/repositories?q=<query>&sort=stars&order=desc&per_page=5" \
  | python -c "import sys,json; d=json.load(sys.stdin); [print(it['stargazers_count'], it['full_name'], (it.get('description') or '')[:70]) for it in d.get('items',[])]"
```

## Queries that surfaced legit streams (this session)
- `passive income automation` -> `techroy23/BandwidthBucks` (11*, bandwidth-sharing),
  `DuxSec/videoGenerator` (282*, Reels/Shorts maker)
- `affiliate marketing bot` -> `dylanpersonguy/MoneyPrinterV2` (26*, YouTube Shorts)
- `print on demand automation` -> `IncomeStreamSurfer/print_on_demand_printify_automation`
  (125*, Printify+SD+Shopify -> became Stream E), `kristynamarie99/pod-automation-system` (9*)

## Vetting rules
1. Read repo metadata (stars, language, license) via API — cheap, no HTML parse.
2. Confirm the program is FREE to join via its official page (curl HTTP 200).
   POD (Printify/Printful) is free; they print+ship on sale = no upfront cost.
3. REJECT: crypto/DEX "arbitrage", "automatic money" bots, token-airdrop schemes
   (scams/illegal). Found and excluded: `Triangular-Arbitrage-JS-DEX-Bot`,
   `AutomaticMoneyMakingBot`, `DFDTOKEN`.

## Gotchas
- Unauthenticated API is rate-limited (~10 req/min, returns HTTP 429). Back off; retry later.
- `raw.githubusercontent.com` README fetches also 429 under load — use the API
  metadata, or read the cloned repo locally instead of fetching raw over HTTP.
- Don't clone repos with `license: None` for reuse; prefer your own clean
  reimplementation (as done for Stream E) to avoid unclear-license entanglement.
- GitHub API search needs no auth for low volume; `gh` CLI was NOT installed on
  the host, so curl + python parse is the reliable path.
