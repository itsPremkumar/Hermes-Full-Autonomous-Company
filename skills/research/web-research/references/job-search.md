# Job Search (live, no API key) + Apply Policy

## Search recipe (proven this session, India fresher/remote)
```bash
q="remote AI ML engineer India work from home salary"
enc=$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$q")
curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=$enc" \
  | grep -oE '\[[^]]+\]\(https://duckduckgo.com/l/\?uddg=[^)]+\)'
```
Scope queries with job-board sites:
- `site:linkedin.com/jobs` — LinkedIn India (e.g. `remote developer jobs`, `generative ai jobs for freshers`)
- `site:naukri.com` — Naukri fresher AI/ML
- `site:wellfound.com` — startups, apply with one profile, talk to founders (best upside for proof-based candidates)
- `site:weworkremotely.com` / `site:remoteok.com` — curated remote
- `site:foundit.in` / `site:glassdoor.co.in` — aggregates + salary data

Real numbers seen this session: LinkedIn 3,000+ remote dev (India), Indeed 50 Chennai
AI/ML fresher + 162 Bangalore SDE trainee, foundit 11,414 Fresher AI/ML, Glassdoor 197 ML
fresher, Wellfound 1,000+ remote AI engineer.

## CRITICAL: headless browser reality (learned this session)
- Hermes `browser_*` tools drive a **headless Chromium in the backend** — the USER CANNOT
  SEE IT OR TYPE INTO IT. "Log in in my browser" / "open my browser so I can log in" is
  IMPOSSIBLE for the user. Never promise it.
- Any login-gated flow needs the user to PASTE creds into chat (risky: password lands in the
  transcript; LinkedIn may throw 2FA/CAPTCHA the agent can't solve) OR be done on a no-login
  board. Prefer no-login sources (RemoteOK index, RemoteAI) over LinkedIn headless login.

## Board-specific reality (verified this session)
- **Wellfound** direct page (`wellfound.com/role/r/ai-engineer`): DataDome CAPTCHA via BOTH
  the `browser_*` session AND Jina Reader. BLOCKED headless. BUT its postings are INDEXED by
  DDG — surface them via `site:wellfound.com` search; open the specific link in the USER's
  own browser.
- **RemoteOK** deep links (`/remote-jobs/remote-ai-engineer`): 404 via Jina. The INDEX
  `remoteok.com/remote-jobs-in-india` WORKS (~207 India results) and lists real postings with
  apply links. Salary hidden behind Premium — verify on the posting.
- **RemoteAI** (`remoteai.io/v2/jobs/ai-ml-engineering`): loads via Jina, no login. Best
  dedicated remote-AI board for India. Also `…/nlp-prompt-engineering` (LLM/RAG fit).
- **LinkedIn** jobs search: only works logged-in; headless login needs user creds (see above).
  Highest volume (3,000+ remote dev; 1,000+ GenAI fresher).
- **Glassdoor / foundit / Indeed**: indexed results fine; apply needs login.

## Salary reality (India fresher, 2025 grad)
- AI/ML Engineer fresher: ~₹6–12 LPA (avg GenAI ≈ ₹9.9 LPA). Senior 60–90 LPA+.
- "High salary" as a fresher realistically = ₹6–12 LPA remote. Anything promising ₹20+ LPA
  to a fresher with no prior job is almost always a scam/MLM — do NOT point users at those.
- Remote work-from-home is the user's stated preference (Tamil Nadu, India).

## APPLY POLICY — do NOT auto-submit
- Searching + shortlisting + tailored cover notes: YES.
- Bot auto-applying (fill forms + submit at scale): NO. Reasons: LinkedIn/Naukri/Indeed ToS
  ban, CAPTCHA/login walls, ATS filters out spam. Hurts a strong candidate.
- Supported semi-auto: user (or agent driving the user's already-logged-in browser, with user
  watching) submits each role (~30s each). "Human at the wheel", not a banned bot.
- If user wants scale, an Apify token can scrape listings (search only) — still user applies.

## Tailored cover note pattern (per role, swap [Company])
Subject: Application — AI/ML Engineer (Remote) | <Name>
Hi [Company] team,
I'm <Name>, a 2025 B.Tech IT graduate who builds production AI systems end to end.
I maintain <flagship repo, stars> — <one-line what it does + green CI / test count>.
Also <second proof: OSCG mentor / Stable Diffusion pipeline>.
Looking for a remote AI/ML (or backend) role to ship real product. Resume: <github>.
Best, <Name>
(Keep 8–10 lines. Lead with the 2-3 pinned flagships, real numbers.)
