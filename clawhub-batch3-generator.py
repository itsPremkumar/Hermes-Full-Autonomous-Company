#!/usr/bin/env python3
"""Batch 3: Create more ClawHub skill folders."""

import os, json

SKILLS_DIR = r"C:\one\paperclip-company\clawhub-skills"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def create_skill(slug, name, description, tags, body):
    sdir = os.path.join(SKILLS_DIR, slug)
    os.makedirs(sdir, exist_ok=True)
    tags_str = json.dumps(tags)
    skill_md = f"""---
name: {slug}
version: 1.0.0
description: {description}
tags: {tags_str}
---

# {name}

{body}

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
"""
    write_file(os.path.join(sdir, "SKILL.md"), skill_md.lstrip())
    abs_path = os.path.abspath(sdir)
    tags_csv = ",".join(tags)
    print(f"✓ {slug}")
    print(f"  clawhub publish \"{abs_path}\" --slug {slug} --name \"{name}\" --version 1.0.0 --tags \"{tags_csv}\"")
    print()

# All batch 3 skills
create_skill("maps-cli", "Maps & Geocoding CLI",
    "Geocode addresses, search points of interest, get routes and directions, and look up timezones — all from the CLI. Uses free OpenStreetMap/OSRM APIs.",
    ["maps", "geocoding", "routes", "osm", "cli", "python"],
    """## Install
```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/maps-cli/main/maps_cli.py
```

## Usage
```bash
python maps_cli.py geocode "1600 Amphitheatre Parkway, Mountain View"
python maps_cli.py reverse 37.422,-122.084
python maps_cli.py search "coffee shop" --near "New York"
python maps_cli.py route "New York" "Boston" --mode driving
python maps_cli.py timezone 37.422,-122.084
```

## Features
- **Geocoding** — convert addresses to lat/lng coordinates
- **Reverse geocoding** — convert coordinates to addresses
- **POI search** — find places near a location
- **Routing** — get driving, walking, or cycling directions
- **Timezone lookup** — get timezone for any coordinates
- **Zero API keys** — uses free OpenStreetMap Nominatim + OSRM APIs

## Why
Quick location lookups from the terminal. No Google Maps API bills.""")

create_skill("notion-api", "Notion API Toolkit",
    "Read, create, update, and search Notion pages and databases from the CLI. Manage your workspace programmatically.",
    ["notion", "api", "database", "pages", "cli", "python"],
    """## Install
```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/notion-api/main/notion_cli.py
```

## Usage
```bash
# Set your Notion API key
export NOTION_API_KEY=secret_xxxxx

python notion_cli.py search "meeting notes"
python notion_cli.py list-databases
python notion_cli.py query-database <database-id>
python notion_cli.py read-page <page-id>
python notion_cli.py create-page <database-id> --title "New Task" --status "In Progress"
python notion_cli.py update-page <page-id> --property "Status" --value "Done"
```

## Features
- **Search** — search across all pages and databases
- **Database query** — list and query Notion databases
- **Page CRUD** — read, create, and update pages
- **Property management** — update any page property
- **Markdown output** — pages rendered as readable markdown

## Why
Automate your Notion workspace from the terminal. Great for agent workflows.""")

create_skill("airtable-cli", "Airtable API CLI",
    "Read, create, update, delete, and search Airtable records. List bases and tables, filter records, and batch upsert.",
    ["airtable", "database", "api", "cli", "python", "no-code"],
    """## Install
```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/airtable-cli/main/airtable_cli.py
```

## Usage
```bash
# Set your Airtable API key
export AIRTABLE_API_KEY=keyxxxxx

python airtable_cli.py list-bases
python airtable_cli.py list-tables <base-id>
python airtable_cli.py list-records <base-id> <table-name> --limit 10
python airtable_cli.py get-record <base-id> <table-name> <record-id>
python airtable_cli.py create-record <base-id> <table-name> --data '{"Name":"Test","Status":"Active"}'
python airtable_cli.py update-record <base-id> <table-name> <record-id> --data '{"Status":"Done"}'
python airtable_cli.py delete-record <base-id> <table-name> <record-id>
python airtable_cli.py search <base-id> <table-name> <field> <value>
```

## Features
- **Browse bases/tables** — list all accessible bases and their tables
- **Record CRUD** — create, read, update, delete records
- **Search & filter** — find records by field value
- **JSON output** — machine-readable for pipeline integration
- **Rate-limit handling** — automatic retry on Airtable API limits

## Why
Manage your no-code database from the CLI. Automate Airtable workflows.""")

create_skill("polymarket-cli", "Polymarket CLI",
    "Query Polymarket prediction markets: browse markets, check prices, view orderbooks, and track your positions. No API key needed.",
    ["polymarket", "prediction", "markets", "crypto", "cli", "python"],
    """## Install
```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/polymarket-cli/main/polymarket_cli.py
```

## Usage
```bash
python polymarket_cli.py search "election"
python polymarket_cli.py trending
python polymarket_cli.py market <slug-or-id>
python polymarket_cli.py price "will-bitcoin-reach-100k-2025"
python polymarket_cli.py orderbook <token-id>
python polymarket_cli.py categories
```

## Features
- **Market search** — find markets by keyword
- **Trending** — see hot prediction markets
- **Market details** — volume, liquidity, description
- **Price lookup** — current YES/NO prices
- **Orderbook** — bid/ask depth for any market
- **Categories** — browse market categories
- **No API key** — uses public Polymarket API

## Why
Check prediction markets from your terminal. No wallet or API key needed.""")

create_skill("excalidraw-cli", "Excalidraw Diagram Generator",
    "Generate hand-drawn style Excalidraw diagrams (architecture, flow, sequence) as JSON files from the CLI. Edit and merge existing diagrams.",
    ["excalidraw", "diagrams", "drawing", "visualization", "cli", "python"],
    """## Install
```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/excalidraw-cli/main/excalidraw_cli.py
```

## Usage
```bash
# Create various diagram types
python excalidraw_cli.py diagram --type architecture --title "System Design" --output system.excalidraw.json
python excalidraw_cli.py diagram --type flow --title "Auth Flow" --steps "Login,Validate,Redirect"
python excalidraw_cli.py diagram --type sequence --title "API Call" --actors "Client,Server,DB" --steps "Request,Process,Response"

# Manipulate existing diagrams
python excalidraw_cli.py merge base.json overlay.json
python excalidraw_cli.py info diagram.json
python excalidraw_cli.py export diagram.json --format png
```

## Features
- **Architecture diagrams** — cloud/infra system design with labeled boxes
- **Flow charts** — step-by-step process flows with arrows
- **Sequence diagrams** — actor-based interaction diagrams
- **Merge diagrams** — combine multiple Excalidraw files
- **Info/export** — inspect and export to PNG/SVG
- **Hand-drawn style** — Excalidraw's signature sketch aesthetic

## Why
Quick architecture and flow diagrams from the terminal. No drag-and-drop needed.""")

create_skill("ascii-video", "ASCII Video Converter",
    "Convert video files to colored ASCII art MP4 or GIF animations. Frame-by-frame conversion with color support.",
    ["ascii", "video", "animation", "art", "cli", "python", "fun"],
    """## Install
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
Create unique terminal-art videos. Great for demos, READMEs, and social media.""")

print("Batch 3 created!")
