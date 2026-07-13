# I will build a RAG knowledge base + AI assistant for your SaaS

**Price:** $500 setup + $149/mo
**Margin:** 92%
**Tags:** rag, knowledge base, ai assistant, saas rag, chatbot, llm

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- 1. Ingest docs, help center, changelog
- 2. Chunk + embed (local model, free)
- 3. Deploy RAG on Hermes/OpenClaw + API
- 4. Wire to Slack/website widget
- 5. 14-day tuning + monthly refresh

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
 "name": "rag-kb-build",
 "nodes": [
  {
   "type": "n8n-nodes-base.scheduleTrigger",
   "name": "WeeklyIngest",
   "params": {
    "interval": [
     {
      "field": "cronExpression",
      "expression": "0 4 * * 1"
     }
    ]
   }
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "FetchDocs",
   "params": {
    "url": "={{$env.DOCS_URL}}",
    "httpMethod": "GET"
   }
  },
  {
   "type": "n8n-nodes-base.code",
   "name": "Chunk",
   "code": "const txt = (items[0].json.body||'');\nconst chunks = txt.match(/[^.\\n]{80,500}[.\\n]/g)||[txt];\nreturn chunks.map(c => ({json: {text: c}}));"
  },
  {
   "type": "n8n-nodes-base.httpRequest",
   "name": "EmbedStore",
   "params": {
    "url": "={{$env.RAG_API}}/ingest",
    "httpMethod": "POST"
   }
  }
 ],
 "connections": "WeeklyIngest \u2192 FetchDocs \u2192 Chunk \u2192 EmbedStore"
}
```
