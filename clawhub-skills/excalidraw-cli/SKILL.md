---
name: excalidraw-cli
version: 1.0.0
description: Generate hand-drawn style Excalidraw diagrams (architecture, flow, sequence) as JSON files from the CLI. Edit and merge existing diagrams.
tags: ["excalidraw", "diagrams", "drawing", "visualization", "cli", "python"]
---

# Excalidraw Diagram Generator

## Install
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
Quick architecture and flow diagrams from the terminal. No drag-and-drop needed.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

test: python excalidraw_cli.py --help   # install first: curl -O https://raw.githubusercontent.com/itsPremkumar/excalidraw-cli/main/excalidraw_cli.py
