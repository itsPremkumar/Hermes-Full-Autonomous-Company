# Free job boards (India, remote, fresher) — current URLs

NO paid/Premium boards. Legit employers pay the candidate, never the reverse.

## Naukri (free, India biggest)
- Search: `https://www.naukri.com/ai-ml-jobs?k=artificial%20intelligence%20machine%20learning&l=india&jobType=remote`
- Filter: Experience 0-1 yrs, Job Type Remote, sort by salary.
- ~656 fresher AI/ML remote jobs seen live.

## LinkedIn (free Easy Apply)
- GenAI India: `https://in.linkedin.com/jobs/generative-ai-engineer-jobs`
- Remote filter: `https://in.linkedin.com/jobs/remote-jobs-for-generative-ai-jobs`
- Filters: Location=India, Work type=Remote, Experience=Entry level.
- ~1,000+ GenAI India, 632 remote (live).

## Wellfound (free, founder-direct)
- `https://wellfound.com/role/r/ai-engineer` — one profile -> many startups.
- CAPTCHA-walled (DataDome) -> user solves in own browser. High upside for
  open-source-cred candidates (founders hire on proof, not college brand).

## RemoteAI (free, remote AI/ML India)
- `https://remoteai.io/v2/jobs/ai-ml-engineering`
- Also `https://remoteai.io/v2/jobs/nlp-prompt-engineering` (LLM/RAG strength).

## YC Work at a Startup (free)
- `https://www.workatastartup.com/` -> filter Remote + Engineering.

## Search technique (no login, agent-side)
- Exa/mcporter often broken (node runtime) in this env — use Jina Reader:
  `curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=QUERY"`
  then `grep -oE '\[[^]]+\]\(https://duckduckgo.com/l/\?uddg=[^)]+\)'`.
- Google direct via Jina is JS-redirect blocked; DuckDuckGo HTML works.
- RemoteOK own pages are CAPTCHA-walled too (don't rely on it; and it's paid).

## Salary reality (India fresher 2025)
- AI/ML fresher Rs 6-12 LPA remote realistic; senior Rs 60-90 LPA+.
- Target >=Rs 6 LPA; skip <Rs 3 LPA unless great learning. >Rs 20 LPA no-exp = scam.
