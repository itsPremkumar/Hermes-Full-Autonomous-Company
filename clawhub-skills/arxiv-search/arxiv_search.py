#!/usr/bin/env python3
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
    title = title.text.strip().replace("\n", " ") if title is not None else "Untitled"
    summary = entry.find("summary", ns)
    summary = summary.text.strip()[:500] if summary is not None else ""
    summary = re.sub(r'\s+', ' ', summary)
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
        print(f"\nAbstract:")
        print(textwrap.fill(r['summary'], width=72))
    else:
        print("Paper not found")

import re

def _self_test():
    """Real test of the core Atom entry parser (no network). Returns 0/1."""
    import xml.etree.ElementTree as ET
    ns = {"": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    fake = (
        '<entry xmlns="http://www.w3.org/2005/Atom" '
        'xmlns:arxiv="http://arxiv.org/schemas/atom">'
        '<id>http://arxiv.org/abs/1234.5678v2</id>'
        '<title>Hello World</title>'
        '<summary>An  example  abstract.</summary>'
        '<published>2021-01-02</published>'
        '<author><name>Jane Doe</name></author>'
        '<category term="cs.LG"/>'
        '<link title="pdf" href="http://x/p.pdf"/>'
        '</entry>'
    )
    entry = ET.fromstring(fake)
    r = _parse_entry(entry)
    if r["id"] != "1234.5678":
        print("self-test: FAIL (id parse)")
        return 1
    if r["title"] != "Hello World":
        print("self-test: FAIL (title parse)")
        return 1
    if r["authors"] != ["Jane Doe"]:
        print("self-test: FAIL (authors parse)")
        return 1
    if r["published"] != "2021-01-02":
        print("self-test: FAIL (published parse)")
        return 1
    if "cs.LG" not in r["categories"]:
        print("self-test: FAIL (category parse)")
        return 1
    if r["pdf_url"] != "http://x/p.pdf":
        print("self-test: FAIL (pdf url parse)")
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
