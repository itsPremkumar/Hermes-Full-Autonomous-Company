---
name: job-hunt-agent
description: >-
  Autonomous job-hunting pipeline for a software/AI fresher: audit + fix GitHub
  repos (CI, descriptions, flagship pinning), improve a LaTeX resume, search real
  remote jobs (India/global) via Jina+DDG when Exa is down, and run a SUPERVISED
  apply flow. Encodes the hard limits (no banned auto-apply bots, login wall is the
  user's, the browser_navigate session is invisible to the user) so the agent sets
  expectations correctly instead of looping on a dead end.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
---

# Job-Hunt Agent (fresher SWE / AI)

End-to-end workflow to make a fresher job-ready and surface real remote roles.
Covers: GitHub audit/fix → resume (LaTeX) → remote job search → supervised apply.

## Triggers
- "help me get a [high-salary / remote] job", "search jobs for me", "prepare my
  GitHub/resume for hiring", "apply for jobs automatically".
- User shares a GitHub profile and wants it job-ready.
- User wants an agent to "take over the browser and apply".

## PHASE 0 — Set expectations FIRST (do this before any tool call)
The user will often demand a "fully autonomous agent that applies to everything".
State the truth up front to avoid burning the session:
1. **No banned auto-apply bot.** Mass automated applying violates LinkedIn/Naukri/
   Indeed/Wellfound ToS → account ban; ATS filters blast applications; it wastes a
   strong profile. Offer a *supervised* flow instead.
2. **The browser I drive (`browser_navigate`) is a remote/headless session the user
   CANNOT see or type into.** Never say "log in in my browser" as if they can — they
   can't. If login is needed, tell them to open their OWN browser.
3. **The login wall (password / 2FA / CAPTCHA) is the user's step.** The agent never
   types passwords or solves CAPTCHA (hard rule in computer-use skill too).

## PHASE 1 — GitHub audit + fix (see `github-job-readiness` skill)
- Rank repos by stars/commits; pick 1–2 real, user-backed **flagships** and make them
  mandatory. For this user: `Automated-Video-Generator` (20★, TypeScript/Remotion) +
  `sproutern-open-source` (live Next.js, 367 tests green).
- Verify CI is **green** via API (`actions/runs`) AND check-runs (a green workflow can
  still show a red commit ✗ from one failing job — e.g. a flaky `Render E2E`). Fix by
  making heavy/flaky jobs non-blocking or skip-mode.
- Add a **repo description** (needs a token / user does it in UI — API 401 unauth).
- Rewrite profile README to a single lane + "🟢 Open to work".

## PHASE 2 — Resume (LaTeX) improvement
See `references/resume-improvement.md` + `templates/RESUME_improved.tex`.
Key fixes: "graduate" not "student"; add grad year + CGPA (if ≥7.5); lead with the two
flagships and their proof (stars/commits/test counts); add OSCG mentor; align skills to
the REAL stack; drop weak projects to hold one page. Keep the user's LaTeX style.

## PHASE 3 — Remote job search (no login needed)
Use the **Jina + DuckDuckGo HTML** technique (Exa/mcporter is often broken here):
```bash
Q="remote AI ML engineer india fresher salary"
enc=$(python -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$Q")
curl -s "https://r.jina.ai/https://html.duckduckgo.com/html/?q=$enc" \
  | grep -oE '\\[[^]]+\\]\\(https://duckduckgo.com/l/\\?uddg=[^)]+\\)'
```
### ⚠️ Only recommend boards that are FREE for candidates.
If a board charges candidates (even partially, e.g. salary hidden behind Premium, or
"unlock applications" fees), DO NOT list it. Mark it clearly as PAID or skip entirely.

**FREE boards (safe to recommend):**
- **Naukri** — India's biggest board, free for candidates. Browse/apply without login.
- **LinkedIn** — Easy Apply is free. Needs login (user's step), but highest volume.
- **Wellfound** — free profile → apply to many startups, founder-direct hiring.
- **RemoteAI** — remoteai.io/v2/jobs/ai-ml-engineering (and NLP/Prompt Engineering)
- **YC Work at a Startup** — free, skill-based hiring at YC startups.

**AVOID (PAID for candidates):**
- **RemoteOK** — salary hidden behind Premium. Applying from there routes through paid
  layers. Do not recommend as an apply channel.

Save a curated `JOB_SHORTLIST.md` with direct links + a tailored cover note built from
the user's flagships. Include only FREE boards.

## PHASE 4 — Supervised apply (the only legit "auto-apply")
- **Preferred:** user applies manually from `JOB_SHORTLIST.md` (30 sec/role). Agent did
  the search + targeting + pitch.
- **If user insists on agent-driven browser:** enable computer-use (`computer_use`
  tool), launch the user's real Chrome, **pause for the user to log in**, then fill +
  submit one role at a time with the user watching.
- **Pitfall — computer-use may not enumerate Chrome on Windows:** if
  `capture app="Google Chrome"` returns 0 elements even though the window exists
  (cua-driver only sees the desktop layer), STOP debugging and fall back to manual
  apply. The login wall is the user's step anyway, so the automation gain is small.

## Pitfalls
- **Only recommend FREE job boards.** Never suggest boards where candidates need to
  pay/premium for salary info or applying (RemoteOK, Premium-locked boards, "resume
  unlock" fee schemes). Free only: Naukri, LinkedIn, Wellfound, RemoteAI, YC Work at
  a Startup.
- Don't loop on making `browser_navigate` "visible" to the user — it's headless.
- Don't promise "high salary" to a fresher beyond market reality (India AI/ML fresher
  ₹6–12 LPA; anything >₹20 LPA "no experience" is a scam).
- Don't paste a password into chat to "log in for them" — security + ban risk.
- Exa/mcporter is unreliable here; default to Jina+DDG, not a failed retry loop.

## References
- `references/remote-job-search.md` — Jina+DDG recipe, board list, salary reality.
- `references/resume-improvement.md` — fresher LaTeX resume fix checklist.
- `templates/RESUME_improved.tex` — copyable improved resume template.
