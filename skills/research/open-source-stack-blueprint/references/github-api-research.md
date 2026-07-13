# GitHub API Research Technique + Verified Knowledge Bank

## Technique: pull live stars/license via API
Unauthenticated, ~20 req/min per IP. Batch and space calls. When 403 hits, mark repos
`(canonical)` and note "not re-verified this session."

```bash
# single repo
curl -sL "https://api.github.com/repos/OWNER/REPO" | python -c "
import sys,json
d=json.load(sys.stdin)
print(d.get('full_name'), '|', d.get('stargazers_count'), '|', (d.get('license') or {}).get('spdx_id'), '|', (d.get('description') or '')[:60])
"

# search
curl -sL "https://api.github.com/search/repositories?q=QUERY&sort=stars&per_page=10" | python -c "
import sys,json
d=json.load(sys.stdin)
for i in d.get('items',[]): print(i['full_name'],'|',i.get('stargazers_count'),'|',(i.get('description') or '')[:60])
"

# verify link resolves
curl -s -o /dev/null -w "%{http_code}" "https://github.com/OWNER/REPO"   # expect 200
```

User-Agent header sometimes bypasses 403 (marginal). Sleep 1–1.5s between calls.

## Verified project knowledge bank (stars pulled live, this session)
Format: `owner/repo | ★ | license | role`. ✅ = verified. Re-verify if stale.

### Agent frameworks / orchestration
- NousResearch/hermes-agent | 212k | — | self-improving agent (main post)
- crewAIInc/crewAI | 55.3k | MIT | role-based multi-agent
- FoundationAgents/MetaGPT | 69.3k | MIT | "AI software company"
- microsoft/autogen | 59.6k | CC-BY-4.0 | multi-agent conversation
- langchain-ai/langgraph | 37k | MIT | resilient stateful workflows
- OpenHands/OpenHands | 80.3k | Open | autonomous SWE
- GreenSheep01201/claw-empire | 1.3k | Apache-2.0 | CEO desk orchestration
- markus-global/markus | 166 | AGPL-3.0 | OS for AI workforces
- swarmclawai/swarmclaw | 610 | — | self-hosted multi-agent runtime
- mergisi/awesome-openclaw-agents | 3.8k | — | 162 agent templates

### Research / crawling / browser
- Panniantong/Agent-Reach | 54.3k | MIT | web+social scrape, zero API fee
- firecrawl/firecrawl | 148.8k | AGPL-3.0 | AI web search/scrape/extract
- unclecode/crawl4ai | 72.2k | Apache-2.0 | local-first LLM crawling
- browser-use/browser-use | 104.1k | MIT | AI browser control
- searxng/searxng | 33.7k | AGPL-3.0 | private metasearch
- scrapy/scrapy | 63.1k | BSD-3 | large-scale crawling
- apify/crawlee | 24.6k | Apache-2.0 | JS crawler

### Memory / knowledge
- mem0ai/mem0 | 60.5k | Apache-2.0 | long-term memory layer
- getzep/graphiti | 28.6k | Apache-2.0 | real-time knowledge graph
- open-webui/open-webui | 144.9k | Open | knowledge portal
- docling-project/docling | 62.9k | MIT | document parsing
- pgvector/pgvector | 22.1k | — | vector search for Postgres
- postgres/postgres | 21.4k | — | database

### Automation / app / workflow
- n8n-io/n8n | 195.9k | — | workflow automation
- langgenius/dify | 148.4k | — | agentic app platform
- FlowiseAI/Flowise | 54.5k | — | visual AI workflows
- nocobase/nocobase | 23.3k | — | no-code CRM builder

### Voice / telecalling
- dograh-hq/dograh | 4.8k | BSD-2-Clause | open voice AI (Vapi alt)
- pipecat-ai/pipecat | 13.3k | BSD-2-Clause | voice/multimodal framework
- livekit/livekit | 19.7k | Apache-2.0 | realtime comms
- openai/whisper | 104.7k | MIT | speech recognition
- rhasspy/piper | 11.2k | MIT | local TTS
- PatterAI/Patter | 953 | — | voice SDK

### CRM / ERP / finance
- frappe/erpnext | 36.7k | GPL-3.0 | ERP (accounting/HR/CRM)
- odoo/odoo | 52.9k | — | ERP suite
- twentyhq/twenty | 52.7k | — | open Salesforce alt
- InvoicePlane/InvoicePlane | 3.1k | — | invoicing
- Peppermint-Lab/peppermint | 3.1k | — | help desk

### Marketing / support / email
- mautic/mautic | 10.1k | — | marketing automation
- knadh/listmonk | 22k | AGPL-3.0 | newsletter
- chatwoot/chatwoot | 34.3k | — | live chat / support
- Sharkord/sharkord | 1.4k | — | community/voice server

### Infra / IAM / observability
- keycloak/keycloak | 35.6k | Apache-2.0 | IAM/SSO
- Infisical/infisical | 27.8k | — | secrets mgmt
- coollabsio/coolify | 58.2k | Apache-2.0 | self-host PaaS
- minio/minio | 61.3k | AGPL-3.0 | S3 object storage
- grafana/grafana | 75.5k | AGPL-3.0 | dashboards
- SigNoz/signoz | 28.7k | — | observability
- langfuse/langfuse | 30.9k | — | LLM evals/observability
- metabase/metabase | 48.1k | — | BI
- wazuh/wazuh | — | GPL | SOC/SIEM
- Agno-AGI/agno | 41.1k | Apache-2.0 | agent platform

### Video / design (user's domain)
- itsPremkumar/Automated-Video-Generator | MIT | faceless script→video, MCP-ready (Product #1)
- zai-org/CogVideo | 12.9k | — | text→video model
- Penpot/penpot | — | — | open UI/UX design
- comfyanonymous/ComfyUI | — | — | image+video gen
- mohyware/clip-js | 748 | — | Remotion video editor

### E-commerce
- medusajs/medusa | 35.1k | MIT | Shopify alt
- saleor/saleor | 22k | BSD-3 | GraphQL e-commerce
- vendure-ecommerce/vendure | 6k | MIT | TS e-commerce

## Concept-only (do NOT treat as production)
- Paperclip Maximus — recursive self-improvement *idea*, no mature repo.

## Self-evolving architecture (for AI-agent companies)
Hermes (main, self-improving) + Mem0 (memory evolution) + Graphiti (knowledge evolution)
+ AgentZero (autonomous sub-agent spawning) → orchestrators (claw-empire/CrewAI/LangGraph) on top.
True self-evolution is research-grade; combine, don't bet on one.
