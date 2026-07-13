---
name: Web Research Toolkit
version: 1.0.0
description: Route internet search, research, and lookup tasks through a unified CLI — DuckDuckGo, Wikipedia, and URL fetch in one tool. Zero external dependencies beyond Python stdlib.
tags: research,web,search,cli,python,wikipedia,duckduckgo
---

# Web Research Toolkit

A zero-dependency Python CLI that routes your internet research through three powerful backends — DuckDuckGo search, Wikipedia API, and raw URL fetch — all from the terminal. No API keys, no npm installs, no browser needed.

Perfect for automated research pipelines, AI agent toolchains, CI-based fact-checking, and developers who want web search without leaving the command line.

## Install

```bash
# No pip install required — Python 3.8+ stdlib only
# Copy the script anywhere
cp web_research.py /usr/local/bin/web-research
chmod +x /usr/local/bin/web-research

# Or run directly
python web_research.py --help
```

## Commands

| Command | Description |
|---------|-------------|
| `search <query>` | Search the web via DuckDuckGo Lite (no API key) |
| `search <query> --count 10` | Get N results (default: 5, max: 20) |
| `wiki <term>` | Fetch a Wikipedia summary for any topic |
| `wiki <term> --full` | Fetch the full Wikipedia article content |
| `fetch <url>` | Download and extract text from any webpage |
| `fetch <url> --output file.txt` | Save fetched content to a file |

## Usage

```bash
# Search the web
python web_research.py search "Python 3.13 new features"

# Get more results
python web_research.py search "Rust vs Go performance" --count 10

# Look up a Wikipedia topic
python web_research.py wiki "Transformer (machine learning model)"

# Full Wikipedia article
python web_research.py wiki "Attention Is All You Need" --full

# Fetch a webpage as plain text
python web_research.py fetch https://example.com

# Save output to a file
python web_research.py fetch https://docs.python.org/3/ --output python-docs.txt
```

## Features

- **Zero dependencies** — uses `urllib.request`, `html.parser`, and `json` from the Python standard library only
- **DuckDuckGo Lite search** — scrapes DuckDuckGo's lightweight search page (no API key, no rate limiting)
- **Wikipedia API** — queries the MediaWiki action API for structured article summaries
- **URL fetching** — downloads and extracts readable text from any HTTP/HTTPS URL
- **No API keys** — every command works with public, open APIs
- **Cross-platform** — runs on Linux, macOS, and Windows (Python 3.8+)
- **Structured output** — results returned as clean, parseable text
- **Error-resilient** — graceful fallbacks when a source is unreachable

## Examples

```bash
# Research pipeline - search, then fetch details
python web_research.py search "climate change 2025 report"
python web_research.py search "IPCC latest findings"
python web_research.py fetch https://www.ipcc.ch/report/ar6/

# Quick reference from Wikipedia
python web_research.py wiki "Large language model"
python web_research.py wiki "QLoRA fine-tuning" --full

# Fetch and analyze a blog post
python web_research.py fetch https://news.ycombinator.com/ --output hn-frontpage.txt

# Compare Wikipedia vs web search for the same topic
python web_research.py wiki "Web scraping"
python web_research.py search "web scraping best practices 2025"
```

## Why Web Research Toolkit?

Most web research requires either a browser GUI, an API key (Google Custom Search, Bing, etc.), or heavy npm/Go dependencies. This toolkit gives you three research backends in a single Python file with zero dependencies. It's designed for:

- **AI agents** that need web access without installing Playwright/Puppeteer
- **CI/CD pipelines** that fetch documentation during builds
- **Automated fact-checking** systems
- **Offline-first environments** where you control what gets installed
- **Rapid prototyping** — no signups, no API keys, just run it

Every backend uses public, open APIs (DuckDuckGo Lite, MediaWiki) with no authentication required.

## Support

- File an issue on the [ClawHub registry](https://clawhub.nousresearch.com)
- MIT License — free to use, modify, and share
- Contributions welcome — add more backends (Bing, Google via a proxy, etc.)
