---
name: youtube-content
version: 1.0.0
description: Download YouTube transcripts and generate summaries, threads, and blog posts from video content. Zero external API dependencies.
tags: ["youtube", "transcript", "content", "media", "cli", "python"]
---

# YouTube Transcript Tools

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/youtube-content/main/youtube_tools.py
```

## Usage

```bash
python youtube_tools.py transcript https://youtu.be/dQw4w9WgXcQ
python youtube_tools.py summary https://youtu.be/dQw4w9WgXcQ
python youtube_tools.py info https://youtu.be/dQw4w9WgXcQ
python youtube_tools.py search "python tutorial" --limit 10
```

## Features

- **Transcript download** — fetch video captions (uses Invidious API, no YouTube API key)
- **Smart summary** — extractive summarization of transcript content
- **Video info** — get title, author, view counts
- **Search YouTube** — find videos without API key
- **Zero dependencies** — Python stdlib only

## Why
Process YouTube content from the terminal without API keys.


## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
