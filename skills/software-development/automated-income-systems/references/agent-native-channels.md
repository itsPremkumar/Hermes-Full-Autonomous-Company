# Agent-Native Distribution Channels (ClawHub + Moltbook + Gumroad)

Condensed from a live 2026 build session. Use when the user runs an OpenClaw/Hermes/
Paperclip stack and wants to monetize agent-native tools.

## Why this class beats the static-site streams
The *publish* step is itself agent-automatable. ClawHub publish = one CLI command;
Moltbook post = one REST call. Only the Gumroad payout is human. So ~95% of the
distribution funnel runs with zero human action (once accounts are authed).

## ClawHub (distribution, free)
- OpenClaw's native skill/plugin registry. `clawhub` CLI already installed on the box.
- Publish: `clawhub publish <folder> --slug <s> --name <n> --version 1.0.0 --tags ...`
  - Folder must contain `SKILL.md` (YAML frontmatter: name/version/description/tags) +
    the tool files. Use an ABSOLUTE path (relative path can error "Path must be a folder").
- Everything on ClawHub is FREE. It is a discovery/distribution layer, not a storefront.
- Monetization is OFF-ClawHub: premium Gumroad version, custom builds, consulting.
- Authed as the user: `clawhub whoami` -> `itsPremkumar` means publish needs no login.
- Verify live: `curl -sL -o /dev/null -w "%{http_code}" https://clawhub.ai/skills/skills/<slug>`
  (returns 200 + redirects to /skills/skills/<slug>).

## Moltbook (agent social, announcements)
- Live REST API. Base: `https://www.moltbook.com/api/v1`. Bearer token.
- Register (NO login needed): `POST /agents/register` -> `{agent:{api_key, claim_url,
  verification_code}}`. Save `api_key` to a gitignored `.moltbook_key`.
- Post (NEEDS claimed agent): `POST /posts` with `{title, content, submolt}`.
  - **400 "property link should not exist"** - the text endpoint rejects a top-level
    `link` field. Embed the URL inside `content` instead.
  - **403 "requires a claimed agent"** - until the user verifies at `claim_url`
    (Twitter/X). After claim, posting works.
  - **429** - aggressive rate-limit on bulk posting. Space posts ~45-90s apart; retry
    loop a few times. Do not batch-post many at once.
- Pitfall: the API key is a real secret - gitignore `.moltbook_key`, never copy it into
  product repos or verifiers.
- Stdlib-only poster pattern: `urllib.request` with `Authorization: Bearer <key>` header;
  no pip deps.

## Gumroad (the money layer - human-gated)
- Premium versions of free ClawHub skills + prompt packs. User creates account, links
  payout (PayPal/bank), clicks Publish. Agent prepares `PRODUCT.md` + `LISTING.txt`.

## Funnel
ClawHub (free skill) -> Moltbook (agent announcement) -> Gumroad (premium $). Agent runs
the first two end-to-end; only Gumroad payout is human.

## Payment reality (India / global)
- Gumroad, GitHub Sponsors, Buy Me a Coffee, PayPal -> all pay via **PayPal or bank wire
  (USD)**. **UPI is NOT supported by any.** Never ask the user for a UPI ID; never put
  payout creds in agent context. Indian creator chain: buyer -> platform -> PayPal ->
  withdraw to Indian bank.

## Per-project repo split (when a product is reusable)
1. `curl -X POST -H "Authorization: Bearer <tok>" -d '{"name":<repo>,"license_template":"mit","private":false}' https://api.github.com/user/repos`
2. Stage files into a temp dir; `find . -iname '*moltbook_key*' -delete` (secret guard).
3. `git init` -> commit -> `git pull --rebase <url> HEAD` (remote has auto-LICENSE) -> push.
4. Link every product repo in main repo's `repo-index.md` (URL + status). Keep secret-free.

## Honesty rules (embed in posts/READMEs)
- No "guaranteed income" claims. State the tool is free/free-tier; premium is optional.
- Disclose premium Gumroad link only AFTER Gumroad is published (human step).
- Donation ask (GitHub Sponsors / Buy Me a Coffee) as a supplement, with placeholders the
  user fills.
