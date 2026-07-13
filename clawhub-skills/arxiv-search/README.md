[![ClawHub](https://img.shields.io/badge/ClawHub-arxiv-search-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: arxiv-search
version: 2.0.0
description: Search arXiv papers by keyword, author, category with full-text download and citation export
tags: ["arxiv", "research", "papers", "academic", "cli", "search", "python", "open-source", "agent", "automation", "MIT"]
---

# arXiv Research Search

**Search arXiv papers by keyword, author, or category with citation export.**

> *Keywords: arxiv, research, papers, academic, cli, search, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Keeping up with the arXiv firehose is manual and citation formatting is painful. arXiv Research Search solves this: Search arXiv papers by keyword, author, or category with citation export.

**Best for:** Researchers, students, and AI/ML engineers tracking papers.

## Features

- **Search by keyword/author/category**
- **Sort and filter recent papers**
- **Export BibTeX citations**
- **Pull paper metadata into a pipeline**
- **Track a research niche**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/arxiv-search/main/arxiv_search.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python arxiv_search.py --help        # list options
```

## Use cases

1. Search by keyword/author/category
1. Sort and filter recent papers
1. Export BibTeX citations
1. Pull paper metadata into a pipeline
1. Track a research niche

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| arXiv website UI | Scriptable search + citation export for pipelines. |
| Manual BibTeX | Citations generated automatically. |
| Reading every new submission | Filtered, category-aware search. |

## FAQ (SEO / AEO)

**Q: What can I search by?**  
A: Keyword, author, and arXiv category (cs.AI, cs.LG, etc.).

**Q: Can I export citations?**  
A: Yes — BibTeX/citation export is built in.

**Q: Does it need an API key?**  
A: No — uses the public arXiv API.

**Q: Offline?**  
A: No — it queries arXiv live.

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
      - name: Self-test arxiv-search
        run: python arxiv_search.py --help
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/arxiv-search)
