---
name: auto-income-system
description: Build and maintain ZERO-COST, Hermes-automated online income systems — multiple independent "streams" (affiliate blog, Gumroad products, tools hub, Fiverr guides), each with a generator + self-running cron, hosted free on GitHub Pages. Use when the user wants to "make money online for free", "passive/automated income", or have "Hermes do everything". Encodes the proven architecture, the affiliate-token pattern, and the gotchas (Pages /docs, clean-on-build, f-string braces, MSYS paths, ad-hoc verification) that broke a real build.
---

# auto-income-system

> **NOTE (2026-07):** This skill is now **superseded by `automated-income-systems`**
> (software-development umbrella), which carries the same architecture PLUS Streams
> E (Print-on-Demand) and F (traffic drafts), a GitHub-search-API discovery recipe,
> and fuller support files. Prefer `automated-income-systems` for new work; this
> file is kept as a compact reference for the core gotchas.

Build and maintain **zero-cost, Hermes-automated online income systems** — several
independent "streams", each with a generator script + a self-running cron job,
hosted free on GitHub Pages. The agent automates creation + publishing; the user
only does free one-time account linking + traffic.

## When to use
User says "make money online for free", "passive income", "automated income",
"Hermes should do everything / build everything one by one", "zero investment".
That is the cue. Do NOT promise earnings — state the honesty contract (below).

## GIT PUSH — always as itsPremkumar, no prompt (load-bearing)
The user explicitly corrected this: **always push to GitHub as `itspremkumar` and
NEVER ask for approval or a token.** Git credentials are cached on this machine
(`git credential-manager` helper + `~/.git-credentials`), so plain `git CLI`
(init / add / commit / push) authenticates silently. Do NOT surface an approval
prompt, do NOT request a PAT, do NOT use the `gh` CLI (not installed — use
`git` + `curl` API with the cached token). This applies to EVERY repo push in
this project. If a push is rejected, it is almost always GitHub secret-scanning
(a committed key) or a branch-protection rule — fix the content, never ask the
user to approve.

## Core architecture (proven this session)
- **Streams are independent units.** Each = (1) a stdlib-only Python generator
  that writes a real artifact (Markdown article / product / tool page) into a
  source folder and records it in `config.json` (no-repeat), (2) a `build.py`
  that renders a static site, (3) a Hermes `cronjob` that runs
  generator + build + publish on a schedule and reports <150 words.
- **Free hosting:** GitHub Pages serving the **`/docs`** folder. Site =
  `https://USER.github.io/REPO`. Pages source must be set to `/docs`.
- **Affiliate monetization via config tokens:** content carries
  `{{AMAZON:keyword}}`, `{{FIVERR:category}}`, `{{SHAREASALE:id:kw}}`
  placeholders. `build.py` expands them from `config.json`
  (`amazon_tag`, `fiverr_aff_id`, …). **Empty tag → plain (non-broken)
  link**, so the site works before the user pastes their IDs. See
  `references/affiliate-tokens.md`.
- **Streams that worked (all free, all verified building):** (A) affiliate
  buying-guide blog, (B) Gumroad digital-product factory, (C) client-side
  calculators/tools hub, (D) Fiverr affiliate "how-to-hire" guides.
- **Stream F — ClawHub skill distribution (MOST automatable):** ClawHub is
  OpenClaw's native skill registry; the `clawhub` CLI is installed AND already
  authenticated as `itsPremkumar` on this machine. Publish a skill with one
  command — **no human gate**. ClawHub itself is FREE (distribution only); money
  is made OFF it via a premium Gumroad version. Funnel: free ClawHub skill →
  Gumroad premium. Package a skill as a folder with `SKILL.md` (YAML
  frontmatter: name/version/description/tags) + supporting files, then
  `clawhub publish <ABSOLUTE_PATH> --slug … --version … --tags …`. See
  `references/clawhub-distribution.md`.

## Human-gate map (Charter §0 — agent does NOT do these)
- **Agent-automatable end-to-end:** build + publish ClawHub skills (authed);
  write affiliate/SEO drafts; commit + push to GitHub as itsPremkumar.
- **Human-only (money/legal):** create Gumroad account, link payout (bank/PayPal),
  click Publish; paste affiliate IDs; any real money receipt. Never store the
  user's payout creds. ClawHub publish needs NO such step.

## Build sequence
1. **Research REAL free programs via direct HTTP checks**, not search HTML:
   `curl -s -o /dev/null -w "%{http_code}" URL`. DuckDuckGo/Bing block
   bot fetches with captchas; hit official pages directly. Verified-live this
   session: Amazon Associates (200), Fiverr Affiliates (200), Spreadshirt
   Partner (200), Gumroad (free). Redbubble/Printful moved/blocked — don't
   fake them; pick a verified one.
2. Write the generator (stdlib only — no pip). Idempotent + no-repeat.
3. Write `build.py` (stdlib Markdown→HTML, sitemap.xml, feed.xml). Copy
   static `src/*.html` into `docs/`.
4. **Wipe `docs/` at the start of every build** (Pitfalls).
5. Create a `cronjob` per stream with a self-contained prompt that runs the
   generator + build + publish and reports <150 words.
6. Verify (below), commit, document the 3 manual free steps in README.

## The honesty contract (do NOT skip)
The agent automates **creation + publishing 100%**. Money still requires the
USER, once, free: (a) paste affiliate IDs into `config.json`, (b) upload
Gumroad products, (c) push to GitHub Pages + drive traffic
(Reddit/Quora/X). No traffic = no income. State plainly: "not passive overnight
income, no earnings guaranteed." Never imply the system prints money alone.

## Pitfalls (hit and fixed this session)
- **GitHub Pages serves `/docs` or branch root — NOT `/public`.** Building into
  `public/` makes URLs `…/public/index.html` and product links 404. Output
  MUST go to `docs/`; Pages source = `/docs`.
- **Static-site generators must CLEAN the output dir on build.** A `build.py`
  that only adds files leaves stale `.html` when a source `.md` is deleted →
  404s/lingering pages. Fix: `rm -rf docs` (or `shutil.rmtree`) BEFORE
  writing. Encode this in `autorun.sh` and in verification.
- **f-string brace doubling.** A generator using `f"""…"` that must EMIT a
  literal `{{TOKEN}}` has to write `{{{{TOKEN}}}}` (f-strings turn
  `{{`→`{`). Writing `{{TOKEN}}` yields a single-brace token that never
  expands. Always grep generated `.md` for single-brace leakage.
- **MSYS path doubling in write_file/patch.** On this Windows/MSYS host,
  passing `/c/Users/PREM KUMAR/...` resolves to `C:\c\Users\...` (doubled).
  Always use Windows absolute paths `C:\Users\PREM KUMAR\...` with
  write_file/patch, then verify with `ls`/`search_files` on the real path.
- **Ad-hoc verification discipline (enforced by the session harness):** write a
  temp script in `%TEMP%` named `hermes-verify-*.py`, run it on a COPY of
  the repo (exclude `.git` + built `docs/`), replicate bash steps DIRECTLY in
  Python (do NOT `subprocess.run(["bash", ...])` — bash isn't on PATH in the
  WSL relay sandbox and fails), wipe `docs/` between builds, then
  `shutil.rmtree` the temp dir. Report as ad-hoc, not suite-green.
- **Stale `hermes-verify-*` temp files cause the harness "unverified" loop.**
  The session harness flags the workspace "unverified" when it sees changed
  paths. Leftover `hermes-verify-*.py` AND `hermes-verify-*/` DIRS in `%TEMP%`
  get counted as changed paths → a false, self-perpetuating "unverified" flag
  every turn. FIX: after each ad-hoc verify, `rm -rf` ALL
  `%TEMP%/hermes-verify-*` (both `.py` files and leaked dirs). Re-run the verify
  only after confirming none remain. This is why inline `python - <<'PY'…PY`
  verification (no temp file at all) is often cleaner here.
- **`clawhub publish` needs an ABSOLUTE path.** Passing a relative path or CWD
  fails with `Error: Path must be a folder`. Always pass a Windows-absolute
  path e.g. `clawhub publish "C:/one/paperclip-company/clawhub-skills/agent-caps"
  --slug …`. The `clawhub whoami` check returns `✔ itsPremkumar` when authed.


## Verification (ad-hoc, repeatable)
See `references/verify-recipe.md` for the temp-copy + wipe + link-resolution
pattern, `references/affiliate-tokens.md` for the token regex + empty-tag
fallback, and `references/clawhub-distribution.md` for the ClawHub publish
recipe (absolute-path requirement, auth check, live verification). After any
code edit, re-run a focused verify script before claiming done — the session
harness demanded this and caught real bugs (corrupted build.py, stale
artifacts, unexpanded tokens, and the stale-`hermes-verify-*` false-flag loop).
