---
name: prompt-templates-cli
version: 1.0.0
description: Render parameterized prompt templates from a catalog ({{var}} fill). Stdlib.
tags: [prompt, templates, cli, openclaw, hermes, agent]
---

# prompt-templates-cli — ship consistent agent instructions

Loads a templates.json catalog, fills {{var}} placeholders via --set, and prints the
rendered prompt. Great for standardizing code-review / summarize / triage prompts.
Stdlib, offline.

## Usage
```bash
python prompt_templates_cli.py list
python prompt_templates_cli.py render code-review --set role=senior --set tone=strict
```

## Why
Prompt drift causes agent drift. Templatize. Free + MIT.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar  *(add your link)*
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar      *(add your link)*
