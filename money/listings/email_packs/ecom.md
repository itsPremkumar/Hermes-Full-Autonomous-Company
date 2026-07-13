# ecom

**Price:** $500–$500
**Margin:** 95%
**Tags:** 

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process


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
 "name": "cold-email-outreach",
 "nodes": [
  {
   "name": "CRON (daily send)",
   "type": "n8n-nodes-base.cron",
   "position": [
    0,
    0
   ]
  },
  {
   "name": "Enrich leads (Firecrawl/API)",
   "type": "n8n-nodes-base.httpRequest",
   "position": [
    300,
    0
   ]
  },
  {
   "name": "Branch by touch (1/2/3)",
   "type": "n8n-nodes-base.switch",
   "position": [
    600,
    0
   ]
  },
  {
   "name": "Send via Listmonk/Postal",
   "type": "n8n-nodes-base.emailSend",
   "position": [
    900,
    0
   ]
  },
  {
   "name": "Log to Google Sheet/DB",
   "type": "n8n-nodes-base.googleSheets",
   "position": [
    900,
    200
   ]
  },
  {
   "name": "Weekly report (Stirling-PDF)",
   "type": "n8n-nodes-base.code",
   "position": [
    1200,
    0
   ]
  }
 ],
 "connections": {
  "CRON (daily send)": {
   "main": [
    [
     {
      "node": "Enrich leads (Firecrawl/API)",
      "type": "main",
      "index": 0
     }
    ]
   ]
  },
  "Enrich leads (Firecrawl/API)": {
   "main": [
    [
     {
      "node": "Branch by touch (1/2/3)",
      "type": "main",
      "index": 0
     }
    ]
   ]
  },
  "Branch by touch (1/2/3)": {
   "main": [
    [
     {
      "node": "Send via Listmonk/Postal",
      "type": "main",
      "index": 0
     }
    ]
   ]
  },
  "Send via Listmonk/Postal": {
   "main": [
    [
     {
      "node": "Log to Google Sheet/DB",
      "type": "main",
      "index": 0
     }
    ]
   ]
  }
 },
 "tools": "n8n + Listmonk + Postal + Stirling-PDF (all free/self-hosted)",
 "note": "Replace enrich + send nodes with client's real list & domain."
}
```
