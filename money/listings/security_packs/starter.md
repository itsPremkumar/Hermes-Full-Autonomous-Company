# I will scan your repo for leaked secrets + vulnerabilities

**Price:** $199 setup + $99/mo
**Margin:** 97%
**Tags:** security scan, secret scanning, vulnerability, devsecops, starter security, code audit

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- 1. Client grants repo / site access
- 2. n8n cron runs secret-scanner + skill-lint
- 3. Generate branded report (Stirling-PDF)
- 4. Email findings + severity ranking
- 5. Monthly trend + fix checklist

## Why this works
- Self-hosted stack (n8n + free tools) → 90–99% profit margin
- Every deliverable is generated and delivered automatically
- You own the system; scale to unlimited clients

## FAQ
**Q: Do I need to pay for software?**
A: No. Everything runs on free open-source tools (n8n, Chatwoot, Stirling-PDF, Listmonk).

**Q: Is this a one-time build or ongoing?**
A: Both. One-time setup + optional monthly retainer for monitoring/optimization.

**Q: Can you customize for my niche?**
A: Yes — every package is generated from a template and tuned to your vertical.

## Technical spec (for the build)
```json
{
 "name": "security-scan",
 "nodes": [
  {
   "type": "n8n-nodes-base.scheduleTrigger",
   "name": "ScanCron",
   "params": {
    "interval": [
     {
      "field": "cronExpression",
      "expression": "0 3 * * 1"
     }
    ]
   }
  },
  {
   "type": "n8n-nodes-base.executeCommand",
   "name": "SecretScan",
   "params": {
    "command": "python secret_scanner.py --repo $REPO --json out.json"
   }
  },
  {
   "type": "n8n-nodes-base.executeCommand",
   "name": "LintScan",
   "params": {
    "command": "python skill_lint.py --check $REPO"
   }
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "RenderPDF",
   "params": {
    "url": "={{$env.STIRLING}}/api/converter/file/pdf",
    "httpMethod": "POST"
   }
  }
 ],
 "connections": "ScanCron \u2192 SecretScan \u2192 LintScan \u2192 RenderPDF"
}
```
