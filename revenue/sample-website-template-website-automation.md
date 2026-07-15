# Sample Reference: Website Automation Suite (another complete website template)

> **Canonical source of truth:** `Hermes-Full-Autonomous-Company`
> **Sibling flagship:** `sproutern` (Next.js + Firebase + Genkit daily loop)
> **This sample:** `website-automation-public` — a *second, complete* website template
> for the autonomous money-earning system, built for speed and zero hosting cost.

**Repo:** https://github.com/itsPremkumar/website-automation-public
**Full doc:** `ARCHITECTURE.md` in that repo.

---

## Where it fits in the money stack

| Layer | `sproutern` (flagship) | `website-automation` (this sample) |
|-------|-------------------------|--------------------------------------|
| Stack | Next.js 16 + Firebase + Genkit | Static HTML/CSS/JS + GitHub Pages |
| Cost | Hosting + domain | **$0** (GitHub Pages free) |
| Strength | Rich app, auth, AI daily loop | Fast, lightweight, many sites at once |
| Monetization | AdSense (rejected: thin content) → Monetag fallback | Monetag zone, config-driven |
| Automation | Genkit daily content loop | `self-improve.js` measure→improve→deploy loop |
| Best use | Flagship product site | **Site farm / niche portfolio** |

Use **both**: `sproutern` as the flagship, `website-automation` to spin up a
portfolio of supporting niche sites that feed traffic + ad inventory — all
autonomous, all from one template.

---

## What "complete website template" means here

This is a finished, secure, autonomous engine — not a stub:

- ✅ Build from one master template → many branded, SEO-ready sites
- ✅ Deploy to GitHub Pages (auto repo create + Pages enable + verify)
- ✅ **Self-improving loop**: measures each site daily, applies the single
  weakest fix (content, title, meta, JSON-LD, sitemap), deploys, logs
- ✅ Original 800+ word content generator (avoids AdSense thin-content reject)
- ✅ Config-driven Monetag ad zone (no hardcoded third-party IDs)
- ✅ Security: token git-ignored, `.env.example` only, `SECURITY.md`, clean history
- ✅ MIT licensed, `npm test` passing

---

## Honest money model (no guaranteed-income claims)

| Stage | Mechanism | Gate |
|-------|-----------|------|
| Build & host | GitHub Pages | none |
| Content | `lib/content.js` | quality bar |
| Traffic | SEO | **algorithmic** |
| Monetize | Monetag (AdSense fallback) | **ad approval** |
| Payout | ad network | **payment + threshold** |

The loop improves *system quality* (content/SEO/sitemap/structured data) — the
inputs search engines reward. Revenue depends on traffic + ad approval, which
remain external gates. **No automatic money; operation works, booked revenue
starts at $0 until payout.**

---

## How to run (autonomous)

```bash
git clone https://github.com/itsPremkumar/website-automation-public
cd website-automation-public && npm install
cp .env.example .env          # add a fine-grained PAT (repo + Pages)
npm run deploy -- my-niche "My Niche" "desc" "#6366f1"
npm run content -- my-niche 5  # 5 original posts
npm run loop                   # daily self-improve (add to crontab, see cron.example)
```

See `ARCHITECTURE.md` in the repo for the full system diagram, component
reference, and security model.

---

*This file is a sample reference inside the Hermes-Full-Autonomous-Company
revenue playbook. It links an external, complete website template as a
practical building block for the autonomous money-earning system.*
