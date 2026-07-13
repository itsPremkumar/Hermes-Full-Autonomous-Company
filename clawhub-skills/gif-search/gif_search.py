#!/usr/bin/env python3
"""gif_search.py — Search and download GIFs from Tenor API.

Usage:
  python gif_search.py search <query> [--limit 5]
  python gif_search.py trending [--limit 10]
  python gif_search.py random <query>
  python gif_search.py info <gif-id>

Requires: requests or curl. Optional: set TENOR_API_KEY env var.
"""
import sys, os, json, urllib.request, urllib.parse, urllib.error, html

TENOR_API_KEY = os.environ.get("TENOR_API_KEY", "AIzaSyCx-GlApCF5ULgMLUaFs_78RAQk1JMNhLk")  # demo key
BASE_URL = "https://tenor.googleapis.com/v2"
USER_AGENT = "GIFSearch/1.0"

def _get(endpoint, params):
    params["key"] = TENOR_API_KEY
    url = f"{BASE_URL}/{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def cmd_search(query, limit=5):
    data = _get("search", {"q": query, "limit": limit, "media_filter": "minimal"})
    results = data.get("results", [])
    for i, r in enumerate(results, 1):
        desc = r.get("content_description", "No description")
        gif_id = r.get("id", "?")
        url = ""
        for fmt in ("gif", "mp4", "webm"):
            media = r.get("media_formats", {}).get(fmt, {})
            if media.get("url"):
                url = media["url"]
                break
        print(f"{i}. [{gif_id}] {desc}")
        if url:
            print(f"   {url}")
        print()

def cmd_trending(limit=10):
    data = _get("featured", {"limit": limit, "media_filter": "minimal"})
    for i, r in enumerate(data.get("results", []), 1):
        desc = r.get("content_description", "No description")
        print(f"{i}. {desc} (id: {r.get('id','?')})")

def cmd_random(query):
    data = _get("search", {"q": query, "limit": 1, "media_filter": "minimal"})
    results = data.get("results", [])
    if results:
        r = results[0]
        print(f"Random GIF: {r.get('content_description', '?')}")
        for fmt in ("gif", "mp4", "webm"):
            media = r.get("media_formats", {}).get(fmt, {})
            if media.get("url"):
                print(f"  [{fmt}]: {media['url']}")
    else:
        print("No results found")

def cmd_info(gif_id):
    data = _get("posts", {"ids": gif_id, "media_filter": "minimal"})
    results = data.get("results", [])
    if results:
        r = results[0]
        print(f"ID: {r.get('id')}")
        print(f"Description: {r.get('content_description', 'N/A')}")
        print(f"Created: {r.get('created', 'N/A')}")
        for fmt in ("gif", "mp4", "webm"):
            media = r.get("media_formats", {}).get(fmt, {})
            if media.get("url"):
                dims = f"{media.get('dims',['?','?'])[0]}x{media.get('dims',['?','?'])[1]}"
                print(f"  [{fmt}]: {media['url']} ({dims}, {media.get('size',0)//1024}KB)")
    else:
        print("GIF not found")

def main():
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "search" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        limit = 5
        if "--limit" in sys.argv:
            limit = int(sys.argv[sys.argv.index("--limit")+1])
        cmd_search(query, limit)
    elif cmd == "trending":
        limit = 10
        if "--limit" in sys.argv:
            limit = int(sys.argv[sys.argv.index("--limit")+1])
        cmd_trending(limit)
    elif cmd == "random" and len(sys.argv) >= 3:
        cmd_random(" ".join(sys.argv[2:]))
    elif cmd == "info" and len(sys.argv) >= 3:
        cmd_info(sys.argv[2])
    else:
        print(f"Unknown command or missing args", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
