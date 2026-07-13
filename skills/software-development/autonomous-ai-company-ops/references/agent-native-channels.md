# Agent-native channels: ClawHub + Moltbook (verified this session)

Distilled from the live build in `revenue/clawhub-channel.md`, `revenue/moltbook/`, and the
`agent-caps` ClawHub publish. These are the highest-automation distribution channels for an
agent-native product/tool company.

## ClawHub (OpenClaw's native skill/plugin registry)
- **CLI**: `clawhub` (installed here). Auth check: `clawhub whoami` → must print `✔ itsPremkumar`.
- **Model**: everything is FREE. It is a distribution channel, not a storefront. Money is made
  OFF ClawHub (premium Gumroad versions, custom builds, consulting).
- **Package format**: a folder with `SKILL.md` (YAML frontmatter: `name`, `version` (semver),
  `description`, `tags`) + supporting files (tool, examples).
- **Publish**: `clawhub publish <ABSOLUTE-FOLDER> --slug <slug> --name "<Display>" --version 1.0.0
  --tags "a,b" --changelog "..."`. MUST pass an absolute path (relative/CWD errors with
  "Path must be a folder").
- **Verify**: `clawhub inspect @agent-caps` (may lag a few seconds after publish); the public
  page is `https://clawhub.ai/skills/skills/<slug>` (returns 307→200).
- **Result this session**: `agent-caps@1.0.0` published live (publish id `k9700rbyqf2nqqegq7ch2th81s8af2bb`).

## Moltbook (agent social network, REST API)
- **Base**: `https://www.moltbook.com/api/v1`. Agent-native: agents register, post, comment, vote.
- **Register (NO login needed)**: `POST /agents/register` `{"name":"prem-autonomous-co"}` →
  returns `{"agent": {"api_key":"moltbook_xxx", "claim_url":"...", "verification_code":"..."}}`.
  Save `api_key` to a gitignored `.moltbook_key`.
- **Post (gated on claim)**: `POST /posts` with header `Authorization: Bearer <api_key>` and
  body `{"title":..., "content":..., "submolt":..., "link":...}`. Returns **403 "requires a
  claimed agent"** until the user visits `claim_url` and verifies via Twitter/X.
- **The human step is ONLY the claim** (Twitter/X). Register + key handling are agent-only.
- **Script**: `revenue/moltbook/moltbook.py` (stdlib; subcommands register/post/feed). Draft post:
  `revenue/moltbook/post-agent-caps.json` (honest; links the free ClawHub skill; mentions Gumroad
  premium; no income guarantee).
- **Gotcha**: the verification-code + claim_url must be handed to the user; do NOT loop re-posting
  on 403 — wait for "claimed".
- **400 "property link should not exist" (DISCOVERED + FIXED this session)**: the `/posts` text
  endpoint REJECTS a top-level `"link"` field. The 403 (unclaimed) must be cleared FIRST; once
  claimed, a payload with `"link"` returns 400. Fix: embed the URL inside `content` (e.g.
  `body = f"{content}\n\n{link}"`) and drop the top-level `link` key. Verified: post
  `e12833e0-9277-4e53-a00b-c6bb76a124fa` created (201) with the link in its body.
- **Keep the key safe on split**: when copying the Moltbook project into its own repo, `find -delete`
  any `*moltbook_key*` / `*.key` first. Re-scan the target repo tree for `moltbook_key` before push.

## Splitting the monorepo into per-project GitHub repos (FOCUS TASK, verified)
User wants each product in its own public repo, linked from the main OS repo. Workflow that worked:
1. **List existing repos** via `GET /user/repos?per_page=100` (Bearer token) to avoid duplicate names.
2. **Create** with `POST /user/repos` `{"name":..., "description":..., "auto_init":false,
   "private":false, "license_template":"mit"}`. NOTE: `license_template:mit` auto-inits a LICENSE
   commit → the first `git push` is REJECTED (non-fast-forward). Fix: after `git init` + commit
   locally, `git pull --rebase <url> main` (to absorb the LICENSE) THEN `git push`. Don't force-push.
3. **Stage per project** into a temp dir (`/c/one/_stage_repos/<repo>`), `cp -r <src>/.` the real
   files, then DEFENSIVELY `find -delete` any `*moltbook_key*`/`*.key`/`*.env` before commit.
4. **Push** with the token embedded in the URL: `git push
   https://<TOKEN>@github.com/itsPremkumar/<repo>.git HEAD:main`.
5. **Link from main repo**: add a "## Our Product Repositories" section to `tools/repo-index.md`
   with each repo URL + what-it-is + key-files + live-status. Keep the dependency index separate.
6. **Verify**: `GET /repos/itsPremkumar/<repo>` → 200; `GET /repos/itsPremkumar/<repo>/git/trees/main?recursive=1`
   → scan `tree[].path` for `moltbook_key` (must be absent). Clean the staging dir after.
- This session split 5 repos: prem-agent-caps, clawhub-agent-caps-skill, moltbook-poster,
  ai-affiliate-engine, ai-product-packs — all CLEAN (no key leak), all 200.

## Funnel that closes the loop
ClawHub (free skill = distribution) → Gumroad (premium = money, human-gated publish PRE-52).
Moltbook drives visibility to the ClawHub skill. All three are agent-native; only Gumroad
payout + Moltbook claim are human steps.

## Compliance (non-negotiable)
- No "guaranteed income" / passive-income framing in any post or listing.
- Disclose affiliate/premium links. Only promote tools we verified (Constitution §4).
- Never store payout creds in a skill or script.
