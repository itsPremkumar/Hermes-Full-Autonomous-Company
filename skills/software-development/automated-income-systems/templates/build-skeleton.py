#!/usr/bin/env python
"""
Stdlib-only static-site generator skeleton (zero pip installs).
Reproduce + modify for any content/affiliate site.

Layout:
  config.json        site name, niches, affiliate IDs (user fills)
  content/*.md       articles w/ frontmatter (title/description/slug/date/niche)
  src/tools.html      static client-side tools hub (copied to docs/)
  docs/              BUILT SITE (GitHub Pages serves /docs)
"""
import os, re, html, json, datetime, urllib.parse, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
PUBLIC = os.path.join(ROOT, "docs")          # GitHub Pages serves /docs
CONFIG = os.path.join(ROOT, "config.json")
SITE_URL = "https://USERNAME.github.io/money-engine"

def load_config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)

def slugify(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")

def md_to_html(md):
    out, in_ul = [], False
    def inline(t):
        t = html.escape(t)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
        return t
    for line in md.split("\n"):
        if line.startswith("## "):
            out.append("<h2>" + inline(line[3:]) + "</h2>")
        elif line.startswith("# "):
            out.append("<h1>" + inline(line[2:]) + "</h1>")
        elif re.match(r"^\s*[-*] ", line):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append("<li>" + inline(line.strip()[2:]) + "</li>")
        elif line.strip() == "":
            if in_ul: out.append("</ul>"); in_ul = False
        else:
            out.append("<p>" + inline(line) + "</p>")
    if in_ul: out.append("</ul>")
    return "\n".join(out)

def expand_affiliate(text, cfg):
    tag = cfg.get("amazon_tag", "")
    def repl(m):
        kw = urllib.parse.quote(m.group(1).strip())
        return f'<a href="https://www.amazon.com/s?k={kw}&tag={tag}">' if tag \
               else f'<a href="https://www.amazon.com/s?k={kw}">'
    return re.sub(r"\{\{AMAZON:([^}]+)\}\}", repl, text)

def parse_article(path):
    raw = open(path, encoding="utf-8").read()
    fm, body = {}, raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            for ln in raw[3:end].split("\n"):
                if ":" in ln:
                    k, v = ln.split(":", 1); v = v.strip()
                    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                        v = v[1:-1]
                    fm[k.strip()] = v
            body = raw[end + 4:].strip()
    return fm, body

def main():
    cfg = load_config()
    os.makedirs(PUBLIC, exist_ok=True)
    articles = []
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.endswith(".md"):
            continue
        fm, body = parse_article(os.path.join(CONTENT, fn))
        slug = fm.get("slug", slugify(fm.get("title", fn[:-3])))
        body = expand_affiliate(body, cfg)
        html_body = md_to_html(body)
        open(os.path.join(PUBLIC, slug + ".html"), "w", encoding="utf-8").write(html_body)
        articles.append({"title": fm.get("title", slug), "slug": slug})
    src_tools = os.path.join(ROOT, "src", "tools.html")
    if os.path.isfile(src_tools):
        shutil.copy(src_tools, os.path.join(PUBLIC, "tools.html"))
    print(f"built {len(articles)} articles -> {PUBLIC}")

if __name__ == "__main__":
    main()
