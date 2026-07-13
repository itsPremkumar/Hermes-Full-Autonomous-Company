# Verified free income programs + GitHub vetting recipe

## How to vet a program / repo (do NOT trust claims)
Search-engine HTML (DuckDuckGo/Bing) returns captchas/empty for automated
fetches. Instead hit the official page directly and read HTTP status:

```bash
curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" --max-time 15 URL
# 200 = live / free to join ; 301/404 = moved or gone ; 000 = blocked
```
GitHub's `api.github.com/search/repositories?q=...` works unauthenticated but
is rate-limited (HTTP 429 after a few calls). Batch queries, then stop.

## Verdicts from one session (2026-07, Windows/MSYS host)
| Program / repo | HTTP | Verdict |
|---|---|---|
| Fiverr Affiliates `fiverr.com/affiliates` | 200 | free, per-referred-buyer payout -- Stream D |
| Amazon Associates `affiliate-program.amazon.com/` | 200 | free -- Stream A |
| Spreadshirt Partner `partner.spreadshirt.com/` | 200 | free POD alt to Printify |
| ShareASale `shareasale.com` | 301-> | free affiliate network |
| `IncomeStreamSurfer/print_on_demand_printify_automation` (125*, Py) | meta OK | real POD auto pattern (Printify+SD+Shopify) -- Stream E model |
| `kristynamarie99/pod-automation-system` (9*) | -- | n8n+Claude POD |
| `dylanpersonguy/MoneyPrinterV2` (26*) | -- | Shorts automation, needs a platform acct |
| `techroy23/BandwidthBucks` (11*) | -- | bandwidth-sharing passive income |
| Redbubble sell page | 404 | URL moved; skip or re-find |
| Printful products page | 410 | endpoint gone; provider still real |
| `StarNightCoder/Triangular-Arbitrage-...`, `AutomaticMoneyMakingBot`, `DFDTOKEN` | -- | SCAM / illegal -- excluded |

## Rule encoded in SKILL.md
Crypto/DEX "arbitrage bots", "automatic money" bots, token-airdrop schemes =
scams or illegal. Deliberately exclude. Build only legal, value-providing streams.

## Printify (Stream E) specifics
- Free to join. Prints + ships ONLY when a customer buys -> no inventory, no
  upfront cost. Margin on every order = highest-upside stream.
- The agent generates the LISTING (title/13 tags/description + a free SD design
  prompt). The user pastes it into their free Printify storefront. Agent cannot
  open that account -- same pattern as affiliate IDs.
