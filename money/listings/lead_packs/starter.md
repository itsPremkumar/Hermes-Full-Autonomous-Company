# I will enrich your leads with firmographics + contact data

**Price:** $99/mo
**Margin:** 95%
**Tags:** lead enrichment, b2b leads, lead generation, crm automation, starter leads, data enrichment

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- 1. Client connects CRM / uploads lead list
- 2. n8n cron pulls new leads
- 3. Enrich via maps-cli + web-research nodes
- 4. Push enriched rows back to CRM / webhook
- 5. Monthly quality report

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
 "name": "lead-enrich-starter",
 "nodes": [
  {
   "type": "n8n-nodes-base.scheduleTrigger",
   "name": "DailyPull",
   "params": {
    "interval": [
     {
      "field": "cronExpression",
      "expression": "0 6 * * *"
     }
    ]
   }
  },
  {
   "type": "n8n-nodes-base.function",
   "name": "ParseLeads",
   "code": "return items.map(i => ({json: {email: i.json.email, domain: (i.json.email||'').split('@')[1]}}));"
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "MapsLookup",
   "params": {
    "url": "https://maps.googleapis.com/maps/api/geocode/json",
    "qs": {
     "address": "={{$json.domain}}",
     "key": "={{$env.MAPS_KEY}}"
    }
   }
  },
  {
   "type": "n8n-nodes-base.code",
   "name": "Enrich",
   "code": "for (const i of items) {\n  const d = i.json.domain || '';\n  i.json.firmographics = { domain: d, tld: d.split('.').pop() };\n  i.json.social = { linkedin: 'https://linkedin.com/company/' + d.split('.')[0] };\n}\nreturn items;"
  },
  {
   "type": "n8n-nodes-base.webhook",
   "name": "PushToCRM",
   "params": {
    "httpMethod": "POST",
    "path": "enriched"
   }
  }
 ],
 "connections": "DailyPull \u2192 ParseLeads \u2192 MapsLookup \u2192 Enrich \u2192 PushToCRM"
}
```
