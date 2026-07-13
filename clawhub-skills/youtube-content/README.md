[![ClawHub](https://img.shields.io/badge/ClawHub-youtube-content-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: youtube-content
version: 2.0.0
description: Extract transcripts, summaries, and metadata from YouTube videos for content repurposing
tags: ["youtube", "transcript", "content", "video", "cli", "automation", "python", "open-source", "agent", "MIT"]
---

# YouTube Content Toolkit

**Extract transcripts, summaries, and metadata from YouTube videos for content repurposing.**

> *Keywords: youtube, transcript, content, video, cli, automation, python, open-source, agent, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Turning a video into usable text (blogs, clips, summaries) is manual. YouTube Content Toolkit solves this: Extract transcripts, summaries, and metadata from YouTube videos for content repurposing.

**Best for:** Content creators, marketers, and agents repurposing video.

## Features

- **Fetch a transcript**
- **Summarize a video**
- **Pull metadata**
- **Repurpose into posts**
- **Batch a playlist**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/youtube-content/main/youtube_content.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python youtube_content.py --help        # list options
```

## Use cases

1. Fetch a transcript
1. Summarize a video
1. Pull metadata
1. Repurpose into posts
1. Batch a playlist

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Watching full videos | Transcript-first repurposing. |
| Manual notes | Structured metadata + summary. |
| One-off tools | Transcript + summary + metadata together. |

## FAQ (SEO / AEO)

**Q: Transcript?**  
A: Yes — caption/text extraction.

**Q: Summary?**  
A: Generated from the transcript.

**Q: Metadata?**  
A: Title, channel, duration, etc.

**Q: Offline?**  
A: No — fetches from YouTube.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test youtube-content
        run: python youtube_content.py --help
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/youtube-content)
