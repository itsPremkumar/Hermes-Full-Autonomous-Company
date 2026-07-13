#!/usr/bin/env python3
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
                return "\n".join(transcript) if transcript else None
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
                    return "\n".join(transcript)
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
            print(f"\n[... truncated, full length: {len(transcript)} chars]")
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
    sentences = re.split(r'(?<=[.!?])\s+', transcript)
    summary = []
    char_count = 0
    for s in sentences[:20]:
        summary.append(s)
        char_count += len(s)
        if char_count >= 800:
            break
    print("=== Summary ===")
    print(" ".join(summary))
    print(f"\n(Full transcript: {len(transcript)} chars)")

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
    title = re.sub(r'\s*-\s*YouTube$', '', title)
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

def _self_test():
    """Real test of the video-id extraction core (no network). Returns 0/1."""
    cases = [
        ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/embed/dQw4w9WgXcQ", "dQw4w9WgXcQ"),
        ("https://www.youtube.com/shorts/abcdefghijk", "abcdefghijk"),
        ("dQw4w9WgXcQ", "dQw4w9WgXcQ"),
    ]
    for url, expected in cases:
        got = extract_video_id(url)
        if got != expected:
            print(f"self-test: FAIL (extract_video_id({url!r}) = {got!r}, want {expected!r})")
            return 1
    # Invalid input yields None.
    if extract_video_id("this is definitely not a url") is not None:
        print("self-test: FAIL (invalid input should yield None)")
        return 1
    print("self-test: PASS")
    return 0


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "self-test":
        sys.exit(_self_test())
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
