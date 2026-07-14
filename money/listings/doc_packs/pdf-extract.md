# I will automate PDF extraction & data entry with free open-source tools

**Price:** $149/gig
**Margin:** —%
**Tags:** pdf automation, data extraction, invoice processing, stirling pdf, docling, n8n, document automation, pdf to excel

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- **Basic** ($37, 3 days): Single template; 1 workflow; Email support
- **Standard** ($149, 5 days): Setup + test; Up to 3 templates; Loom walkthrough; 7-day support
- **Premium** ($298, 7 days): Full system; Unlimited templates; Monthly retainer option; Priority support

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
 "name": "deliver-doc-pdf-extract",
 "nodes": [
  {
   "parameters": {},
   "name": "Webhook (intake)",
   "type": "n8n-nodes-base.webhook",
   "typeVersion": 1,
   "position": [
    0,
    0
   ]
  },
  {
   "parameters": {},
   "name": "Stirling-PDF / Docling transform",
   "type": "n8n-nodes-base.code",
   "typeVersion": 1,
   "position": [
    300,
    0
   ]
  },
  {
   "parameters": {},
   "name": "Deliver + notify",
   "type": "n8n-nodes-base.emailSend",
   "typeVersion": 1,
   "position": [
    600,
    0
   ]
  }
 ],
 "connections": {
  "Webhook (intake)": {
   "main": [
    [
     {
      "node": "Stirling-PDF / Docling transform",
      "type": "main",
      "index": 0
     }
    ]
   ]
  },
  "Stirling-PDF / Docling transform": {
   "main": [
    [
     {
      "node": "Deliver + notify",
      "type": "main",
      "index": 0
     }
    ]
   ]
  }
 },
 "note": "Tools: Stirling-PDF + Docling + n8n + your doc-extractor skill \u2014 all free/self-hosted. Replace code node with your doc logic."
}
```
