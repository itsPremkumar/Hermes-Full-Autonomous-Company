[![ClawHub](https://img.shields.io/badge/ClawHub-skill-lint-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: skill-lint
version: 2.0.0
description: Lint ClawHub SKILL.md files: frontmatter, structure, command docs, thin-content detection
tags: ["lint", "skill", "clawhub", "cli", "docs", "quality", "python", "open-source", "agent", "automation", "MIT"]
---

# Skill Linter

**Validate ClawHub/OpenClaw skill folders before publishing: frontmatter, structure, command docs, thin-content detection.**

> *Keywords: lint, skill, clawhub, cli, docs, quality, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Publishing a malformed skill wastes a version and hurts trust. Skill Linter solves this: Validate ClawHub/OpenClaw skill folders before publishing: frontmatter, structure, command docs, thin-content detection.

**Best for:** Skill authors publishing to ClawHub.

## Features

- **Lint a skill folder**
- **Check frontmatter**
- **Detect thin content**
- **Validate command docs**
- **JSON output**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/skill-lint/main/skill_lint.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python skill_lint.py self-test     # prove it works end-to-end
python skill_lint.py check --help   # check subcommand
```

## Use cases

1. Lint a skill folder
1. Check frontmatter
1. Detect thin content
1. Validate command docs
1. JSON output

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Publish and pray | Catch issues pre-publish. |
| Manual review | Automated structure checks. |
| Thin skills | Detects low-value content. |

## FAQ (SEO / AEO)

**Q: What it checks**  
A: Frontmatter, structure, command docs, thin content.

**Q: CI?**  
A: Yes — --json.

**Q: Offline?**  
A: Yes.

**Q: Pair with?**  
A: skill-benchmark for grading.

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
      - name: Self-test skill-lint
        run: python skill_lint.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/skill-lint)
