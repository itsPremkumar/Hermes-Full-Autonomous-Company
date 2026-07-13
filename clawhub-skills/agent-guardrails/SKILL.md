---
name: agent-guardrails
version: 1.0.0
description: Pre-flight safety check for a planned agent action (deny destructive/exfil, warn irreversible). Stdlib.
tags: [safety, guardrails, approval, openclaw, hermes, agent]
---

# agent-guardrails — fail safe before the agent acts

Scans a proposed action against a ruleset: blocks destructive/remote-exec patterns and
plaintext secrets (DENY), warns on irreversible actions without an approval gate (WARN).
Returns ALLOW/WARN/DENY with reasons. Stdlib, offline.

## Usage
```bash
python agent_guardrails.py check "send email to client" [--json]
```

## Why
Cheap pre-flight that stops the boring retry from finding the credentialed path. Free + MIT.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar  *(add your link)*
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar      *(add your link)*
