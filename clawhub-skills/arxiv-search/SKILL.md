---
name: arxiv-search
version: 1.0.0
description: Search academic papers on arXiv by keyword, author, category, or ID. Fetch abstracts, download PDFs, and export citations.
tags: ["arxiv", "papers", "research", "academic", "cli", "python"]
---

# ArXiv Paper Search

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/arxiv-search/main/arxiv_tools.py
```

## Usage

```bash
python arxiv_tools.py search "machine learning transformers" --limit 10
python arxiv_tools.py search "quantum computing" --sort date --limit 5
python arxiv_tools.py author "Yann LeCun" --limit 5
python arxiv_tools.py category cs.AI --limit 10
python arxiv_tools.py abstract 2301.12345
python arxiv_tools.py fetch 2301.12345
```

## Features

- **Keyword search** — full-text search across all arXiv papers
- **Author lookup** — find papers by specific researcher
- **Category browse** — browse recent papers in any arXiv category
- **Abstract fetch** — get full abstract of a specific paper
- **PDF links** — direct download URLs included
- **Zero API key** — uses public arXiv API

## Why
Academic research from the terminal. No API keys, no bloat.


## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
