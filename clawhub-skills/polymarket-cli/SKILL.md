---
name: polymarket-cli
version: 1.0.0
description: Query Polymarket prediction markets: browse markets, check prices, view orderbooks, and track your positions. No API key needed.
tags: ["polymarket", "prediction", "markets", "crypto", "cli", "python"]
---

# Polymarket CLI

## Install
```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/polymarket-cli/main/polymarket_cli.py
```

## Usage
```bash
python polymarket_cli.py search "election"
python polymarket_cli.py trending
python polymarket_cli.py market <slug-or-id>
python polymarket_cli.py price "will-bitcoin-reach-100k-2025"
python polymarket_cli.py orderbook <token-id>
python polymarket_cli.py categories
```

## Features
- **Market search** — find markets by keyword
- **Trending** — see hot prediction markets
- **Market details** — volume, liquidity, description
- **Price lookup** — current YES/NO prices
- **Orderbook** — bid/ask depth for any market
- **Categories** — browse market categories
- **No API key** — uses public Polymarket API

## Why
Check prediction markets from your terminal. No wallet or API key needed.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

test: python polymarket_cli.py --help   # install first: curl -O https://raw.githubusercontent.com/itsPremkumar/polymarket-cli/main/polymarket_cli.py
