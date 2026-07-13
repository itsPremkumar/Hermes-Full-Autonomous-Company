---
name: gif-search
version: 1.0.0
description: Search and download GIFs from the Tenor API. Supports search, trending, and random GIF lookup with customizable limits.
tags: ["gif", "search", "media", "images", "fun", "cli", "python"]
---

# GIF Search & Download

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/gif-search/main/gif_search.py
```

## Usage

```bash
python gif_search.py search "funny cat" --limit 5
python gif_search.py trending --limit 10
python gif_search.py random "celebration"
python gif_search.py info gif_id_here
```

## Features

- **Search GIFs** — query the Tenor library with natural language
- **Trending** — see what's popular right now
- **Random** — get a random GIF on a topic
- **GIF Info** — get details about a specific GIF (URLs, dimensions, size)
- **Multiple formats** — returns GIF, MP4, and WebM URLs
- **No API key needed** — uses demo key (works for moderate usage)

## Example output

```
$ python gif_search.py search "hello world celebration" --limit 2
1. [18732982] Person celebrating with confetti
   https://tenor.com/gif...gif

2. [16543210] Fireworks spelling Hello World
   https://tenor.com/gif...gif
```

## Commands

| Command | Description |
|---------|-------------|
| `search <query> [--limit N]` | Search for GIFs matching query |
| `trending [--limit N]` | List trending GIFs |
| `random <query>` | Get a random GIF |
| `info <gif-id>` | Get details about a specific GIF |

## Why
Quick GIF lookup for README badges, social media posts, or just fun terminal searches.


## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
