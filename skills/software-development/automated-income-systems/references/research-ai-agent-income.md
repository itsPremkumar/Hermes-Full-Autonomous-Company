# Research: AI-agent companies & automation for making money (2026)

Condensed, verified findings from a live deep-search + primary-source read + HTTP
program vetting. Use this when the user says "research how AI agents make money" or
"find a working money method to implement." All programs below were curl-checked
(200 = live/free to join).

## Verified-live free money programs (HTTP check, this session)
| Program | Check | Notes |
|:--------|:-----:|:------|
| Amazon Associates | 200 | affiliate-tag placeholder `YOURTAG`; pays per sale |
| Gumroad | 200 | free storefront; you keep 100% minus fee; upload `PRODUCT.md` |
| Printify | 200 | print-on-demand; print+ship only on sale -> $0 upfront, highest upside |
| ShareASale | 301 | merchant network; needs a merchant ID |
| Fiverr Affiliates | 200 (root) | old `/cp/affiliates` URL 404s; use `fiverr.com/categories/<cat>?source=affiliate_fiverr&aff_id=<id>` |
| Spreadshirt Partner | 200 | (from earlier session) |

## Real earning methods + realistic ranges (primary sources)
From snaplama.com "How to Earn Money from AI Agents in 2026" + richtactic.com + aifundingtracker.com:
1. **Sell AI-agent workflows** (n8n/Make/Zapier templates) - $500-$2,000 each; 5-10 sales/mo = $2.5k-$20k/mo. Time to first sale: 2-4 wks.
2. **Chatbot services for niches** - setup $500-$2k + $500-$2k/mo retainer; 5-15 clients = $2k-$10k/mo.
3. **AI-agent consulting/implementation** - $5k-$50k+ per project; value-based 10-20% of savings; retainers $2k-$5k/mo. Highest leverage.
4. **Affiliate content + tools + Gumroad products** (this skill's A-C) - passive, scales with traffic, $0 cost.

## What NOT to build (scam exclusions - explicit)
Crypto/DEX "arbitrage bots", "automatic money" bots, token-airdrop schemes found on
GitHub are scams/illegal. Deliberately exclude. Build only legal, value-providing streams.

## Search recipe that works here
DuckDuckGo HTML via Jina Reader (Google is JS-redirect blocked):
```bash
q="AI agent automation company make money 2026"
enc=$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")
curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=$enc" \
  | grep -oE '\[[^]]+\]\(https://duckduckgo.com/l/\?uddg=[^)]+\)'
```
Then `curl -s "https://r.jina.ai/<primary-url>"` to read the actual guide.

## Honesty contract (always state to the user)
The agent automates creation + publishing 100%. Three things only the human can do
(all free, ~20 min once): (1) open payout accounts + paste IDs into config; (2) one
`git push` + enable Pages; (3) drive traffic (Reddit/Quora/X weekly). No visitors =
no income. It compounds weekly; NOT overnight passive income; earnings not guaranteed.
