---
name: automated-content-site
description: Build, automate, and verify zero-cost affiliate/content web properties driven by Hermes Agent. Use when a user wants to "make money online free", run a hands-off content/affiliate site, or have Hermes autonomously research+write+publish on a schedule. Covers the full stack — stdlib-only static generator, affiliate-token templating, free GitHub Pages hosting, and a self-running weekly article cron.
---

# Automated Content / Affiliate Site (zero-cost, Hermes-driven)

Build a money-making web property that runs itself for **$0** and **0 paid tools**:
a static site generated from Markdown, affiliate links injected via config tokens,
hosted free on GitHub Pages, and fed new articles by a Hermes cron job that
researches real products and writes them.

## When to use
- "make money online free / zero investment / automation"
- "set up passive income with Hermes"
- any request to autonomously research, write, and publish content on a schedule

## Architecture (the proven shape)
```
project/
├─ build.py          # stdlib-only: Markdown -> static site (index, articles, sitemap.xml, feed.xml, disclosure)
├─ config.json       # site_name, site_url, niches[], amazon_tag, shareasale_id  (affiliate IDs left EMPTY by agent)
├─ content/          # <slug>.md articles (agent adds 1/week via cron)
├─ autorun.sh        # rebuild + `git push` to GitHub Pages (crash-proof: push failure is non-fatal)
├─ README.md         # the 3 manual steps the USER must do
└─ public/           # built output
```
**Why stdlib-only:** no pip, no venv, runs on the bare Python the agent already has.
Avoid third-party deps for the build step so it never breaks across machines.

## Build steps
1. `build.py` — parse frontmatter (`title/description/slug/date/niche`), render a
   minimal Markdown->HTML converter, expand `{{AMAZON:Keyword}}` / `{{SHAREASALE:id:kw}}`
   affiliate tokens from `config.json`, emit index + per-article + sitemap + RSS + disclosure.
2. `config.json` — list `niches` (low-competition buying-guide topics). Keep affiliate
   ID fields EMPTY in the shipped config; the user fills them once.
3. `content/<slug>.md` — start with 1 real, fully-written article (proves the engine).
4. `autorun.sh` — `git pull --rebase`, `python build.py`, commit, `git push` (make push
   failure non-fatal so local builds still succeed without remote creds).
5. Git init on `main`, commit. (Remote + Pages enabled by the user later.)
6. Cron job: weekly, self-contained prompt that picks an uncovered niche, web-searches
   3–5 REAL products, writes 1200–1800 words with affiliate tokens, runs `autorun.sh`.

## The 3 things ONLY the user can do (document in README — never skip)
1. Create free GitHub repo `money-engine`, `git remote add` + push, enable Pages.
2. Sign up FREE for Amazon Associates + ShareASale, paste IDs into `config.json`.
   (The agent cannot open accounts in the user's name — this is the money spigot.)
3. Drive free traffic (Reddit/X/Pinterest/Quora) — no traffic = no earnings.

## CRITICAL pitfalls
- **MSYS path doubling (Windows):** when writing files with the `write_file` tool on a
  Windows host using bash, an MSYS path like `/c/Users/PREM KUMAR/...` is silently
  rewritten to `C:\c\Users\PREM KUMAR\...` (the `C:` gets prepended, doubling the root).
  Always pass **native Windows absolute paths** (`C:\Users\...`) to `write_file` on
  Windows; only use `/c/...` inside `terminal`/`bash` commands. See references/windows-msys-path-pitfall.md.
- **Frontmatter quote bug:** YAML-ish frontmatter values written with quotes
  (`slug: "foo"`) must have quotes STRIPPED during parse, or the rendered filename
  becomes `"foo".html` and the build throws `OSError [Errno 22] Invalid argument`.
- **Affiliate tokens:** use `{{AMAZON:Keyword}}` placeholders in content, never bake in
  a real tag. Empty `amazon_tag` must still render a valid clickable `amazon.com/s?k=`
  link (no stray `&tag=`). Expansion is verified in references/verification.md.
- **Honest framing:** tell the user upfront this is NOT overnight passive income — it
  compounds per published article, and the agent cannot guarantee earnings. Don't
  oversell; the deliverable is working free software, not deposited cash.

## Verification (always, before claiming done)
Write an ad-hoc script to `%LOCALAPPDATA%\Temp\hermes-verify-<name>.py`, run it
against a **temp copy** of the project, assert behavior, then delete it. See
references/verification.md for the checklist that catches the bugs above.

## Support files
- references/windows-msys-path-pitfall.md — the write_file doubling bug + fix
- references/verification.md — ad-hoc verify checklist (17/18 → real result)
- templates/build.py — known-good stdlib static generator (copy + modify)
- templates/config.json — config shape with empty affiliate fields
- templates/autorun.sh — crash-proof deploy script
- templates/sample-article.md — frontmatter + body format the cron must follow
