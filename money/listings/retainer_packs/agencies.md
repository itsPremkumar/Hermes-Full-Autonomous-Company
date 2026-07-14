# I will run a monthly AI-agent retainer for your marketing agency

**Price:** $3000/gig
**Margin:** —%
**Tags:** ai agent, agency automation, n8n, lead research, content automation, outreach, ai retainer

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- **Pilot** ($1000, 1 week): 1 agent; Core workflow; Email support; Weekly report
- **Growth** ($3000, 1 week): 2–3 agents; CRM/marketplace hooks; Loom updates; Monthly call
- **Scale** ($6000, 2 weeks): Unlimited agents; Full autonomy; Priority support; Quarterly roadmap

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
 "name": "deliver-agent-agencies",
 "nodes": [
  {
   "parameters": {},
   "name": "Schedule / Webhook (trigger)",
   "type": "n8n-nodes-base.webhook",
   "typeVersion": 1,
   "position": [
    0,
    0
   ]
  },
  {
   "parameters": {},
   "name": "Hermes agent (reason + act)",
   "type": "n8n-nodes-base.code",
   "typeVersion": 1,
   "position": [
    300,
    0
   ]
  },
  {
   "parameters": {},
   "name": "Deliver + log to pgvector",
   "type": "n8n-nodes-base.code",
   "typeVersion": 1,
   "position": [
    600,
    0
   ]
  }
 ],
 "connections": {
  "Schedule / Webhook (trigger)": {
   "main": [
    [
     {
      "node": "Hermes agent (reason + act)",
      "type": "main",
      "index": 0
     }
    ]
   ]
  },
  "Hermes agent (reason + act)": {
   "main": [
    [
     {
      "node": "Deliver + log to pgvector",
      "type": "main",
      "index": 0
     }
    ]
   ]
  }
 },
 "note": "Tools: n8n + Hermes/OpenClaw + Crawl4AI + pgvector + Listmonk \u2014 all free/self-hosted. Replace code node with your agent logic."
}
```
