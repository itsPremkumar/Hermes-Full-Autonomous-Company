---
name: cron-doctor
version: 1.0.0
description: Validate and diagnose a scheduled-task file for an agent (parse errors, unsafe cmds). Stdlib.
tags: [cron, schedule, safety, openclaw, hermes, agent]
---

# cron-doctor — don't ship a broken schedule

Parses a crontab-style file (30m | every 2h | "0 9 * * * <cmd>") and reports
unparseable lines, collisions, and unsafe commands (rm -rf, sudo, etc). Stdlib, offline.

## Usage
```bash
python cron_doctor.py check <file> [--json]
```

## Why
A bad cron line fails silently at 3am. Check it first. Free + MIT.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar  *(add your link)*
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar      *(add your link)*
