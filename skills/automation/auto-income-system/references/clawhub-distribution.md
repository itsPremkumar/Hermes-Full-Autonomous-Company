# ClawHub Distribution (Stream F)

Agent-native distribution channel. OpenClaw's native skill/plugin registry.
Zero-cost, and on THIS machine the `clawhub` CLI is already authenticated as
`itsPremkumar` — so publishing a skill is fully agent-automatable (no human gate).

## Why it's the best automation fit
- ClawHub has **no paid listings** — everything is FREE. It is a *distribution*
  channel, not a storefront. Money is made OFF it: premium Gumroad version,
  custom builds, consulting.
- Funnel: **free ClawHub skill (distribution) → Gumroad premium (money)**.
- Moltbook ("Reddit for AI agents") = agent-social visibility layer to drive
  ClawHub installs (agents can post autonomously; needs an account).

## Skill package format
A folder containing:
- `SKILL.md` — YAML frontmatter: `name`, `version` (semver), `description`,
  `tags` (comma list). Body = usage + commands + example.
- Supporting files: the tool/script, `examples/`, `test_*.py`.

## Publish (one command, authed)
```bash
clawhub publish "C:/one/paperclip-company/clawhub-skills/agent-caps" \
  --slug agent-caps \
  --name "Agent Capability Manifest Toolkit" \
  --version 1.0.0 \
  --tags "agent,manifest,validation,devtools" \
  --changelog "Initial release"
```
- **MUST pass an absolute path** (relative → "Path must be a folder").
- Auth check: `clawhub whoami` → `✔ itsPremkumar` when logged in.
- Verify live: web page `https://clawhub.ai/skills/skills/<slug>` returns 200
  (vector `clawhub search` is semantic and won't rank a brand-new skill).
- Publish returns an ID like `k9700rbyqf2nqqegq7ch2th81s8af2bb`.

## Compliance
- Skill must be honest (no "guaranteed income"). A free, real tool is ideal.
- Only link the premium Gumroad URL AFTER the user publishes it (human gate).
- Never embed payout creds in the skill.

## Source of truth
Skill source lives in the company repo under `clawhub-skills/<slug>/` and is
pushed to GitHub (as itsPremkumar) alongside the published registry entry.
