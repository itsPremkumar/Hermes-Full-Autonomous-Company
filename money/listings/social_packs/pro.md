# I will run a multi-platform content machine for you

**Price:** $199/mo
**Margin:** 97%
**Tags:** social media, content automation, pro social, auto posting, social media manager, growth

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- 1. Client sets brand + topics
- 2. n8n generates content (gif/diagram/video)
- 3. Schedule + auto-post across platforms
- 4. Track engagement, optimize
- 5. Monthly content calendar + report

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
 "name": "social-poster",
 "nodes": [
  {
   "type": "n8n-nodes-base.scheduleTrigger",
   "name": "DailyPost",
   "params": {
    "interval": [
     {
      "field": "cronExpression",
      "expression": "0 10 * * *"
     }
    ]
   }
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "GenContent",
   "params": {
    "url": "={{$env.CONTENT_GEN}}/make",
    "httpMethod": "POST"
   }
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "PostX",
   "params": {
    "url": "={{$env.X_API}}/tweet",
    "httpMethod": "POST"
   }
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "PostIG",
   "params": {
    "url": "={{$env.IG_API}}/media",
    "httpMethod": "POST"
   }
  }
 ],
 "connections": "DailyPost \u2192 GenContent \u2192 PostX \u2192 PostIG"
}
```
