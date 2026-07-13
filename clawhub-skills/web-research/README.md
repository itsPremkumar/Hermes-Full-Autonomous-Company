[![ClawHub](https://img.shields.io/badge/ClawHub-web-research-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: web-research
version: 2.0.0
description: DuckDuckGo + Wikipedia research CLI with URL fetching, content extraction, and citation export
tags: ["web", "research", "search", "duckduckgo", "wikipedia", "cli", "python", "open-source", "agent", "automation", "MIT"]
---

# Web Research Toolkit

**Route search, research, and lookups through one CLI — DuckDuckGo, Wikipedia, and URL fetch — zero dependencies.**

> *Keywords: web, research, search, duckduckgo, wikipedia, cli, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Web research is scattered across sites and needs API keys for most tools. Web Research Toolkit solves this: Route search, research, and lookups through one CLI — DuckDuckGo, Wikipedia, and URL fetch — zero dependencies.

**Best for:** Researchers, agents, and CI fact-checkers.

## Features

- **DuckDuckGo search**
- **Wikipedia lookups**
- **Fetch + extract a URL**
- **Export citations**
- **Batch research in CI**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/web-research/main/web_research.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python web_research.py self-test     # prove it works end-to-end
python web_research.py search --help   # search subcommand
python web_research.py wiki --help   # wiki subcommand
python web_research.py fetch --help   # fetch subcommand
```

## Use cases

1. DuckDuckGo search
1. Wikipedia lookups
1. Fetch + extract a URL
1. Export citations
1. Batch research in CI

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Per-site research | One CLI, three backends. |
| API-key tools | Zero-dependency, keyless. |
| Copy-paste | Citations + extraction built in. |

## FAQ (SEO / AEO)

**Q: Backends?**  
A: DuckDuckGo, Wikipedia, raw URL fetch.

**Q: API key?**  
A: No — stdlib only.

**Q: Citations?**  
A: Exportable.

**Q: Offline?**  
A: No — live web.

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
      - name: Self-test web-research
        run: python web_research.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/web-research)
