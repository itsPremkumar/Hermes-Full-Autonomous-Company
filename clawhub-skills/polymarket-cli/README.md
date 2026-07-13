[![ClawHub](https://img.shields.io/badge/ClawHub-polymarket-cli-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: polymarket-cli
version: 2.0.0
description: Query Polymarket prediction markets: search, price history, trending, categories, stats
tags: ["polymarket", "prediction", "markets", "trading", "cli", "crypto", "python", "open-source", "agent", "automation", "MIT"]
---

# Polymarket CLI

**Query Polymarket prediction markets: search, price history, trending, categories, and stats.**

> *Keywords: polymarket, prediction, markets, trading, cli, crypto, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Tracking prediction markets means juggling the website and spreadsheets. Polymarket CLI solves this: Query Polymarket prediction markets: search, price history, trending, categories, and stats.

**Best for:** Traders, analysts, and agents monitoring markets.

## Features

- **Search markets**
- **Pull price history**
- **List trending**
- **Browse categories**
- **Show stats**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/polymarket-cli/main/polymarket_cli.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python polymarket_cli.py --help        # list options
```

## Use cases

1. Search markets
1. Pull price history
1. List trending
1. Browse categories
1. Show stats

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Polymarket website | Scriptable search + history. |
| Manual tracking | Trending + stats in one CLI. |
| Spreadsheets | Pipe to CSV/JSON. |

## FAQ (SEO / AEO)

**Q: Live data?**  
A: Yes — queries Polymarket's public API.

**Q: Price history?**  
A: Available per market.

**Q: Categories?**  
A: Browse by category.

**Q: Offline?**  
A: No — live API.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test polymarket-cli
        run: python polymarket_cli.py --help
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/polymarket-cli)
