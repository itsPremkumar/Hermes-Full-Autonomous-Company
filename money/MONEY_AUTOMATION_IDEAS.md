# 💰 MONEY_AUTOMATION_IDEAS.md — Autonomous Money System Roadmap (15 pipelines)

*Master index of every money-automation pipeline in `money/`. Each entry maps a
validated 2026 market idea → a free/open-source tool stack → a drop-in pipeline
that generates ready-to-sell packages + an n8n delivery stub.*

*Deep 2026 market research (20 ideas scored, top 10 cited) lives in
`research/MONEY_IDEAS_2026.md`. This file is the canonical "what to sell" index.*

> All pipelines are 95–99% margin, solo-operable, $0 budget. Regenerate everything:
> `python money/run_all.py` → writes `money/INCOME_DASHBOARD.md`.

---

## The 15 pipelines

| # | Pipeline | What it sells | Price (validated) | Free tool stack | File |
|---|----------|---------------|-------------------|-----------------|------|
| 1 | Fiverr Gig Factory | Done-for-you AI automation gigs | $200–$2,000/gig | n8n + Listmonk + Mautic | `pipeline1_fiverr_gig_factory.py` |
| 2 | Cold-Email Agency | Outreach that converts | $2K–$8K/mo (recurring) | n8n + Listmonk + Mautic | `pipeline2_cold_email_agency.py` |
| 3 | Video Service | AI product/promo videos | $100–$500/video | Remotion + Edge-TTS + CogVideoX | `pipeline3_video_service.py` |
| 4 | Support Bot Deployer | 24/7 AI support bot | $500–$1,500 + $99–$299/mo | Chatwoot + Hermes/OpenClaw | `pipeline4_support_bot.py` |
| 5 | SEO/Audit Reporter | Branded audit PDFs | $49–$199/mo/site | codebase-inspection + secret-scanner + Stirling-PDF | `pipeline5_seo_reporter.py` |
| 6 | Lead-Enrichment SaaS | Clean enriched lead CSVs | $0.10–$0.50/lead or $29–$99/mo | n8n + Crawl4AI + maps-cli | `pipeline6_lead_enrichment.py` |
| 7 | RAG-KB Builder | Private business knowledge base | $1,000–$3,000 + $99–$199/mo | Mem0 + pgvector + Docling + Open WebUI | `pipeline7_rag_kb.py` |
| 8 | Affiliate Farm | Auto affiliate content | recurring | n8n + Listmonk | `pipeline8_affiliate_farm.py` |
| 9 | Invoice Automation | Auto invoicing/reminders | $99–$299 setup + $49/mo | n8n + Stirling-PDF | `pipeline9_invoice_automation.py` |
| 10 | Security Scanner | Site security scan + report | $49–$199/mo | secret-scanner + skill-lint + Stirling-PDF | `pipeline10_security_scanner.py` |
| 11 | Proposal Generator | Tailored proposals/contracts | $50–$300/doc | DocAssemble + Stirling-PDF | `pipeline11_proposal_generator.py` |
| 12 | Social Auto-Poster | 30-day content done-for-you | $300–$800/mo/client | n8n + youtube-content + gif-search + ascii-art | `pipeline12_social_poster.py` |
| 13 | **Voice AI Agent Deployer** ⭐new | 24/7 voice receptionist | $900–$2,000 setup + $299–$799/mo | Piper + Whisper + Chatwoot + n8n | `pipeline13_voice_agent.py` |
| 14 | **Document Automation Service** ⭐new | PDF extract/redact/report | $99–$399 setup + $49–$199/mo | Stirling-PDF + Docling + n8n | `pipeline14_document_automation.py` |
| 15 | **AI Agent Retainer Builder** ⭐new | Monthly autonomous-agent retainer | $2,500–$6,000/mo | n8n + Hermes/OpenClaw + Crawl4AI + pgvector | `pipeline15_agent_retainer.py` |
| 16 | **WhatsApp AI Commerce Agent** ⭐new | WhatsApp catalog/order/lead/support bot | $400–$1,800 setup + $149–$799/mo | Baileys + Chatwoot + n8n + local LLM | `pipeline16_whatsapp_commerce.py` |
| 17 | **AI UGC / Ad-Creative Factory** ⭐new | AI UGC avatar / product / dub / faceless videos | $50–$1,500/video | Remotion + Edge-TTS + CogVideoX + Flowise | `pipeline17_ugc_ad_factory.py` |
| 18 | **Autonomous Backend Agent** ⭐new | Autonomous data/devops/research/CRM agent | $800–$4,000 setup + $299–$1,500/mo | Flowise + n8n + Crawl4AI + pgvector | `pipeline18_backend_agent.py` |

⭐ = discovered + validated by `research/MONEY_IDEAS_2026.md` (see citation table there).
Pipelines 16–18 added in the 2026-07-14 research pass; each passes `python money/pipelineN_ideaname.py self-test`.

---

## How an idea beats an existing one (update rule)

When a new idea's *validated* demand + margin + speed-to-first-dollar beats a
current pipeline, it gets a numbered `pipelineN_*.py` and a row above. The three
2026 additions (13–15) qualified because:
- **Voice agent** — voice-agent market growing 34–39% CAGR to $47.5B; recovers the
  27% of SMB calls lost to unavailable owners (deantek stats).
- **Document automation** — live Fiverr `pdf-automation` category; 95–99% margin on
  self-hosted Stirling-PDF/Docling.
- **Agent retainer** — highest ceiling ($2,500–$6,000/mo, betonai 54-operator rate card).

---

## Activation (no human gate to research; gates only apply if you BUILD)

1. Pick a pipeline → `python money/pipelineN_ideaname.py --list` → `--service/--niche/--vertical`.
2. Paste generated gig copy into Fiverr/Upwork; import the `n8n_workflow` stub.
3. Publish → deliver → upsell to monthly retainer.
4. Queue a promo draft to `revenue/moltbook/` (your scheduler posts it; never auto-posted here).

Regenerate dashboard anytime: `python money/run_all.py`
