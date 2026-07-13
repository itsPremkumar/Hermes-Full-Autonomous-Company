---
name: maps-cli
version: 1.0.0
description: Geocode addresses, search points of interest, get routes and directions, and look up timezones — all from the CLI. Uses free OpenStreetMap/OSRM APIs.
tags: ["maps", "geocoding", "routes", "osm", "cli", "python"]
---

# Maps & Geocoding CLI

## Install
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
Quick location lookups from the terminal. No Google Maps API bills.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
