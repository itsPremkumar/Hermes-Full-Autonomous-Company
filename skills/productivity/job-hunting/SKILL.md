---
name: job-hunting
description: End-to-end job-hunting pipeline for a fresher/switcher targeting high-salary remote roles — GitHub readiness, resume, FREE-board search, supervised apply, and portfolio-project building. Use whenever the user wants to find/get a job, apply to roles, build a portfolio project to improve offers, or asks about auto-apply/browser-takeover for jobs.
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [job-hunting, career, resume, github, remote-work, fresher, apply]
---

# Job Hunting (fresher → high-salary remote)

## When to use
- "find me a job", "search for jobs", "apply for jobs", "high salary package", "remote job"
- Building a unique portfolio project to boost offers
- GitHub/resume audit for job readiness

## The pipeline (in order)
1. **GitHub readiness** — audit repos; fix CI green; pin 2–3 flagship projects; write a one-lane profile README ("AI/ML & Backend Engineer · open to work"). Related skill: `github-job-readiness`.
2. **Resume** — one-page, ATS-friendly, lead with real projects + proof (stars, commits, test counts). Keep as LaTeX or Markdown; the agent CANNOT run LaTeX — user compiles to PDF.
3. **Search FREE boards ONLY** (see Pitfall 1).
4. **Supervised apply** — agent drafts/shortlists; human submits. Never mass auto-apply (Pitfall 2).
5. **Portfolio project** — build a unique, real, agentic/dev-tools project (see references/agentic-copilot.md).

## Core principles
- **Quality over quantity.** Targeted applications beat spray-and-pray. A 20★ project + green CI + OSCG mentor > 100 generic applications.
- **Free boards only.** Never pay to apply; legit employers pay YOU.
- **Supervised, not autonomous, apply.** Agent searches/shortlists/drafts; human does the submit click. Safe from ToS bans + ATS filtering.
- **Salary reality (India fresher 2025):** AI/ML ₹6–12 LPA remote is realistic; >₹20 LPA "no experience needed" = scam. Target ₹6 LPA min, ₹8–12 LPA if AI-specific.

## PITFALL 1 — paid job boards
RemoteOK (and similar) gate salary behind **PAID Premium** and push paid tiers to apply. **Do NOT recommend RemoteOK as an apply channel.** User explicitly flagged this ("POSTTAL IS PAID FOR APPLYING"). Use only FREE channels:
- **Naukri** — free, India's biggest board (656+ fresher AI/ML remote jobs). `https://www.naukri.com/ai-ml-jobs?k=...&l=india&jobType=remote`
- **LinkedIn** — free Easy Apply (1,000+ GenAI India, 632 remote). `https://in.linkedin.com/jobs/remote-jobs-for-generative-ai-jobs`
- **Wellfound** — free, founder-direct; CAPTCHA-walled (user solves in own browser). `https://wellfound.com/role/r/ai-engineer`
- **RemoteAI** — free remote AI/ML India. `https://remoteai.io/v2/jobs/ai-ml-engineering`
- **YC Work at a Startup** — free, skill-based. `https://www.workatastartup.com/`

### How to pull LIVE counts/roles without a browser (verified technique)
Google is blocked via Jina (`r.jina.ai/https://www.google.com/...` 403s). Use instead:
- **DuckDuckGo HTML via Jina** (works): `curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=<query>"`
  returns real aggregator counts (e.g. Naukri 656, foundit 11414, LinkedIn 1000+) and snippet links.
- **Jina direct on a board's index** for postings: `curl -s "https://r.jina.ai/https://remoteai.io/v2/jobs/ai-ml-engineering"`.
- Build `JOB_SHORTLIST.md` from these (Tier-1/Tier-2 + direct apply links + tailored cover note).
- Never scrape behind login/paywall; never invent counts — only report what the fetch returned.

## PITFALL 2 — "agent takes over and auto-applies"
User will ask for full browser takeover / auto-apply bots. Decline the banned-bot pattern:
- LinkedIn/Naukri/Indeed ToS forbid automated applying → account ban.
- CAPTCHA/2FA + login walls break scripts; agent must never type passwords.
- Mass generic applying gets ATS-filtered; wastes a strong profile.
Offer instead: (a) search+shortlist+tailor via agent, (b) user logs in + submits 30s/role, (c) supervised browser fill with user watching. Note: even computer-use may fail to drive the user's Chrome on some Windows setups (compositing limitation) — don't promise it.

## Deliverables the agent produces
- `JOB_SHORTLIST.md` — Tier-1/Tier-2 roles with direct links + tailored cover note
- `RESUME_*.tex` — improved LaTeX resume
- Portfolio repo (e.g. agentic copilot) — see references/agentic-copilot.md

## References
- references/agentic-copilot.md — recipe for the local-first agentic job-hunt copilot TS project (RAG-lite scoring, MCP server, CLI, green CI)
- references/free-boards.md — current free board URLs + filters
