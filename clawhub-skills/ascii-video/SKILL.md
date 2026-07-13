---
name: ascii-video
version: 1.0.0
description: Convert video files to colored ASCII art MP4 or GIF animations. Frame-by-frame conversion with color support.
tags: ["ascii", "video", "animation", "art", "cli", "python", "fun"]
---

# ASCII Video Converter

## Install
```bash
# Requires Python 3.8+. Install: pip install Pillow
# For video input: ffmpeg required
curl -O https://raw.githubusercontent.com/itsPremkumar/ascii-video/main/ascii_video.py
```

## Usage
```bash
# Convert video to ASCII animation
python ascii_video.py convert input.mp4 --output output.gif --width 80 --fps 10
python ascii_video.py convert input.mp4 --output output.mp4 --width 120 --color

# Preview a single frame
python ascii_video.py frame input.mp4 --at 00:01:30 --width 100

# Convert image to ASCII
python ascii_video.py image input.jpg --width 80 --color
```

## Features
- **Video to ASCII** — convert any video to ASCII animation
- **Color support** — full ANSI color in terminal output
- **GIF/MP4 output** — export as animated GIF or MP4
- **Frame preview** — grab a single frame at any timestamp
- **Image to ASCII** — convert still images too
- **Customizable** — width, height, FPS, character set

## Commands
| Command | Description |
|---------|-------------|
| `convert <input> --output <file>` | Convert video to ASCII animation |
| `frame <input> --at <timestamp>` | Preview a single frame |
| `image <input>` | Convert image to ASCII |

## Why
Create unique terminal-art videos. Great for demos, READMEs, and social media.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
