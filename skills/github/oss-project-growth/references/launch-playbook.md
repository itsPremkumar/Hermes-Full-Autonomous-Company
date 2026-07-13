# Launch Playbook (condensed)

For a full repo, the canonical copy already lives in the repo's own
`LAUNCH_KIT.md` / `GOOD_FIRST_ISSUES.md` / `GO_LIVE.md`. This file captures the
*reusable mechanics* so any session can rebuild the sequence without re-research.

## Sequence (spread over 2 to 3 weeks — never burst)

| Week | Channel | Notes |
|------|---------|-------|
| 1 | **Product Hunt** | Ship Tue to Thu, ~12:30pm PT. Title = project name. Tagline <= 60 chars, e.g. "Turn any script into a narrated, stock-footage video — free, local, no API key." First comment explains why not SaaS + tech stack + MIT. |
| 1 | **Hacker News "Show HN"** | Post AFTER PH so the PH link is in the HN thread. Body: problem to what it does to no-cloud/no-API-key/MIT to architecture question to invite discussion to repo URL. |
| 2 | **Reddit** (4 subs, separate posts) | r/selfhosted, r/YouTubeAutomation, r/opensource, r/SideProject. Tailor the opener per sub. Lead with local/no-API-key angle for selfhosted, faceless-channel angle for YTAutomation. |
| 2 | **X / Twitter thread** | 4 to 6 tweets: hook (no spy/charge) to why to faceless-channel use case to MIT + star CTA. Pin it. |
| 3 | **dev.to / Hashnode blog** | "How I built a local, no-API-key text-to-video pipeline with Remotion + Edge-TTS." Link repo top + bottom. Outline: SaaS problem to hexagonal arch to script to scene parse to Edge-TTS to stock fetch/licensing to Remotion render to lessons. |
| 3+ | **Post-launch** | Reply to every comment within 24h for 2 weeks. Pin a "What's next?" comment to convert top requests into issues. Thank every new contributor publicly. |

## Why it works (the mechanics)
- **Autoplaying demo GIF** = instant "this works" trust in <5s.
- **Clean SVG architecture** = "maintained" signal to devs.
- **Open good-first-issues** = GitHub tags repo contributor-friendly, surfaces in explore/topic pages.
- **Spaced single high-signal posts** beat a burst; each platform's algo rewards one strong launch post.
- **First-24h replies** = engagement velocity pushes Show HN / PH to the front.

## Auth-gap workaround (when no gh CLI / token / signed-in browser)
1. Write a `GO_LIVE.md` in the repo: Part A = how to open issues (gh CLI cmd + paste URL), Part B = the launch sequence, Part C = post-launch momentum, Part D = the why.
2. Keep `GOOD_FIRST_ISSUES.md` as the paste-ready title+body source.
3. Hand the user the exact commands: install gh CLI, run `gh auth login`, then `gh issue create --title ... --body-file GOOD_FIRST_ISSUES.md --label "good first issue"`.
4. Be explicit: "I prepared these; I could not post them because there is no GitHub auth in this environment."

## Demo-asset recipe (real proof, not mockup)
Render from a real generated clip with bundled ffmpeg-static (see scripts/render-demo-gif.sh).
Prefer a ~8s portrait (1080x1350) short for Shorts/TikTok vibe. Keep <=1.5 MB.
Verify live with: `curl -sI https://raw.githubusercontent.com/<user>/<repo>/<branch>/assets/demo.gif`
(expect HTTP 200, Content-Length > 0).
