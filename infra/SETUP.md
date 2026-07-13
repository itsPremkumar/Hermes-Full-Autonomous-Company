# Infra Setup — Autonomous Money System

Self-hosted stack backing all 12 money pipelines. Free/open-source, zero SaaS fees.

## 1. Prerequisites
- Docker + Docker Compose installed (Linux/macOS/Windows with WSL2)
- A domain (optional but recommended for webhooks: `your-domain.com`)
- `.env` file (copy from template below)

## 2. .env template
```
N8N_USER=admin
N8N_PASS=change-me-strong
PG_PASS=change-me-strong
```

## 3. Launch
```bash
cd infra
cp .env.example .env   # then edit passwords
docker compose up -d
```

## 4. Service URLs (after launch)
| Service | URL | Used by |
|---------|-----|---------|
| n8n | http://localhost:5678 | ALL pipelines (orchestration) |
| Chatwoot | http://localhost:3000 | Pipeline #4 Support Bot |
| Stirling-PDF | http://localhost:8080 | #5 SEO, #10 Security, #11 Proposal (PDF render) |
| Listmonk | http://localhost:9000 | #2 Cold-Email, #9 Invoice (email) |

## 5. Wire a pipeline
Each package JSON in `money/*_packs/` and `money/gigs/` carries an
`n8n_workflow` (or `render_manifest`) block. To activate:
1. Open n8n (localhost:5678) → New Workflow → Paste the nodes from the JSON.
2. Set env vars referenced in the workflow (`$env.MAPS_KEY`, etc.) in n8n Credentials.
3. Activate the workflow. It runs on its cron schedule.

## 6. Backup
```bash
docker compose exec postgres pg_dump chatwoot > backup.sql
docker volume ls | grep _data   # volumes persist across restarts
```

## 7. Cost
- Compute: only your VPS/box (e.g. $5-20/mo Hetzner/Contabo).
- No per-seat SaaS. Margins stay 90-99% as designed.
