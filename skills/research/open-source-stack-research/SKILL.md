---
name: open-source-stack-research
description: Build a verified open-source tool/agent stack for a given function or company blueprint. Use when a user asks "find all free projects for X", "what open-source tools do I need for Y", "search for the best project for Z", or wants a department-by-department tool map. Emphasizes LIVE GitHub verification, honest canonical-vs-verified marking, and the rate-limit workaround.
---

# Open-Source Stack Research

The user wants free, self-hostable, open-source projects (MIT/Apache/GPL/BSD preferred) mapped to
functions or company departments. Goal: a customizable, $0-software-cost stack — NOT a SaaS list.

## When to use
- "find all the free projects for an AI company / video gen / telecalling / crawling"
- "what tools does this department need"
- "search for the best web crawler project and give me the link"
- Building/maintaining a company blueprint folder (department → project map)

## Steps
1. **Search GitHub API** for the category. Use `curl -sL "https://api.github.com/..."`:
   - repo: `https://api.github.com/repos/<owner>/<repo>`
   - search: `https://api.github.com/search/repositories?q=<query>&sort=stars&per_page=N`
   - For multi-repo star/license pulls, loop with `urllib.request` in python and **sleep 0.3–1.5s
     between calls** (see pitfall).
2. **Record per project**: name, ★ (live), license (SPDX), link, one-line role. Prefer the
   `license.spdx_id` field. Flag AGPL/NOASSERTION (not OSI) so the user knows obligations.
3. **Mark verification honestly**:
   - `✅` = star count pulled live this session
   - `(canonical)` = well-known repo, NOT re-verified (rate-limited / not checked)
   Never present an unverified star count as fact.
4. **Check the homepage/link resolves** (optional): `curl -s -o /dev/null -w "%{http_code}"`.
5. **Categorize by function**, not just dump. For a company: Executive, Research, Engineering,
   Marketing, Sales/CRM, Finance, Voice, Support, Infra, Security, plus a "compulsory baseline"
   (IAM, secrets, DB, storage, observability, deploy, CRM, ERP, docs, automation, support, analytics).
6. **Flag experimental/concept projects** explicitly (e.g. "Paperclip Maximus = concept only, no
   production repo"; tiny repos = evaluate maintenance before prod). This honesty is expected.
7. **Output shape**: a master index + per-category files; each file = Role / Recommended projects
   (★, license, link) / Why / Integration. Keep it forkable and customizable.

## PITFALL — GitHub API rate limiting (403)
Unauthenticated `api.github.com` calls get `HTTP Error 403: rate limit exceeded` after ~50–60
requests/IP, sometimes immediately on a shared IP. Workarounds that worked:
- Add a `User-Agent` header: `urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})`.
  (Helps but does NOT eliminate the limit.)
- **Space calls out** with `time.sleep(1.2)` between requests in python loops.
- If fully blocked: pause, then retry later; OR verify a smaller critical subset only; OR note
  repos as `(canonical)` and move on. Never invent star counts to fill gaps.
- The `curl` HTML site scrape (duckduckgo etc.) is unreliable for structured data — prefer the API.

## PITFALL — verify the SPECIFIC repo, not just the search
`search/repositories` can return forks or near-names. Before citing a star count, confirm
`repos/<owner>/<repo>` returns the expected `full_name` and `description`. (e.g. "Agent-Reach" is
`Panniantong/Agent-Reach`, 54k★, MIT — not a lowercase variant.)

## PITFALL — "best project" needs a criterion
When asked "best crawler / best X", rank by: live stars, license (AGPL has obligations), maintenance
activity, and fit (AI-native vs legacy scraper). For web intelligence the consensus set is
Agent-Reach (social), Crawl4AI (local), Firecrawl (AI extraction), Browser Use (interactive),
SearXNG (private search). State the tier (must-have / enterprise / specialized).

## Reusable knowledge bank
Condensed verified stacks live in `references/verified-stacks.md` (crawlers, voice, ERP/CRM,
agent frameworks, OpenClaw ecosystem). Update it as you verify new repos so future sessions start
warm.
