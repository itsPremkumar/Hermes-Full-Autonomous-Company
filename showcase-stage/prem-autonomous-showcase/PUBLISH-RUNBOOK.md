# Founder Publish Runbook — Showcase Repo (PRE-5)

This bundle is build-complete and review-ready. **Publication is a founder (Prem) decision** (house rule: no auto-publish of public-facing properties). The agent staged everything; you push the button.

## What's in this bundle (`showcase-stage/prem-autonomous-showcase/`)
- `README.md` — GitHub repo front page (offerings, proof table, pricing pointer).
- `index.html` — GitHub Pages site (self-contained, dark theme).
- `linkedin-launch.md` — Company Page "About" + 2 launch-post drafts.
- `.github/workflows/pages.yml` — auto-deploys `index.html` to GitHub Pages on push to `main`.

## Go-live (founder, ~10 min)

> ⚠️ **Do NOT run `git init` inside this folder as-is.** This bundle lives inside the
> `paperclip-company` monorepo (whose `origin` is `itsPremkumar/Hermes-Full-Autonomous-Company`).
> Running `git init` here would reinitialize that parent repo and `git remote add origin`
> would fail (origin already exists). Instead, publish from a clean external copy.

1. **Create the repo** `itsPremkumar/prem-autonomous-showcase` on GitHub (public).
2. **Copy the bundle to a clean folder outside the monorepo, then publish:**
   ```
   # from C:/one (NOT inside paperclip-company)
   xcopy /E /I paperclip-company\showcase-stage\prem-autonomous-showcase C:\one\prem-autonomous-showcase
   cd C:\one\prem-autonomous-showcase
   git init -b main
   git add -A
   git commit -m "Showcase: autonomous agent offerings (PRE-5)"
   git remote add origin https://github.com/itsPremkumar/prem-autonomous-showcase.git
   git push -u origin main
   ```
   (On macOS/Linux use `cp -r` instead of `xcopy`.)
3. **Enable Pages:** repo Settings → Pages → Source: "GitHub Actions". The workflow deploys `index.html` automatically.
4. **LinkedIn:** copy `linkedin-launch.md` content into the Company Page "About" and publish one launch post.
5. **Confirm pricing link:** `README.md`/`index.html` reference the pricing tiers (PRE-6). PRE-6 is `in_review` — confirm the approved floor ($129–$499/mo + $990 custom) before quoting exact numbers publicly, or link to the staged pricing doc.

## Status gates (do NOT auto-cross)
- Public GitHub Pages site: **founder publish approval required** (PRE-5 is `in_review`).
- LinkedIn page: **founder publish approval required**.
- Pricing numbers: **founder approval required** (PRE-6 §4).

## Verify after publish
- Pages URL returns 200 and renders `index.html`.
- LinkedIn post visible on the Company Page.
- Report the public URLs back on PRE-5 so the agent can flip it to `done` and link it from PRE-8 outreach + PRE-7 video descriptions.
