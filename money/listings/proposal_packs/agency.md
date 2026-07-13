# I will craft agency service proposals that close

**Price:** $400/gig
**Margin:** 96%
**Tags:** proposal writer, business proposal, agency proposal, freelance, RFP, sales

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- 1. Client fills brief (form)
- 2. n8n pulls brief → template engine
- 3. Generate proposal MD (your templates)
- 4. Lint + render PDF (Stirling-PDF)
- 5. Deliver + reusable template saved

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
 "name": "proposal-gen",
 "nodes": [
  {
   "type": "n8n-nodes-base.webhook",
   "name": "BriefIn",
   "params": {
    "httpMethod": "POST",
    "path": "brief"
   }
  },
  {
   "type": "n8n-nodes-base.code",
   "name": "FillTemplate",
   "code": "const b = items[0].json;\nconst md = `# Proposal for ${b.client}\\n\\n## Scope\\n${b.scope}\\n\\n## Price\\n$${b.price}`;\nreturn [{json: {md, email: b.email}}];"
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
 "connections": "BriefIn \u2192 FillTemplate \u2192 RenderPDF"
}
```
