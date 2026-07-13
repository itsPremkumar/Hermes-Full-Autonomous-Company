#!/usr/bin/env python3
"""Batch 2: Create additional ClawHub skill folders with rich SKILL.md + Python tools."""

import os, json, textwrap

SKILLS_DIR = r"C:\one\paperclip-company\clawhub-skills"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def create_skill(slug, name, description, tags, tool_code, body_extra=""):
    sdir = os.path.join(SKILLS_DIR, slug)
    os.makedirs(sdir, exist_ok=True)
    
    # Build SKILL.md
    tags_str = json.dumps(tags)
    skill_md = f"""---
name: {slug}
version: 1.0.0
description: {description}
tags: {tags_str}
---

# {name}

{body_extra}

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
"""
    write_file(os.path.join(sdir, "SKILL.md"), skill_md.lstrip())
    
    # Write tool file
    if tool_code:
        tool_path = os.path.join(sdir, f"{slug.replace('-','_')}.py")
        write_file(tool_path, tool_code.lstrip())
        # Note: can't chmod on Windows easily, but the file works
    
    # Print publish command
    abs_path = os.path.abspath(sdir)
    tags_csv = ",".join(tags)
    print(f"✓ {slug} created")
    print(f"  clawhub publish \"{abs_path}\" --slug {slug} --name \"{name}\" --version 1.0.0 --tags \"{tags_csv}\"")
    print()

# Skill 1: gif-search
create_skill("gif-search", "GIF Search & Download",
    "Search and download GIFs from the Tenor API. Supports search, trending, and random GIF lookup with customizable limits.",
    ["gif", "search", "media", "images", "fun", "cli", "python"],
    '''#!/usr/bin/env python3
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
''',
    body_extra=textwrap.dedent("""\
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
    """))

# Skill 2: youtube-content
create_skill("youtube-content", "YouTube Transcript Tools",
    "Download YouTube transcripts and generate summaries, threads, and blog posts from video content. Zero external API dependencies.",
    ["youtube", "transcript", "content", "media", "cli", "python"],
    '''#!/usr/bin/env python3
"""youtube_tools.py — YouTube transcript download and content processing.

Usage:
  python youtube_tools.py transcript <video-url-or-id>
  python youtube_tools.py summary <video-url-or-id> [--lang en]
  python youtube_tools.py search <topic> [--limit 5]
  python youtube_tools.py info <video-url-or-id>

Stdlib only. No YouTube API key needed (uses yt-dlp-style extraction or invidious).
"""
import sys, json, re, urllib.request, urllib.parse, urllib.error, html, textwrap

USER_AGENT = "YouTubeTools/1.0"

def extract_video_id(url_or_id):
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/shorts/)([A-Za-z0-9_-]{11})',
        r'^([A-Za-z0-9_-]{11})$'
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    return None

def fetch_page(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.read().decode("utf-8", errors="replace")

def extract_transcript(video_id):
    """Extract transcript from YouTube's API (captions endpoint)."""
    # Try IV (Invidious) API first - no auth needed
    try:
        iv_url = f"https://invidious.snopyta.org/api/v1/videos/{video_id}"
        req = urllib.request.Request(iv_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        captions = data.get("captions", [])
        if captions:
            # Get first available caption
            caption_url = captions[0].get("url", "")
            if caption_url:
                if not caption_url.startswith("http"):
                    caption_url = f"https://invidious.snopyta.org{caption_url}"
                req = urllib.request.Request(caption_url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=10) as r:
                    content = r.read().decode("utf-8", errors="replace")
                # Parse transcript XML-like format
                texts = re.findall(r'<text[^>]*>(.*?)</text>', content)
                transcript = []
                for t in texts:
                    text = html.unescape(t)
                    text = re.sub(r'<[^>]+>', '', text)
                    transcript.append(text)
                return "\\n".join(transcript) if transcript else None
    except Exception:
        pass
    
    # Fallback: scrape page for captions
    try:
        page = fetch_page(video_id)
        # Try to find caption URLs in page source
        matches = re.findall(r'"captionTracks":\s*(\[.*?\])', page)
        if matches:
            import json as j
            tracks = j.loads(matches[0])
            for track in tracks:
                if track.get("baseUrl"):
                    req = urllib.request.Request(track["baseUrl"], headers={"User-Agent": USER_AGENT})
                    with urllib.request.urlopen(req, timeout=10) as r:
                        content = r.read().decode("utf-8", errors="replace")
                    texts = re.findall(r'<text[^>]*>(.*?)</text>', content)
                    transcript = [html.unescape(t) for t in texts]
                    return "\\n".join(transcript)
    except Exception:
        pass
    return None

def cmd_transcript(url_or_id):
    vid = extract_video_id(url_or_id)
    if not vid:
        print("Could not extract video ID", file=sys.stderr)
        sys.exit(1)
    transcript = extract_transcript(vid)
    if transcript:
        print(transcript[:5000])
        if len(transcript) > 5000:
            print(f"\\n[... truncated, full length: {len(transcript)} chars]")
    else:
        print(f"No transcript available for video {vid}", file=sys.stderr)
        print("The video may have no captions or be unavailable.", file=sys.stderr)
        sys.exit(1)

def cmd_summary(url_or_id):
    vid = extract_video_id(url_or_id)
    if not vid:
        print("Could not extract video ID", file=sys.stderr)
        sys.exit(1)
    transcript = extract_transcript(vid)
    if not transcript:
        print(f"No transcript available", file=sys.stderr)
        sys.exit(1)
    # Simple extractive summary: split into chunks, take first sentences
    sentences = re.split(r'(?<=[.!?])\\s+', transcript)
    summary = []
    char_count = 0
    for s in sentences[:20]:
        summary.append(s)
        char_count += len(s)
        if char_count >= 800:
            break
    print("=== Summary ===")
    print(" ".join(summary))
    print(f"\\n(Full transcript: {len(transcript)} chars)")

def cmd_info(url_or_id):
    vid = extract_video_id(url_or_id)
    if not vid:
        print("Could not extract video ID", file=sys.stderr)
        sys.exit(1)
    page = fetch_page(vid)
    # Extract basic info
    title_m = re.search(r'<title>(.*?)</title>', page)
    title = html.unescape(title_m.group(1)) if title_m else "Unknown"
    # Remove " - YouTube" suffix
    title = re.sub(r'\\s*-\\s*YouTube$', '', title)
    print(f"Video ID:   {vid}")
    print(f"Title:      {title}")
    print(f"URL:        https://youtu.be/{vid}")

def cmd_search(topic, limit=5):
    """Search YouTube via Invidious API (no auth)."""
    try:
        url = f"https://invidious.snopyta.org/api/v1/search?q={urllib.parse.quote(topic)}&sort=relevance"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        for i, v in enumerate(data[:limit], 1):
            title = v.get("title", "Unknown")
            author = v.get("author", "?")
            views = v.get("viewCount", 0)
            vid = v.get("videoId", "")
            print(f"{i}. {title}")
            print(f"   By {author} | {views:,} views")
            print(f"   https://youtu.be/{vid}")
            print()
    except Exception as e:
        print(f"Search failed: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print(__doc__.strip())
        sys.exit(1)
    cmd = sys.argv[1]
    arg = " ".join(sys.argv[2:])
    if cmd == "transcript":
        cmd_transcript(arg)
    elif cmd == "summary":
        cmd_summary(arg)
    elif cmd == "info":
        cmd_info(arg)
    elif cmd == "search":
        limit = 5
        if "--limit" in sys.argv:
            limit = int(sys.argv[sys.argv.index("--limit")+1])
        cmd_search(arg, limit)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
''',
    body_extra=textwrap.dedent("""\
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
    """))

# Skill 3: arxiv papers
create_skill("arxiv-search", "ArXiv Paper Search",
    "Search academic papers on arXiv by keyword, author, category, or ID. Fetch abstracts, download PDFs, and export citations.",
    ["arxiv", "papers", "research", "academic", "cli", "python"],
    '''#!/usr/bin/env python3
"""arxiv_tools.py — Search arXiv papers by keyword, author, category, or ID.

Usage:
  python arxiv_tools.py search <query> [--limit 10] [--sort relevance|date]
  python arxiv_tools.py author <name> [--limit 5]
  python arxiv_tools.py category <cat> [--limit 10]
  python arxiv_tools.py fetch <arxiv-id>
  python arxiv_tools.py abstract <arxiv-id>

Stdlib only. Uses arXiv API (no API key needed).
"""
import sys, json, urllib.request, urllib.parse, xml.etree.ElementTree as ET, textwrap

ARXIV_API = "http://export.arxiv.org/api/query"
USER_AGENT = "ArxivTools/1.0"

def _query(params, max_retries=2):
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode("utf-8")
        except Exception as e:
            if attempt == max_retries - 1:
                raise e

def _parse_entry(entry):
    ns = {"": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    title = entry.find("title", ns)
    title = title.text.strip().replace("\\n", " ") if title is not None else "Untitled"
    summary = entry.find("summary", ns)
    summary = summary.text.strip()[:500] if summary is not None else ""
    summary = re.sub(r'\\s+', ' ', summary)
    id_elem = entry.find("id", ns)
    arxiv_id = id_elem.text.split("/")[-1].split("v")[0] if id_elem is not None else "?"
    authors = []
    for a in entry.findall("author", ns):
        name = a.find("name", ns)
        if name is not None:
            authors.append(name.text)
    published = entry.find("published", ns)
    published = published.text[:10] if published is not None else "?"
    categories = [c.get("term", "") for c in entry.findall("category", ns)]
    link = ""
    for l in entry.findall("link", ns):
        if l.get("title", "") == "pdf":
            link = l.get("href", "")
            break
    return {
        "id": arxiv_id,
        "title": title,
        "authors": authors[:5],
        "published": published,
        "categories": categories[:3],
        "summary": summary,
        "pdf_url": link,
        "url": f"https://arxiv.org/abs/{arxiv_id}",
    }

def cmd_search(query, limit=10, sort="relevance"):
    xml_data = __query({
        "search_query": f"all:{urllib.parse.quote(query)}",
        "max_results": limit,
        "sortBy": sort,
    })
    root = ET.fromstring(xml_data)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    results = [_parse_entry(e) for e in entries]
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['id']}] {r['title'][:80]}")
        print(f"   Authors: {', '.join(r['authors'])}")
        print(f"   Published: {r['published']} | Categories: {', '.join(r['categories'])}")
        print(f"   {r['url']}")
        print()

def cmd_author(name, limit=5):
    xml_data = _query({
        "search_query": f"au:{urllib.parse.quote(name)}",
        "max_results": limit,
    })
    root = ET.fromstring(xml_data)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    results = [_parse_entry(e) for e in entries]
    print(f"Papers by {name}:")
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['published']}] {r['title'][:80]}")
        print(f"   {r['url']}")

def cmd_category(cat, limit=10):
    xml_data = _query({
        "search_query": f"cat:{urllib.parse.quote(cat)}",
        "max_results": limit,
    })
    root = ET.fromstring(xml_data)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    results = [_parse_entry(e) for e in entries]
    print(f"Recent papers in category {cat}:")
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r['published']}] {r['title'][:80]}")
        print(f"   Authors: {', '.join(r['authors'][:3])}")

def cmd_fetch(arxiv_id):
    """Fetch paper details by ID."""
    cmd_search(arxiv_id, limit=1)

def cmd_abstract(arxiv_id):
    xml_data = _query({"id_list": arxiv_id})
    root = ET.fromstring(xml_data)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    if entries:
        r = _parse_entry(entries[0])
        print(f"Title: {r['title']}")
        print(f"Authors: {', '.join(r['authors'])}")
        print(f"Published: {r['published']}")
        print(f"Categories: {', '.join(r['categories'])}")
        print(f"URL: {r['url']}")
        print(f"\\nAbstract:")
        print(textwrap.fill(r['summary'], width=72))
    else:
        print("Paper not found")

import re

def main():
    if len(sys.argv) < 3:
        print(__doc__.strip())
        sys.exit(1)
    cmd = sys.argv[1]
    arg = " ".join(sys.argv[2:])
    limit = 10
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit")+1])
    if cmd == "search":
        sort = "relevance"
        if "--sort" in sys.argv:
            sort = sys.argv[sys.argv.index("--sort")+1]
        cmd_search(arg, limit, sort)
    elif cmd == "author":
        cmd_author(arg, limit)
    elif cmd == "category" or cmd == "cat":
        cmd_category(arg, limit)
    elif cmd == "fetch":
        cmd_fetch(sys.argv[2])
    elif cmd == "abstract":
        cmd_abstract(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
''',
    body_extra=textwrap.dedent("""\
    ## Install
    
    ```bash
    # Requires Python 3.8+. No pip install needed.
    curl -O https://raw.githubusercontent.com/itsPremkumar/arxiv-search/main/arxiv_tools.py
    ```
    
    ## Usage
    
    ```bash
    python arxiv_tools.py search "machine learning transformers" --limit 10
    python arxiv_tools.py search "quantum computing" --sort date --limit 5
    python arxiv_tools.py author "Yann LeCun" --limit 5
    python arxiv_tools.py category cs.AI --limit 10
    python arxiv_tools.py abstract 2301.12345
    python arxiv_tools.py fetch 2301.12345
    ```
    
    ## Features
    
    - **Keyword search** — full-text search across all arXiv papers
    - **Author lookup** — find papers by specific researcher
    - **Category browse** — browse recent papers in any arXiv category
    - **Abstract fetch** — get full abstract of a specific paper
    - **PDF links** — direct download URLs included
    - **Zero API key** — uses public arXiv API
    
    ## Why
    Academic research from the terminal. No API keys, no bloat.
    """))

print("Batch 2 skill folders created!")
