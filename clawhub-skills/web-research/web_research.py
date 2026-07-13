#!/usr/bin/env python3
"""
Web Research Toolkit — search, wiki lookup, and URL fetch from the terminal.

Backends (all stdlib, no API keys):
  - DuckDuckGo Lite HTML search (urllib + HTMLParser)
  - Wikipedia Action API (urllib + json)
  - Raw URL fetch / text extraction (urllib + HTMLParser)

Usage:
  python web_research.py search <query> [--count N]
  python web_research.py wiki <term> [--full]
  python web_research.py fetch <url> [--output file]
"""

import argparse
import html.parser
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from typing import List, Optional


# ── Helpers ──────────────────────────────────────────────────────────────────

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)


def _fetch(url: str, timeout: int = 15) -> str:
    """GET a URL and return the response body as text."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        # Try UTF-8, fall back to latin-1
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError:
            return raw.decode("latin-1")


def _strip_html(html_text: str) -> str:
    """Remove HTML tags and decode common entities."""

    SKIP_TAGS = {"script", "style", "noscript"}

    class _Parser(html.parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self._text = []
            self._skip = set()

        def handle_starttag(self, tag, attrs):
            if tag in SKIP_TAGS:
                self._skip.add(tag)

        def handle_endtag(self, tag):
            self._skip.discard(tag)

        def handle_data(self, data):
            if not self._skip:
                self._text.append(data)

        def get_text(self):
            return "".join(self._text)

    parser = _Parser()
    parser.feed(html_text)
    text = parser.get_text()
    # Decode common entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'")
    # Collapse whitespace
    text = re.sub(r"\n\s*\n", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


# ── Search (DuckDuckGo Lite) ────────────────────────────────────────────────


def _search_ddg(query: str, count: int = 5) -> List[dict]:
    """Search DuckDuckGo Lite and return result dicts."""
    url = "https://lite.duckduckgo.com/lite/"
    data = urllib.parse.urlencode({"q": query}).encode()
    req = urllib.request.Request(
        url, data=data, headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        html_text = resp.read().decode("utf-8", errors="replace")

    # Parse the result table — DuckDuckGo Lite uses a simple HTML table
    results = []
    # Find all result rows: <tr> with class or structure containing links
    # Pattern: look for <a rel="nofollow" href="...">text</a>
    link_pattern = re.compile(
        r'<a\s+rel="nofollow"\s+href="([^"]+)"[^>]*>(.*?)</a>', re.DOTALL
    )
    snippet_pattern = re.compile(
        r'<td\s+class="result-snippet">(.*?)</td>', re.DOTALL
    )

    links = link_pattern.findall(html_text)
    snippets = snippet_pattern.findall(html_text)

    for i, (url_href, title_html) in enumerate(links[:count]):
        title = _strip_html(title_html).strip()
        snippet = _strip_html(snippets[i]).strip() if i < len(snippets) else ""
        results.append({"title": title, "url": url_href, "snippet": snippet})

    return results


def cmd_search(args: argparse.Namespace) -> None:
    query = " ".join(args.query)
    count = min(args.count or 5, 20)
    results = _search_ddg(query, count)

    if not results:
        print(f"⚠  No results found for '{query}'")
        return

    print(f"🔍  DuckDuckGo results for: {query}\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   {r['url']}")
        if r["snippet"]:
            print(f"   {r['snippet'][:200]}")
        print()


# ── Wikipedia ────────────────────────────────────────────────────────────────


def _wiki_summary(term: str) -> Optional[dict]:
    """Fetch a Wikipedia summary via the MediaWiki action API."""
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "titles": term,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1,
        }
    )
    url = f"https://en.wikipedia.org/w/api.php?{params}"
    data = json.loads(_fetch(url))
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            return None
        return {
            "title": page.get("title", term),
            "extract": page.get("extract", ""),
            "page_id": page_id,
            "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page.get('title', term).replace(' ', '_'))}",
        }
    return None


def _wiki_full(term: str) -> Optional[dict]:
    """Fetch full Wikipedia article content."""
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "titles": term,
            "prop": "extracts",
            "explaintext": True,
            "redirects": 1,
        }
    )
    url = f"https://en.wikipedia.org/w/api.php?{params}"
    data = json.loads(_fetch(url))
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            return None
        return {
            "title": page.get("title", term),
            "extract": page.get("extract", ""),
            "page_id": page_id,
            "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page.get('title', term).replace(' ', '_'))}",
        }
    return None


def cmd_wiki(args: argparse.Namespace) -> None:
    term = " ".join(args.term)
    full = args.full

    result = _wiki_full(term) if full else _wiki_summary(term)
    if not result:
        print(f"⚠  No Wikipedia article found for '{term}'")
        return

    print(f"📖  Wikipedia: {result['title']}")
    print(f"   {result['url']}\n")
    print(result["extract"][:5000])
    if len(result["extract"]) > 5000:
        print("\n… (article truncated)")
    print()


# ── Fetch URL ───────────────────────────────────────────────────────────────


def cmd_fetch(args: argparse.Namespace) -> None:
    url = args.url
    try:
        html_text = _fetch(url)
    except Exception as e:
        print(f"⚠  Failed to fetch {url}: {e}", file=sys.stderr)
        sys.exit(1)

    text = _strip_html(html_text)
    # Show title if we can find it
    title_match = re.search(r"<title>(.*?)</title>", html_text, re.DOTALL)
    title = _strip_html(title_match.group(1)) if title_match else url

    output = args.output
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅  Downloaded {url}")
        print(f"   Title: {title}")
        print(f"   Saved to: {output}  ({len(text)} chars)")
    else:
        print(f"📄  {title}\n")
        print(text[:3000])
        if len(text) > 3000:
            print("\n… (output truncated, use --output to save full text)")


# ── CLI ─────────────────────────────────────────────────────────────────────


def _self_test():
    """Real test of the HTML-stripping core (_strip_html). Returns 0/1."""
    html_in = "<html><head><title>T</title></head><body><p>Hello &amp; world</p><script>bad()</script></body></html>"
    text = _strip_html(html_in)
    if "Hello" not in text or "&amp;" in text:
        print(f"self-test: FAIL (strip_html entities/content: {text!r})")
        return 1
    if "bad()" in text:
        print("self-test: FAIL (script content leaked)")
        return 1
    # Script/style content must be dropped.
    js = "<div>keep</div><script>var x = 1;</script>"
    if "var x" in _strip_html(js):
        print("self-test: FAIL (script tag not stripped)")
        return 1
    print("self-test: PASS")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Web Research Toolkit — search, Wikipedia, and URL fetch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s search \"Python 3.13 features\"\n"
            "  %(prog)s search \"climate report\" --count 10\n"
            "  %(prog)s wiki \"Transformer (machine learning)\"\n"
            "  %(prog)s wiki \"Attention Is All You Need\" --full\n"
            "  %(prog)s fetch https://example.com\n"
            "  %(prog)s fetch https://docs.python.org/3/ --output docs.txt\n"
        ),
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # search
    p_search = sub.add_parser("search", help="Search the web via DuckDuckGo")
    p_search.add_argument("query", nargs="+", help="Search query")
    p_search.add_argument("--count", type=int, default=5, help="Number of results (max 20)")

    # wiki
    p_wiki = sub.add_parser("wiki", help="Look up a Wikipedia article")
    p_wiki.add_argument("term", nargs="+", help="Article title or search term")
    p_wiki.add_argument("--full", action="store_true", help="Show full article")

    # fetch
    p_fetch = sub.add_parser("fetch", help="Fetch a URL and extract readable text")
    p_fetch.add_argument("url", help="URL to fetch")
    p_fetch.add_argument("--output", "-o", help="Save output to file")

    # self-test
    sub.add_parser("self-test", help="Run built-in self tests")

    args = parser.parse_args()

    if args.command == "search":
        cmd_search(args)
    elif args.command == "wiki":
        cmd_wiki(args)
    elif args.command == "fetch":
        cmd_fetch(args)
    elif args.command == "self-test":
        sys.exit(_self_test())
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
