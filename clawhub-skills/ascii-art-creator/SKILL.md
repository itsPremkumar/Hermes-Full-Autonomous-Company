---
name: ASCII Art Creator
version: 1.0.0
description: Generate ASCII art banners (figlet-style), unicode boxes, cow messages, data tables, and image-to-ASCII conversions. Zero dependencies beyond Python stdlib.
tags: ascii,art,text,fun,cli,python,cowsay,figlet,banner
---

# ASCII Art Creator

A zero-dependency Python CLI that brings classic ASCII art to your terminal — figlet-style banners, unicode-boxed messages, talking cows, structured data tables, and even image-to-ASCII conversion. All implemented with Python's standard library only.

Perfect for terminal splash screens, README badges, CLI tool output formatting, fun commit messages, and adding personality to your command line.

## Install

```bash
# No pip install needed — Python 3.8+ stdlib only
cp ascii_art.py /usr/local/bin/ascii-art
chmod +x /usr/local/bin/ascii-art

# Or run directly
python ascii_art.py --help
```

## Commands

| Command | Description |
|---------|-------------|
| `banner <text>` | Generate a figlet-style ASCII banner (big letters) |
| `banner <text> --font block` | Choose a banner font: `standard`, `block`, `slant` |
| `box <text>` | Wrap text in a unicode box with rounded/corners |
| `box <text> --style double` | Box styles: `single`, `double`, `round`, `thick` |
| `cow <msg>` | Display a message with a classic cowsay cow |
| `cow <msg> --face dead` | Cow faces: `default`, `stoned`, `dead`, `happy`, `bored` |
| `table [data...]` | Render pipe-separated data as a clean ASCII table |
| `table --header "Name,Age,City" --rows "Alice,30,NYC" "Bob,25,LA"` | |
| `image <image-file>` | Convert an image to ASCII art (grayscale + character map) |
| `image <image-file> --width 80` | Set output width in characters (default: 80) |

## Usage

```bash
# Create a banner
python ascii_art.py banner "Hello World"

# Try different banner fonts
python ascii_art.py banner "WELCOME" --font block
python ascii_art.py banner "CLI" --font slant

# Box a message
python ascii_art.py box "System ready — all checks passed"

# Fancy box styles
python ascii_art.py box "Notice" --style double
python ascii_art.py box "Hello!" --style round

# Talking cow
python ascii_art.py cow "Hello from the terminal!"

# Cow with different moods
python ascii_art.py cow "Feed me data" --face happy
python ascii_art.py cow "I'm tired" --face dead

# Render a table
python ascii_art.py table --header "Name,Role,Status" --rows "Alice,Admin,Active" "Bob,User,Away" "Carol,Editor,Online"

# Image to ASCII
python ascii_art.py image photo.jpg --width 60
```

## Features

- **Zero dependencies** — everything uses the Python standard library only
- **Multiple banner fonts** — `standard` (figlet-style), `block` (thick blocks), `slant` (italic-style)
- **Unicode box drawing** — single, double, round, and thick border styles using box-drawing characters
- **Cowsay implementation** — classic talking cow with 5 facial expressions
- **ASCII tables** — render structured data with column headers and alignment
- **Image-to-ASCII** — converts images to grayscale ASCII art (uses Python's built-in image support via raw pixel access or PIL-like fallback)
- **Pipe-compatible** — all commands can be chained in shell pipelines
- **Color-safe** — prints plain text, compatible with any terminal

## Examples

```bash
# Terminal welcome screen
clear && python ascii_art.py banner "MyApp" --font block && python ascii_art.py box "Version 2.0 — Ready"

# Fun git commit prompt
python ascii_art.py cow "Time to commit?" --face happy

# Data report in a table
python ascii_art.py table --header "File,Size,Status" --rows "main.py,12KB,✓" "utils.py,8KB,✓" "test.py,3KB,✗"

# Art for a README
python ascii_art.py banner "API" --font slant | sed 's/^/    /'
python ascii_art.py box "Fast • Reliable • Scalable" --style round

# Birthday greeting
python ascii_art.py banner "HAPPY" --font block
python ascii_art.py banner "BIRTHDAY" --font block
python ascii_art.py cow "Have a great day!" --face happy
```

## Why ASCII Art Creator?

ASCII art tools are usually scattered across multiple packages — `figlet` (a C binary), `cowsay` (a Perl script), `jp2a` (image-to-ASCII with C dependencies). Each requires a separate install and often a different package manager. This tool consolidates five ASCII art generators into a single Python file that runs anywhere Python does.

Perfect for:
- **CI/CD pipelines** — add personality to build output without installing extra packages
- **Terminal applications** — format output with boxes, tables, and banners
- **README badges & headers** — generate ASCII art for documentation
- **Fun scripts & games** — add retro charm to any CLI tool
- **Minimal environments** — Docker containers, embedded systems, locked-down servers

## Font Samples

```
Standard:    Block:      Slant:
 ██╗██╗       ██ ██       /██╗ /██╗
 ██║██║     ████████      \██║ \██║
 ██║██║       ██ ██        ██║ ██║
 ██║██║     ████████       ██║ ██║
 ██║██║       ██ ██        ██║ ██║
```

## Support

- File an issue on the [ClawHub registry](https://clawhub.nousresearch.com)
- MIT License — free to use, modify, and share
- Contributions welcome — add more fonts, cow styles, and table features
