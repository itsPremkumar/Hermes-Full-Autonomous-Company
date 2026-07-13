<!-- Canonical SEO/AEO/GEO SKILL.md skeleton for a ClawHub skill.
Copy per skill, fill <PLACEHOLDERS>, keep every section. Rules below. -->

---
name: <slug>
version: 2.0.1
description: <one-line, keyword-rich: what it does + key benefit>
tags: ["<primary>", "<secondary>", "cli", "python", "open-source", "agent", "automation", "MIT"]
---

# <Display Title>

**<one-liner: what it does and why it matters>**

> *Keywords: <comma, separated, seo, terms>*
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

<Problem statement in one sentence.> <Title> solves this: <one-liner>.

**Best for:** <target audience — who should use this>

## Features

- **<use case 1>**
- **<use case 2>**
- **<use case 3>**
- **<use case 4>**
- **<use case 5>**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/<slug>/main/<tool>.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python <tool>.py self-test     # ONLY if the .py has add_parser("self-test")
python <tool>.py <subcmd> --help   # <subcmd> from add_parser(...) ONLY
# NEVER list positional args (path/file/query) as if they were subcommands
```

## Use cases

1. <use case 1>
2. <use case 2>
3. <use case 3>
4. <use case 4>
5. <use case 5>

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| <competitor / manual approach> | <concrete differentiator> |
| <competitor / manual approach> | <concrete differentiator> |
| <competitor / manual approach> | <concrete differentiator> |

## FAQ (SEO / AEO)

**Q: <search-style question?>**  
A: <direct answer>

**Q: <search-style question?>**  
A: <direct answer>

**Q: <search-style question?>**  
A: <direct answer>

**Q: <search-style question?>**  
A: <direct answer>

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
      - name: Self-test <slug>
        run: python <tool>.py self-test   # or `--help` if no self-test subcommand
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/<slug>)

<!--
RULES (do not violate):
1. Quick-start subcommands = ONLY names from add_parser("...") in <tool>.py.
   A cli_flags inventory also contains positional args (path/file/query) — do NOT
   present those as `python <tool>.py path --help`.
2. self-test line only if add_parser("self-test") exists. Bare string match hits
   skills like notion-api that have NO self-test.
3. URL format is owner-namespaced: https://clawhub.ai/itspremkumar/skills/<slug>
   (NOT https://clawhub.ai/skills/skills/<slug> — that 404s).
4. README.md = same content + 3 shields.io badges at top.
-->
