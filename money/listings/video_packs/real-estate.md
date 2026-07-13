# I will create AI listing videos for real estate agents

**Price:** $200/gig
**Margin:** 99%
**Tags:** real estate video, listing video, property tour, realtor marketing

## What you get
A done-for-you, automated solution built on 100% free/open-source tooling.
No recurring SaaS fees — the system runs on your own infrastructure.

## Delivery process
- 1. Client submits input via order form
- 2. Auto-generate script (if URL) via Hermes
- 3. Render with Automated-Video-Generator (1080p MP4 + vertical cut + voiceover)
- 4. QA pass + captions
- 5. Deliver MP4 + Loom review link

## Why this works
- Self-hosted stack (n8n + free tools) → 90–99% profit margin
- Every deliverable is generated and delivered automatically
- You own the system; scale to unlimited clients

## FAQ
**Q: Do I need to pay for software?**
A: No. Everything runs on free open-source tools (n8n, Chatwoot, Stirling-PDF, Listmonk).

**Q: Is this a one-time build or ongoing?**
A: Both. One-time setup + optional monthly retainer for monitoring/optimization.

**Q: Can you customize for my niche?**
A: Yes — every package is generated from a template and tuned to your vertical.

## Technical spec (for the build)
```json
{
 "job": "video-real-estate",
 "engine": "remotion",
 "tts": "edge-tts",
 "resolution": "1920x1080",
 "vertical_cut": "1080x1920",
 "duration": "45-60s",
 "stock_source": "pexels/pixabay (free tier)",
 "captions": true,
 "repo": "itsPremkumar/Automated-Video-Generator",
 "note": "Feed this manifest to the video generator's render entrypoint."
}
```
