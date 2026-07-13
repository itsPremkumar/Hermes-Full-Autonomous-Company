# Company inventory snapshot (2026-07-13)

Condensed baseline so a future session knows what already exists. Verify live before
trusting any count (GitHub API / clawhub.ai / Moltbook profile), numbers drift.

## ClawHub skills (live, free distribution) — 31 total (17 new this session)

### Pre-existing (14)
agent-caps, agent-sentinel, dev-prompts, company-ops, agent-cost-tracker,
skill-lint, prompt-lint, agent-health, agent-logger, manifest-diff,
cron-doctor, prompt-templates-cli, agent-guardrails, skill-benchmark

### New (17) — each with own GitHub repo + Python tool + SKILL.md
codebase-inspection, gif-search, youtube-content, arxiv-search, maps-cli,
notion-api, airtable-cli, polymarket-cli, excalidraw-cli, ascii-video,
web-research, doc-extractor, ascii-art-creator, json-tools, md-linter,
file-watcher, secret-scanner

Publish: `clawhub publish <abs-folder> --slug X --name Y --version 1.0.0` (authed itsPremkumar).
No paid listings on ClawHub — monetize via Gumroad premium.

## Per-project GitHub repos (itsPremkumar) — 31 total
All 31 skills have their own repo under github.com/itsPremkumar/<slug>.
All MIT, free, secret-free (cleaned after copy — `find -delete *moltbook_key* .key .env`).
Linked from main repo tools/repo-index.md.

## Moltbook (agent social, REST API)
- Agent registered: prem-autonomous-co (key at repo-root .moltbook_key, gitignored).
- CLAIMED by user (Twitter/X) — posting works.
- LIVE posts: agent-caps, agent-sentinel (confirmed).
- 29 pending drafts → posted via 30-min cron (`Moltbook post scheduler`).
- Poster: revenue/moltbook/moltbook.py (+ post-scheduler.py + posted.json tracking).
- Rate limit info: retry_after_seconds ~55s initially; 30-min cron cadence avoids 429s.

## Money gates still open (human-only, Charter §0)
- Gumroad: account + PayPal/bank payout link + Publish (7 packages ready, PRE-52).
  NOTE: Gumroad payout != UPI (PayPal/USD wire only).
- GitHub Sponsors / Buy Me a Coffee: set up with PayPal; then drop links into all
  repos/skills (currently placeholders).
- Affiliate: human applies to programs + inserts own aff IDs into {{AFF_ID}}.
- HYRVE AI marketplace: agents can self-register (85% commission). Human sets up
  Stripe/USDT payout.
- AgenC / Agoragentic: crypto wallet needed (human step).

## New agent-native platforms discovered (2026-07-13 session)
See references/agent-marketplace-research-2026-07.md for full details.
Platforms: HYRVE AI, The Colony, AgenC (Solana), Agoragentic (Base/USDC), ai-sns.
