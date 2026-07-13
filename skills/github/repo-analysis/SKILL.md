---
name: repo-analysis
description: "Deep end-to-end analysis of any GitHub repository: API metadata, file structure, tech stack, architecture, dependency security audit, mock-vs-real feature detection, and repo-health signals. Use for 'analyze / review / audit this repo' requests."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, code-analysis, security-audit, repo-review, architecture, dependency-audit]
    related_skills: [codebase-inspection, github-code-review]
---

# GitHub Repository Analysis

Turn a "analyze this repo" / "review this project" request into a structured, evidence-backed report. This goes far beyond LOC counts: it combines **GitHub API metadata** (no clone needed) with a **local clone for deep code review** (security audit, architecture, feature reality-check).

## When to Use

- User pastes a GitHub repo URL and asks to "analyze", "review", "audit", or "what is this project"
- Due diligence before forking / contributing / reusing a repo
- Checking whether a project's marketing claims match its code (mock vs real features)
- Repo health / bus-factor / security posture assessment
- **Web/research gathering during the audit** (reading the repo's web context,
  GitHub, social discussion): prefer the **web-research** skill (Agent Reach
  capability layer). It self-heals platform routing and covers social/Chinese
  platforms (Twitter, Reddit, 小红书, Bilibili) that Hermes reaches poorly alone.

## Two-phase approach

### Phase 1 — API metadata (fast, no clone)

Fetch repo overview + full file tree + language breakdown + commit history via the GitHub REST API. See `references/github-api-recipe.md` for the exact `curl` + `python` parsing commands.

Extract: name, description, primary language, stars/forks, created/updated, license, topics, open issues, default branch, archived flag, homepage.

Then read the **key human-readable files** by raw URL (README.md, package.json / pyproject.toml, AGENTS.md, CHANGELOG.md) — these reveal intent, stack, and architecture claims.

### Phase 2 — Deep review (clone required)

`git clone --depth 1 <url>` then inspect the actual code:

1. **Security audit** — `npm audit --omit=dev --json` (Node) / `pip-audit` (Python). Parse the JSON to a severity table. See `references/security-audit-recipe.md`.
2. **Architecture** — identify layering pattern (hexagonal/clean/MVC), entry points, core business logic dirs.
3. **Feature reality-check** — grep for `mock.ts`, `MockProvider`, `placeholder`, `TODO`, `stub`. Confirm whether advertised features (AI video gen, lipsync, etc.) are real or stubbed. **Critical check:** does the *main* app import the mocked modules, or are they standalone experiments? If the main pipeline never imports them, the mocks don't poison the primary path.
4. **Repo health** — bus factor (commit author counts), test count (`find -name '*.test.*'`), CI workflows present, placeholder assets / missing referenced assets (e.g. `default.mp4` referenced but absent).
5. **Bloat / hygiene** — duplicate large binaries (identical byte sizes committed multiple times), committed secrets (`.env`), git-lfs candidates.

## Key checks for web/API projects (security posture)

- **Bind address**: does the server bind `127.0.0.1` (safe) or `0.0.0.0` (exposed)?
- **Endpoint gating**: are sensitive routes behind a local-only / auth middleware (e.g. `requireLocalAccess`, loopback check)? Is there an explicit opt-in override flag?
- **Command execution**: if the app shells out (`exec`/`spawn`), is input **allowlisted** before use? (A whitelist of commands = safe; raw string interpolation = injection risk.)
- **Secrets**: no `.env` committed; `.env.example` only.

## Output format

Lead with a snapshot table (language, license, stars, contributors, size, issues), then structured sections: What it is → Tech stack → Architecture → Strengths → Weaknesses/Risks → Recommended next steps. Use tables and concrete file paths as evidence. Separate **verified-in-code** facts from **marketing claims** explicitly.

## Pitfalls

- **`python3` may be missing** on some hosts (Windows/git-bash) — use `python`. Already captured in memory; don't hard-fail on `python3`.
- **Don't over-rely on README claims** — the README is marketing. Cross-check every "✨ feature" against actual code before reporting it as real.
- **Mock providers are often lab experiments** — a repo full of `mock.ts` files is not necessarily broken; check import graph from the main entry point.
- **Large repos**: use `git clone --depth 1` to avoid pulling full history.
- **npm audit fixes can break builds** — after `npm audit fix`, re-run typecheck/build before declaring success.

See `references/review-checklist.md` for the full inspection checklist and `references/github-api-recipe.md` / `references/security-audit-recipe.md` for copy-paste commands.
