---
name: cron-doctor
version: 2.0.0
description: Diagnose and fix cron job issues: missed runs, overlapping jobs, silent failures
tags: ["cron", "doctor", "diagnostics", "cli", "scheduler", "debug", "python", "open-source", "agent", "automation", "MIT"]
---

# Cron Doctor

**Validate and diagnose a scheduled-task file for an agent: parse errors, unsafe commands, collisions, missed/overlapping runs.**

> *Keywords: cron, doctor, diagnostics, cli, scheduler, debug, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

A bad cron line fails silently at 3am and you find out from users. Cron Doctor solves this: Validate and diagnose a scheduled-task file for an agent: parse errors, unsafe commands, collisions, missed/overlapping runs.

**Best for:** Agent operators, SREs, and anyone with scheduled jobs.

## Features

- **Check a crontab-style file for errors**
- **Flag unsafe commands (rm -rf, sudo)**
- **Detect overlapping jobs**
- **Suggest auto-fixes**
- **JSON output for CI**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/cron-doctor/main/cron_doctor.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python cron_doctor.py self-test     # prove it works end-to-end
python cron_doctor.py check --help   # check subcommand
```

## Use cases

1. Check a crontab-style file for errors
1. Flag unsafe commands (rm -rf, sudo)
1. Detect overlapping jobs
1. Suggest auto-fixes
1. JSON output for CI

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| crontab -l and hope | Parses, validates, and explains failures. |
| Cron lint gists | Adds unsafe-command detection and collisions. |
| Debugging at 3am | Catch it before the run, not after. |

## FAQ (SEO / AEO)

**Q: What schedules does it parse?**  
A: 30m, every 2h, '0 9 * * *', and standard crontab forms.

**Q: What is unsafe?**  
A: Destructive/gated commands like rm -rf, sudo, etc. are flagged.

**Q: CI?**  
A: Yes — --json + non-zero exit on failure.

**Q: Offline?**  
A: Yes.

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
      - name: Self-test cron-doctor
        run: python cron_doctor.py self-test
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/cron-doctor)
