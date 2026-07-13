# Repository review checklist

Use this as the structured pass for any "analyze this repo" task. Each item = a concrete command or grep.

## Phase 1 — Remote (no clone)
- [ ] Repo metadata (stars, license, language, size, issues, archived) via API
- [ ] Recursive file tree — note large binaries / duplicated files (same byte size = redundancy)
- [ ] Language breakdown %
- [ ] Commit author distribution (bus factor)
- [ ] README / package.json / AGENTS.md / CHANGELOG.md read by raw URL

## Phase 2 — Local deep review (clone --depth 1)
- [ ] Dependency audit (npm audit --omit=dev / pip-audit) -> severity table
- [ ] Architecture: identify layering pattern + entry points
- [ ] Feature reality-check:
  - [ ] grep `mock`, `Mock`, `placeholder`, `TODO`, `stub`, `not implemented`
  - [ ] does the MAIN entry point import the mocked modules, or are they standalone?
- [ ] Repo health:
  - [ ] test count: `find . -name '*.test.*' -not -path '*/node_modules/*' | wc -l`
  - [ ] CI workflows present under `.github/workflows/`
  - [ ] missing referenced assets (e.g. `default.mp4`, hero images) — grep references, check files exist
- [ ] Hygiene:
  - [ ] duplicate large binaries
  - [ ] committed secrets (`.env`)
  - [ ] git-lfs candidates

## Security posture (if it's a server/web app)
- [ ] Bind address (127.0.0.1 vs 0.0.0.0)
- [ ] Sensitive endpoint gating (local-only middleware)
- [ ] Command exec allowlists vs raw interpolation
- [ ] No secrets committed

## Report structure
1. Snapshot table (lang, license, stars, contributors, size, issues)
2. What it is (verified in code, not README)
3. Tech stack
4. Architecture
5. Strengths
6. Weaknesses / Risks (tie each to a file path or audit line)
7. Recommended next steps (concrete, sized in time)

Separate **verified-in-code facts** from **marketing claims** explicitly.
