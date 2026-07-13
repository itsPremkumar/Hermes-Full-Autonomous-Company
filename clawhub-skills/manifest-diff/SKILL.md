---
name: manifest-diff
version: 1.0.0
description: Diff two agent capability manifests and report what changed (caps/deps/status). Stdlib.
tags: [manifest, diff, versioning, openclaw, hermes, agent]
---

# manifest-diff — see exactly what changed between two agent versions

Compares two agent manifest JSONs and reports changed fields, added/removed keys
(capabilities, dependencies, status). Stdlib, offline.

## Usage
```bash
python manifest_diff.py a.json b.json [--json]
```

## Why
When you bump an agent, you want to know what you actually changed before it goes live.
Free + MIT.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar  *(add your link)*
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar      *(add your link)*
