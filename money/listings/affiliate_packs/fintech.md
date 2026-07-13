# I will launch a fintech affiliate site (cards, brokers, tools)

**Price:** $300 setup + $99/mo
**Margin:** 99%
**Tags:** affiliate marketing, fintech affiliate, content farm, passive income, blog automation, seo

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- 1. Pick niche + affiliate programs
- 2. Generate 30 posts/mo (blog + social)
- 3. Auto-publish via n8n (WordPress + X/threads)
- 4. Insert affiliate links + track clicks
- 5. Monthly earnings report

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
 "name": "affiliate-farm",
 "nodes": [
  {
   "type": "n8n-nodes-base.scheduleTrigger",
   "name": "DailyPost",
   "params": {
    "interval": [
     {
      "field": "cronExpression",
      "expression": "0 9 * * *"
     }
    ]
   }
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "GenContent",
   "params": {
    "url": "={{$env.BLOG_GEN}}/generate",
    "httpMethod": "POST"
   }
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "PostWP",
   "params": {
    "url": "={{$env.WP}}/wp-json/wp/v2/posts",
    "httpMethod": "POST"
   }
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "PostSocial",
   "params": {
    "url": "={{$env.SOCIAL_API}}/post",
    "httpMethod": "POST"
   }
  }
 ],
 "connections": "DailyPost \u2192 GenContent \u2192 PostWP \u2192 PostSocial"
}
```
