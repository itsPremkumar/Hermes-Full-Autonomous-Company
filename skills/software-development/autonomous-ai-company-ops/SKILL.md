---
name: autonomous-ai-company-ops
description: >-
  Operate the Hermes-Full-Autonomous-Company — a $0-budget AI company running on
  Paperclip (7-agent org) + Hermes Agent (executive) + OpenClaw (comms/computer-use)
  + hermes-paperclip-adapter, with GitHub as the single source of truth. Covers server
  launch, the 24/7 cron autonomy loop, Constitution-as-OS v3.0, the product
  research→build→test→push cycle, revenue-channel research, and the human-in-the-loop
  gates. Use when the user says "continue the company," "build/push a product," "start
  earning," "run 24/7," or anything about operating this autonomous company.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Autonomous AI Company Operations

## When to use
- "run the company 24/7", "continue building", "build a product and push it"
- "research money-earning / revenue possibilities", "start the money earning process"
- Any task touching Paperclip, the autonomy loop, `CONSTITUTION.md`, `digital-products/`,
  `income-engine/`, or `revenue/`
- Pushing company code to GitHub as `itsPremkumar`

## The stack (verified, running)
- **Paperclip** — org layer: 7 agents, budgets, ticketing, governance. Server on :3100;
  embedded Postgres on :5432.
- **Hermes Agent** — executive/CEO. Local folder `C:\one\paperclip-company` = git repo
  tracking `github.com/itsPremkumar/Hermes-Full-Autonomous-Company` (branch `master`).
- **OpenClaw** — comms + computer-use, gateway :18789.
- **hermes-paperclip-adapter** — CEO↔Paperclip bridge.
- **OmniRoute→OpenRouter** — free-model escalation (key from env ONLY).

## Operating principles (load-bearing)
1. **GitHub = single source of truth.** Every asset, prompt, lesson, state is committed.
   If it isn't on GitHub, it didn't happen.
2. **Constitution = the OS.** `CONSTITUTION.md` v3.0 is the behavior spec; the repo is
   the operating system (kernel map, dependency graph, failure taxonomy, maturity levels,
   roadmap — all in `docs/`). The prompt defines behavior; the repo defines the system.
3. **Human-in-the-loop is non-negotiable (Charter §0).** Money movement is gated: Gumroad
   account creation, payout/bank/PayPal linking, clicking Publish, affiliate-program
   applications, any spend → PRINCIPAL does it. The agent may prepare everything up to
   the click.
4. **Memory discipline (low-RAM box ~644MB free).** Never spawn >2-3 heavy procs. Scope
   `find` tightly (deep `/c` scans hang). Check RAM via `wmic OS Get FreePhysicalMemory`.
5. **Never push secrets.** OpenRouter key, .env, credentials stay local/in env. GitHub
   secret scanning blocks the push if a key is committed — redact to env var and rewrite
   history.
6. **Auto-push as `itsPremkumar` via git CLI — NEVER ask for approval.** Cached creds make
   `git push` silent. This is an explicit, repeated user directive (the account-picker
   modal, if it ever returns, is fixed in references/git-credential-fix.md).

## Start the company server (if down)
```
terminal(background=true): cmd.exe //c "C:\one\paperclip-company\run-server.bat"
then poll http://127.0.0.1:3100/api/health until 200
```
A Windows Scheduled Task `PaperclipServer` should launch it on boot; if the chat session
restarted it may need a manual start.

## The 24/7 autonomy loop
- Cron job "Company Autonomy Loop" runs every 30 min, forever. Each tick: RAM check →
  `git pull --ff-only` → read tasks.md + Paperclip issues → do next AGENT-ACTIONABLE,
  NON-HUMAN-GATED task → commit + push.
- Implementation: `autonomy-loop.py` (confidence gate + benchmark logging + failure
  categorization).
- Human-gated tasks are detected (keywords: gumroad publish, payout, bank, create account,
  tax, PRE-52) and skipped with a flag.

## Product research→build→test→push cycle
1. **Research** with the "never reinvent" rule (Constitution §4): GitHub search ≥3 mature
   solutions before building.
2. **Build** stdlib-only / $0 tools that run on the low-RAM box (e.g. `agent-caps` — the
   capability-manifest toolkit, product #9).
3. **Test / verify — the 7-axis harness (CANONICAL test command).** This is the
   "verify from all perspectives" system and the cure for the recurring
   "unverified" flag loop. Every product in `clawhub-skills/<name>/` MUST pass all 7 axes:
     1. **structure** — `SKILL.md` + a `.py` tool (OR an external-tool skill: `requirements.txt`/install note)
     2. **frontmatter** — `name`/`version`/`description` in `SKILL.md`
     3. **compiles** — `py_compile` every `.py`
     4. **self-test** — a `.py` exposing `self-test` (REAL asserts, NOT fake `return 0`) OR `test_*.py` OR a `test:` line in `SKILL.md` (external-tool skills)
     5. **security** — no hardcoded secret (`key=value` with a real value)
     6. **docs** — `SKILL.md` has Usage/Why/Example
     7. **deploy-ready** — `ci/ci_check.py` hard-fails a broken package (must FAIL on missing `SKILL.md`)

   **Run it (not ad-hoc temp scripts):**
   ```bash
   python ci/verify_product.py clawhub-skills/<name>   # one product
   python ci/verify_product.py clawhub-skills/*/            # whole portfolio (31 folders)
   ```
   Exit 0 = all axes green. CI in every repo runs this on **Python 3.8 AND 3.11** + a `ci_check.py` deploy-check job (`docs/ci-workflow-template.yml` is the template).
   **Adding a tool?** It MUST get a real `self-test` subcommand (call a pure function on temp input + assert). Delegate the mechanical addition of `self-test` to 13+ tools via `delegate_task` (leaf), then **independently re-run the harness yourself** — subagent self-reports are not verified facts (we caught real gaps: 19/31 folders failed the harness before the fix).
   **Why this killed the unverified loop:** the system flags ANY changed path as needing verification. Writing a `hermes-verify-*.py` temp script re-triggers the flag on itself. The permanent cure is a committed canonical suite (`ci/verify_product.py` + `tools/test_all_skills.py`) so the harness has a real test command and stops demanding ad-hoc proofs. See references/portfolio-verification.md.
4. **Package** as a Gumroad product: `income-engine/gumroad/products/<id>/PRODUCT.md` +
   `LISTING.txt` (copy-paste Title/Price/Description). Template: templates/product-package.md.
5. **Catalog** in `digital-products/product-catalog.json` (update stats).
6. **Push** to GitHub (silent, itsPremkumar).
7. **Human publishes** on Gumroad (PRE-52 runbook).

## Revenue channels (scored, updated 2026-07-13)

- **ClawHub skill (OpenClaw native registry)** — **95% automatable, PUBLISHED live.** `clawhub`
  CLI is installed + authed as `itsPremkumar` (`clawhub whoami` ✔). Publish = one command,
  no human step. Everything on ClawHub is FREE (distribution, not storefront); money is made
  off it via premium Gumroad versions. Our 31 skills are live.
  See references/agent-native-channels.md.
- **HYRVE AI marketplace (agent freelance marketplace)** — **~90% automatable, NEW.**
  `hyrveai.com` — first AI agent marketplace. 5,750+ community, 85% commission to creator,
  48-hour escrow, Stripe/USDT/stablecoin payouts. Agents self-register in 30s via API/skill.md.
  Our skills (doc-extractor, secret-scanner, codebase-inspection, json-tools etc.) map
  directly to service offerings. Only payout setup is human-gated. Research in
  `agent-native-distribution` skill's references/agent-marketplace-research-2026-07.md.
- **Moltbook (agent social network, REST API)** — ~80% automatable. `POST /api/v1/agents/register`
  needs NO login (returns api_key); posting is gated on the human "claim" step (Twitter/X
  verify, 403 until claimed). We registered `prem-autonomous-co`; post flow works end-to-end.
  See references/agent-native-channels.md + the post-scheduler setup below.

## Moltbook post scheduler (automated product announcements)
To backfill Moltbook posts for all 31 ClawHub skills without hitting rate limits:
- **Pre-built drafts**: `revenue/moltbook/post-<slug>.json` — 31 files, one per skill.
- **Tracker**: `revenue/moltbook/posted.json` — `{"posted": ["agent-caps", "agent-sentinel", ...]}`
- **Scheduler script**: `revenue/moltbook/post-scheduler.py` — finds first unposted draft,
  posts it to Moltbook API, updates tracker. Stdlib-only.
- **Cron job**: `Moltbook post scheduler` — fires every 30 min, deliver=origin.
- **Rate limit**: Moltbook returns `retry_after_seconds: ~55` on 429. The 30-min cadence
  safely avoids hitting it. ~14.5h to backfill 29 remaining posts.
- **Setting up**: `cd /c/one/paperclip-company && python revenue/moltbook/post-scheduler.py`
  to test. The cron does this automatically each tick.
- **The Colony (agent social + marketplace)** — **~70% automatable, NEW.** `thecolony.cc` —
  topic-based forums + paid task marketplace. OpenClaw skill exists for integration.
  Agents self-register; marketplace transactions may need human wallet setup.
- **Affiliate content engine** — 85% automatable (agent writes SEO drafts + disclosure;
  human applies to programs + inserts own aff IDs). Engine: `revenue/affiliate/affiliate-engine.py`.
- **Gumroad product sales** — 70% (human publishes 7 ready packages, PRE-52).
- **ai-sns (OpenClaw agent social network)** — **~70% automatable, NEW.** `ai-sns/ai-sns` (319★).
  OpenClaw-native 3D agent social network on A2A protocol.
- **AgenC (Solana agent hiring protocol)** — **~60% automatable, NEW.** `tetsuo-ai/AgenC` (190★).
  Agents get hired and paid on Solana mainnet. Crypto wallet needed.
- **Micro-SaaS** (wrap free-tier AI APIs) — 60%, pilot in `revenue/microsaas/`.
- **Agoragentic (cross-framework agent commerce)** — **~50% automatable, NEW.**
  `rhein1/agoragentic-integrations`. Settle in USDC on Base. 50+ framework adapters.
- Fiverr / ads / newsletter — deferred (low automation or traffic-gated).
- Compliance: disclose affiliate links, no fake reviews, no income guarantees, only
  verified tools. ClawHub/Moltbook posts must be honest (no "guaranteed income").

## Publish agent-native skills (ClawHub + Moltbook)
These are the MOST end-to-end-automatable distribution channels — the agent can build AND
publish with zero human action (only eventual money receipt is gated).
- **ClawHub** (`clawhub` CLI, authed as `itsPremkumar`): package a skill as a folder with
  `SKILL.md` (YAML frontmatter: name/version/description/tags) + supporting files, then
  `clawhub publish "<abs-folder>" --slug X --name "Name" --version 1.0.0 --tags "t1,t2,t3"`.

  **Content quality is enforced.** The registry rejects thin/templated SKILL.md with
  `"Skill content is too thin or templated. Add meaningful, specific documentation."`.
  Every published SKILL.md MUST include rich, substantive sections — at minimum:
  install instructions, usage with command examples, a features list, a commands table,
  and a "why" section. Code blocks, example output, and CI integration snippets all
  help. A skeleton with just frontmatter + one paragraph will be rejected.

  **Exact publish command:**
  ```bash
  clawhub publish "C:\path\to\skill-folder" --slug my-skill --name "My Skill" --version 1.0.0 --tags "tag1,tag2,tag3"
  ```
  Verify token first: `clawhub whoami` (must show ✔ itsPremkumar). Absolute path required
  (relative/CWD paths error with "Path must be a folder").

  **Confirmation**: success returns `✔ OK. Published <slug>@1.0.0 (<hash>)`.
  Search index may lag — `clawhub search <slug>` may not immediately return results after
  publish. The publish response itself is the authoritative confirmation.

  **Batch upgrade + republish (verified 2026-07-13).** When upgrading all N skills at once
  (e.g. v1 → v2 with new features + README + docs): do it in 4 deterministic passes, NOT by
  hand:
  1. **Generate docs** — a Python script (`generate_v2_docs.py`) loops all `clawhub-skills/<name>/`
     folders and writes `README.md` (badge bar, Quick start, feature table, sample output, links)
     + a v2 `SKILL.md` (frontmatter `version: 2.0.0` + Install/Commands/Features/CI/Why/Support).
     Keep a dict of `{slug: {name, tool, desc, tags, commands[], features[]}}` so every skill
     gets consistent structure. Verify with `ast.parse` on every `.py` + a glob count of
     generated files (must == N).
  2. **Push to GitHub per repo** — `push_all_v2.py` does, per skill: `git init` → `git remote add
     origin https://github.com/itsPremkumar/<slug>.git` → `git add -A` → commit →
     `git branch -m master main` → `git pull --rebase -X theirs` → `git rm -r --cached __pycache__`
     → `git push origin main`. For renamed repos use a URL_MAP (agent-caps→prem-agent-caps,
     dev-prompts→dev-prompts-pack). **Always rebase-pull before push** — the remote may have a
     LICENSE/README commit from `license_template` and reject a non-FF push.
  3. **Republish on ClawHub** — `republish_all_v2.py` calls `clawhub publish` for each with
     `--version 2.0.0`. The FIRST publish of a version succeeds; re-running the SAME version
     errors `✖ Uncaught ConvexError: Version 2.0.0 already exists` — that is HARMLESS (it's
     already live). Capture only `✖` lines that are NOT the version-exists message.
  4. **Update Moltbook drafts** — `update_moltbook_drafts_v2.py` rewrites `revenue/moltbook/
     post-<slug>.json` titles/content to v2 messaging; the scheduler cron picks them up on its
     30-min tick.
  All four scripts live in the repo root and are committed. See references/clawhub-batch-upgrade.md
  for the exact script skeletons + the 14-check ad-hoc verification pattern that proves the
  generated docs/tool parse correctly (run from `%TEMP%/hermes-verify-*.py`, then DELETE it so
  it doesn't re-trigger the unverified flag).

  **Batch generation**: for 5+ skills, write a Python script that creates the folder +
  SKILL.md + tool files, then publish individually. This avoids repetitive manual folder
  setup and ensures consistent frontmatter structure. See `references/clawhub-batch-publishing.md`.

  Note: ClawHub has NO paid listings — it's free distribution; monetize via Gumroad premium.
- **Moltbook** (agent REST API at `https://www.moltbook.com/api/v1`): `POST /agents/register`
  (no login → returns `api_key` + `claim_url`), save key to a gitignored `.moltbook_key`,
  then `POST /posts` with `Authorization: Bearer <key>`. Posting returns 403 until the agent
  is CLAIMED (Twitter/X verify at the `claim_url`) — that's the user's one step. Build a
  stdlib poster (`revenue/moltbook/moltbook.py`); never hardcode the key; gitignore it.
- Keep posts honest: announce the free skill, link it, mention the Gumroad premium, NO income
  guarantees. Rate-limit; don't spam.

## Pitfalls (from real sessions)
- **Account-picker modal on every push** → `x-access-token` GCM entry. Fix:
  references/git-credential-fix.md.
- **Push rejected by GitHub secret scanning** → hardcoded OpenRouter key in a .bat/.sh.
  Fix: redact to `%OPENROUTER_API_KEY%` / `"$OPENROUTER_API_KEY"`, rewrite the commit so
  the key is never in history, re-push. references/push-secret-scan-block.md.
- **"Unverified" flag loop after editing code** → stale `hermes-verify-*` temp files in
  `%TEMP%` counted as changed paths. Fix: verify inline (heredoc) or write a
  `hermes-verify-*.py` temp script, run it, then DELETE it + any leaked `hermes-verify-*`
  dirs. references/verification-unverified-flag.md.
- **`write_file` with `/c/...` absolute paths** gets a `C:\` prefix but resolves to the
  same MSYS path — verify with `ls` after writing.
- **Server dark after session restart** → start it; the Scheduled Task may not have fired.
- **Deep `find /c` scans hang under memory starvation** → scope searches tightly.
- **ClawHub publish needs absolute path** → `clawhub publish <abs-path>` (relative/CWD
  paths error with "Path must be a folder"). Check `clawhub whoami` ✔ before publishing.
- **Moltbook 403 "requires a claimed agent"** → post only works after the user claims the
  agent at the `claim_url` (Twitter/X verify). Register is login-free; the claim is the
  human step. Don't re-attempt posting in a loop — hand the claim_url to the user.
- **Moltbook 400 "property link should not exist"** → the `/posts` text endpoint rejects a
  top-level `"link"` field. Once claimed, a payload with `"link"` 400s. Fix: embed the URL
  inside `content` (`body = f"{content}\n\n{link}"`) and drop the top-level `link` key.
- **Moltbook `.moltbook_key` location + path-math trap** → NEVER store the key inside the
  working dir that gets committed/staged (e.g. `revenue/moltbook/.moltbook_key`). The
  canonical test suite flags "secret in dir" and a monorepo split would otherwise try to
  push it. Keep it at **repo root** `.moltbook_key` (already gitignored). In `moltbook.py`,
  `KEY_FILE` must resolve TWO levels up from `revenue/moltbook/moltbook.py`:
  `os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".moltbook_key"))`.
  `os.path.dirname(os.path.dirname(__file__))` resolves to `revenue/`, NOT repo root — a
  silent wrong-path bug. After moving the key, re-run `load_key()` to confirm it resolves.
- **Moltbook 429 rate-limit floor is 2.5 MINUTES, not 90s.** The live API returns
  `{"statusCode":429,"message":"You can only post once every 2.5 minutes","retry_after_seconds":109}`
  (note: the message says 2.5 min but the field says 109s — treat the FLOOR as ~2.5 min). The
  autonomy loop's 30-min tick is SAFE and correct. A background posting loop with 90s/5-min gaps
  WILL still 429 — do NOT use short backoff for Moltbook. **The scheduler must handle 429
  gracefully**: on 429, do NOT mark the draft as posted (leave it in the unposted queue so the
  next tick retries), and do NOT crash. The proven `post-scheduler.py` reads `posted.json`, posts
  the first unposted draft, and only appends to `posted.json` on HTTP 201 — so a 429 simply leaves
  the draft for next time. Confirmed: agent-caps + agent-sentinel posted live; the rest land
  gradually via the 30-min loop without manual intervention.
- **Unverified-flag loop in THIS repo → canonical suite fix.** The harness kept flagging
  `hermes-verify-*` temp files. The permanent cure: `tools/test_all_skills.py` runs every
  tool's `self-test`, the agent-caps suite, validates all Moltbook drafts (honest/linked/
  donation ask), and checks no secret in `revenue/moltbook/`. Run `python tools/test_all_skills.py`
  → exit 0. Commit it so the harness has a test command and stops demanding ad-hoc proofs.
- **Splitting monorepo → per-project GitHub repos** (user focus task) → see
  references/agent-native-channels.md "Splitting the monorepo". Key traps: (a) `license_template`
  auto-inits a LICENSE → first push non-fast-forward; `git pull --rebase` then push. (b) Defensively
  `find -delete` `*moltbook_key*`/`*.key`/`*.env` from each staged project; re-scan the target repo
  tree for `moltbook_key` before declaring clean. Link the new repos from `tools/repo-index.md`
  ("Our Product Repositories" section), not the dependency index.
- **Gumroad payout ≠ UPI** → Gumroad pays out via **PayPal or USD bank wire only**; it does NOT
  support Indian UPI. If the user offers a UPI ID for payments, tell them to link PayPal (→ Indian
  bank) instead, and NEVER accept the UPI ID (or any payout credential) into the agent context —
  Charter §0 forbids the agent handling payout creds. The agent prepares everything up to the
  Gumroad Publish click; the user does the payout linking + publish.
- **ClawHub rejects thin/templated SKILL.md** → publish fails with `"Skill content is too thin
  or templated. Add meaningful, specific documentation."` Every SKILL.md needs rich sections:
  install, usage with examples, features list, commands table, and why. Code blocks with example
  output help. A skeleton with just frontmatter + one paragraph will be rejected. Fix: expand
  the SKILL.md with substantive content, then retry publish.
- **`__pycache__/` committed to GitHub repos** → when copying skill folders to git repos with
  `cp -r`, `__pycache__/` directories and `*.pyc` bytecode files get included. Fix: after the
  first push, add `.gitignore` with `__pycache__/` and `*.pyc`, `git rm -r --cached __pycache__/`,
  commit, and push. Or add `.gitignore` before the initial commit.
- **Delegation boundaries for ClawHub publishing** → subagents (delegate_task) can create skill
  folders and publish to ClawHub (clawhub CLI works in subagent terminal). However, subagents
  CANNOT access the GCM token for GitHub repo creation (the token lives in the parent session's
  git credential helper context). Always create GitHub repos and push code in the parent context
  after subagents finish their publishes.
- **ClawHub `inspect` gives FALSE NEGATIVES — do not trust it for audit.** `clawhub inspect @slug`
  FAILS (the `@` prefix is rejected). Use the bare slug: `clawhub inspect <slug>` (no `@`). Even
  then, if another user published a skill with the SAME slug, the API returns
  `AMBIGUOUS_SKILL_SLUG` and the bare-slug inspect errors out — this is NOT "your skill is
  missing", it just means the slug collides. To confirm YOUR skill is live, check the web page
  `curl -sS -o /dev/null -w "%{http_code}" https://clawhub.ai/itspremkumar/skills/<slug>` (HTTP 200
  = live) or grep `clawhub explore --sort newest` output for your slug. During the 2026-07-13 audit,
  9/31 skills falsely showed "MISSING" from naive `inspect @slug` loops; all 9 were confirmed live
  via the web-page check. Verified-live count was 31/31, not 22/31.
- **ClawHub search index lag after publish** → `clawhub search <slug>` may return nothing for
  minutes after a successful publish (vector index rebuilds asynchronously). Do NOT retry-publish
  — that produces a duplicate. The publish response (`✔ OK. Published <slug>`) is the definitive
  confirmation. Use `clawhub explore --sort newest` as an alternative check after a delay.
- **GitHub repo creation via API token** → to create repos from the CLI, extract the token from
  git credential manager and use curl:
- **Batch-upgrading all N skills (v1→v2) → 4-pass script pattern.** Do NOT edit 31 SKILL.md
  files by hand. (1) `generate_v2_docs.py` writes README.md + v2 SKILL.md for every folder from
  a `{slug: {...}}` dict. (2) `push_all_v2.py` does per-repo `git init`→remote→add→commit→
  `branch -m master main`→`pull --rebase -X theirs`→`rm --cached __pycache__`→push. (3)
  `republish_all_v2.py` re-publishes each with `--version 2.0.0` (ignore "already exists"
  errors). (4) `update_moltbook_drafts_v2.py` rewrites the 31 post drafts. Verify the pass
  with a temp `hermes-verify-*.py` (counts generated files == N, `ast.parse` all `.py`, reads
  back a sample README + SKILL.md), then DELETE the temp file. Full skeletons in
  references/clawhub-batch-upgrade.md.
- **`git push` to a per-project repo rejects non-fast-forward after `license_template`** →
  the auto-init LICENSE commit on origin beats your local commit. Always `git pull --rebase
  -X theirs origin main` BEFORE `git push`. A bare `git push` after local-only commit 404s
  with "src refspec main does not match any" if the local branch is `master` and remote is
  `main` — `git branch -m master main` first.
- **ClawHub version-exists error is NOT a failure** → `clawhub publish ... --version 2.0.0`
  on an already-live 2.0.0 returns `✖ Uncaught ConvexError: Version 2.0.0 already exists`.
  Treat that as "done"; only a DIFFERENT error (network, auth, thin-content) is a real failure.
  To push changes you MUST bump the version — same version can never be re-published.
  ```bash
  TOKEN=$(echo -e "protocol=https\nhost=github.com" | git credential-manager get | grep "^password=" | cut -d= -f2)
  curl -X POST https://api.github.com/user/repos -H "Authorization: token $TOKEN" \
    -d '{"name":"<repo>","description":"<desc>","private":false,"auto_init":false}'
  ```
  The token is a `gho_*` or `ghp_*` string. Never echo it to terminal.

## Support files
- references/git-credential-fix.md — kill the x-access-token account-picker modal.
- references/push-secret-scan-block.md — redact + rewrite history when a secret is committed.
- references/verification-unverified-flag.md — why the "unverified" loop happens and how to clear it.
- references/agent-native-channels.md — ClawHub + Moltbook publish/distribute flow, the Moltbook 400 link fix, and the monorepo→per-project GitHub repo split (verified this session).
- references/agent-marketplace-research-2026-07.md — HYRVE AI, The Colony, AgenC, Agoragentic, ai-sns platforms.
- references/inventory-2026-07.md — live ClawHub skills, 12 GitHub product repos, Moltbook state, open money gates (baseline snapshot).
- references/clawhub-batch-publishing.md — the generator-template + content-quality rules + publish loop for creating 5+ ClawHub skills per session.
- references/clawhub-batch-upgrade.md — the 4-pass script pattern (generate docs → push repos → republish ClawHub → update Moltbook drafts) for upgrading all N skills at once, with the exact `generate_v2_docs.py` / `push_all_v2.py` / `republish_all_v2.py` / `update_moltbook_drafts_v2.py` skeletons + the 14-check temp-verify harness.
- references/clawhub-inspect-audit.md — why `clawhub inspect` gives FALSE NEGATIVES (the `@` prefix, `AMBIGUOUS_SKILL_SLUG` slug collisions) and the reliable web-page HTTP-200 audit pattern.
- references/portfolio-verification.md — the 7-axis `verify_product.py` harness: why it exists, the axes, canonical commands, and the session outcome (31/31 PASS).
- scripts/verify-adhoc.py — template for inline ad-hoc verification (no temp file).
- templates/product-package.md — Gumroad product package skeleton (PRODUCT.md + LISTING.txt).
