# Remote Job Search (fresher / India / WFH) — recipe + reality

## Live search (no API key; Exa/mcporter is broken here)
```bash
Q="remote AI ML engineer india fresher salary"
enc=$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$Q")
curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=$enc" \
  | grep -oE '\\[[^]]+\\]\\(https://duckduckgo.com/l/\\?uddg=[^)]+\\)'
```
Scope with: `site:linkedin.com/jobs`, `site:naukri.com`, `site:wellfound.com`,
`site:weworkremotely.com`, `site:foundit.in`, `site:glassdoor.co.in`.

## ⚠️ FREE boards ONLY — never recommend PAID boards
Only suggest boards where applying is FREE for candidates. If a board requires
Premium to see salary or to apply, flag it as PAID and DO NOT list it as an apply
channel.

### ✅ FREE (safe to recommend)
- **Naukri** — India's biggest job board. Free for candidates. Browse + apply.
- **LinkedIn** — Easy Apply is free. Highest volume (3,000+ remote dev India;
  1,000+ GenAI fresher). Needs login (user's step).
- **Wellfound (AngelList Talent)** — free profile → apply to many startups;
  founders hire on GitHub proof. DataDome CAPTCHA blocks headless — open in the
  USER's own browser.
- **RemoteAI** — remoteai.io/v2/jobs/ai-ml-engineering (loads via Jina, no login;
  also .../nlp-prompt-engineering for LLM/RAG fit).
- **YC Work at a Startup** — free, skill-based hiring at YC companies.

### ❌ PAID / Verify before recommending
- **RemoteOK** — RemoteOK's own page is CAPTCHA-walled; salary hidden behind
  Premium tier. Some listings may be free to browse but NOT free to apply. Do NOT
  recommend as a primary apply channel. Only use for leads that the user verifies
  on the posting itself.
- **Glassdoor** — free to browse but some features gated. Use for salary research.
- **Jooble / foundit / Indeed** — free to browse; verify the specific posting
  isn't behind a paywall before sending user to apply.

## Salary reality (India 2025 fresher)
- AI/ML fresher Rs.6-12 LPA (avg GenAI ~Rs.9.9 LPA); senior 60-90 LPA+.
- "High salary" as fresher = Rs.6-12 LPA remote. Rs.20+ LPA "no experience" = scam.

## Apply policy
- Search + shortlist + tailored cover note: YES.
- Bot auto-submit at scale: NO (ToS ban, CAPTCHA, ATS spam-filtering).
- Supported: user applies manually (30s/role) from a `JOB_SHORTLIST.md`, or agent drives
  the user's logged-in browser WITH the user watching (login is the user's step).
