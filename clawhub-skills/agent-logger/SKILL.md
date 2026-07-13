---
name: agent-logger
version: 1.0.0
description: Analyze agent run logs for errors, token spikes, and failures. Stdlib, offline.
tags: [logging, observability, debug, openclaw, hermes, agent]
---

# agent-logger — know when your agent is sick

Point agent-logger at a log file or directory and get a structured health report:
error lines, warning counts, suspected token spikes, and a HEALTHY/DEGRADED/UNHEALTHY
verdict. Stdlib, offline, no telemetry.

## Usage
```bash
python agent_logger.py scan <logfile|dir> [--json]
```

## Why
"Something's wrong with the agent" is easier to fix when you can see the errors. Free + MIT.
A premium "log dashboard + alerting" bundle is on Gumroad.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar  *(add your link)*
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar      *(add your link)*
