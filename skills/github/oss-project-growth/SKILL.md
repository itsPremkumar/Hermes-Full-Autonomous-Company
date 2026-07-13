---
name: oss-project-growth
description: >-
  Grow an open-source repository's reach — GitHub stars, contributor funnel,
  and launch momentum. Use when the user wants an OSS repo to get more reach,
  go viral, get stars, attract contributors, or ship a launch on Product Hunt,
  Hacker News, Reddit, or X. Covers landing-page trust upgrades (real
  autoplaying demo, clean architecture diagram), opening contributor-friendly
  issues, and a spaced multi-platform launch sequence.
triggers:
  - user wants more reach or more stars for a GitHub repo
  - user wants an OSS project to go viral or become a top open-source project
  - user wants to launch a project on Product Hunt or Hacker News or Reddit
  - user wants to attract contributors or open good first issues
  - user owns an OSS repo and asks for growth or launch assets
---

# OSS Project Growth Playbook

Turn a working OSS repo into one that *converts visitors into stars and
contributors*. The job is mostly landing-page trust + a timed launch, not
new code. Most of this is verifiable with real artifacts (no mockups).

## When to use
- User owns/operates an OSS repo and asks for reach, stars, contributors, or a launch.
- Especially when the project already has a README, tags, and some output artifacts.

## Workflow (do in this order)

1. **Inspect the real repo state first.** Clone/pull locally, read `README.md`,
   and `git remote -v`. Browse the live GitHub page. Note current star count,
   open issues/PRs, tags, and what assets already exist. Do not assume — build on
   what is there (e.g. an existing `LAUNCH_KIT.md`, `GOOD_FIRST_ISSUES.md`).
2. **Find REAL artifacts to use as proof.** Look in `output/`, `samples/`,
   `public/` for generated videos/images. Prefer a short, portrait (1080x1350)
   clip for a Shorts/TikTok-style demo. Never ship a mockup as the demo for a
   *generation* tool — credibility is the whole game.
3. **Upgrade the README landing page** (see Techniques). Commit + push.
4. **Open contributor-friendly issues** (good-first-issues) — signals
   welcoming to GitHub's explore algo and newcomers.
5. **Prepare the launch sequence** (see references/launch-playbook.md) and hand
   it off. Respect auth limits (see Pitfalls) — if you cannot post, leave
   ready-to-paste files + a `GO_LIVE.md` playbook in the repo.
6. **Verify what you shipped is live** (curl the raw asset URLs; check the
   commit appears on GitHub).

## Key techniques

### A. Autoplaying demo GIF (highest-trust landing upgrade)
For a video/visual tool, a moving GIF beats a static diagram. Render from a
real output clip using the project's **bundled `ffmpeg-static`** (so you do not
need ffmpeg on PATH):

```bash
FF="node_modules/ffmpeg-static/ffmpeg.exe"   # or .../ffmpeg on Linux/mac
"$FF" -y -i output/example_short/Example.mp4 -t 8 \
  -vf "fps=12,scale=480:-1:flags=lanczos,palettegen" /tmp/pal.png
"$FF" -y -i output/example_short/Example.mp4 -i /tmp/pal.png -t 8 \
  -lavfi "fps=12,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" assets/demo.gif
```
- Keep it ~8s, 480px wide, palette-optimized (1 to 1.5 MB). Verify with
  `ffmpeg -i assets/demo.gif` (expect `gif, ... 480x600`).
- Embed at top of the README Demo section: `<img src="assets/demo.gif" width="360">`.
- Reusable script: `scripts/render-demo-gif.sh <in.mp4> [out.gif] [dur] [w]`.

### B. Clean architecture SVG (replace ASCII blocks)
ASCII diagrams read as unmaintained to devs skimming. Replace with a branded
SVG (use the project's brand color; keep it simple: runtimes to app core to
lib/services/infra). Commit as `assets/architecture.svg`, embed in README.

### C. Good-first-issues (contributor funnel)
Write 5 to 6 scoped, low-risk issues (docs, tests, CLI help, adapters) each with
a ready title + body. Label `good first issue`. These make the repo surface in
GitHub's contributor-friendly views. `GOOD_FIRST_ISSUES.md` is the canonical
paste source.

### D. Spaced multi-platform launch
See `references/launch-playbook.md` for the exact mechanics: Product Hunt
(Tue to Thu ~12:30pm PT) to Hacker News Show HN (same day, after PH) to Reddit
(r/selfhosted, r/YouTubeAutomation, r/opensource, r/SideProject) to X thread to
dev.to blog. **Spread over 2 to 3 weeks**, and reply to every comment within 24h
for the first two weeks (engagement velocity drives front-page placement).

## Pitfalls
- **No mockups as proof.** A static placeholder GIF/diagram for a generation
  tool reads as fake. Use a real rendered output clip.
- **Broken hero images kill credibility.** Before referencing any
  `assets/*.png/.svg` in the README, confirm the file exists (a search tool may
  misreport; `ls -la assets/` is authoritative).
- **Auth gap.** Without `gh` CLI + auth (or a signed-in browser), you CANNOT
  post issues or launch posts. Detect early (`where gh`, check token). If
  absent, prepare ready-to-paste files + a `GO_LIVE.md` playbook and tell the
  user exactly what to run. Do not claim posted when you only prepared.
- **Path resolution on this Windows + git-bash + Hermes env:** use absolute
  Windows-style paths (`C:/one/...`) for `write_file`/`patch`. MSYS-style paths
  (`/c/one/...`) get mis-resolved by the file tools into `C:\c\...`. Verify the
  resolved path in the tool result and `mv`/fix if needed.
- **Do not burst-post.** All platforms at once = ignored. Space them; each
  platform rewards one high-signal launch post.

## References
- `references/launch-playbook.md` — condensed launch mechanics, platform copy
  pointers, and the auth-gap workaround.
- `scripts/render-demo-gif.sh` — render a palette-optimized demo GIF from a
  real output video using bundled ffmpeg-static.
