#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Stdlib-only static-site generator for the Paperclip income engine.
Reads content/*.md (frontmatter title/description/slug/date/niche),
renders index + article pages + sitemap + rss into docs/.
Expands affiliate tokens from config.json. NO pip installs.

Run:  python build.py
"""
import os, re, html, json, datetime, urllib.parse, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
SRC = os.path.join(ROOT, "src")
PUBLIC = os.path.join(ROOT, "docs")          # GitHub Pages serves /docs
CONFIG = os.path.join(ROOT, "config.json")

def load_config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)

def slugify(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")

def inline(t):
    t = html.escape(t)
    # links [text](url)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t

_md_block = re.compile(r"^(#{1,6})\s+(.*)$")
_md_ul = re.compile(r"^\s*[-*]\s+(.*)$")
_md_ol = re.compile(r"^\s*\d+\.\s+(.*)$")
_md_hr = re.compile(r"^---+$")

def md_to_html(md):
    out, i, lines = [], 0, md.split("\n")
    n = len(lines)
    list_stack = []
    def close_lists():
        while list_stack:
            out.append("</ol>" if list_stack.pop() == "ol" else "</ul>")
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1; continue
        if _md_hr.match(line):
            close_lists(); out.append("<hr>"); i += 1; continue
        m = _md_block.match(line)
        if m:
            close_lists()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>" + inline(m.group(2)) + f"</h{lvl}>")
            i += 1; continue
        m = _md_ul.match(line)
        if m:
            if not list_stack or list_stack[-1] != "ul":
                close_lists(); out.append("<ul>"); list_stack.append("ul")
            out.append("<li>" + inline(m.group(1)) + "</li>")
            i += 1; continue
        m = _md_ol.match(line)
        if m:
            if not list_stack or list_stack[-1] != "ol":
                close_lists(); out.append("<ol>"); list_stack.append("ol")
            out.append("<li>" + inline(m.group(1)) + "</li>")
            i += 1; continue
        close_lists()
        # paragraph; merge consecutive non-blank lines
        para = [line]
        j = i + 1
        while j < n and lines[j].strip() and not _md_block.match(lines[j]) \
              and not _md_ul.match(lines[j]) and not _md_ol.match(lines[j]) \
              and not _md_hr.match(lines[j]):
            para.append(lines[j]); j += 1
        out.append("<p>" + inline(" ".join(para)) + "</p>")
        i = j
    close_lists()
    return "\n".join(out)

def expand_affiliate(text, cfg):
    atag = cfg.get("amazon_tag", "")
    sid = cfg.get("shareasale_id", "")
    fid = cfg.get("fiverr_aff_id", "")
    def a_repl(m):
        kw = urllib.parse.quote(m.group(1).strip())
        url = f"https://www.amazon.com/s?k={kw}"
        if atag:
            url += f"&tag={atag}"
        return f'<a href="{url}">'
    text = re.sub(r"\{\{AMAZON:([^}]+)\}\}", a_repl, text)
    def s_repl(m):
        uid = m.group(1).strip(); kw = m.group(2).strip()
        url = f"https://www.shareasale.com/shareasale.cfm?merchantID={sid}" if sid else "https://www.shareasale.com"
        return f'<a href="{url}">{kw}</a>'
    text = re.sub(r"\{\{SHAREASALE:([^:]+):([^}]+)\}\}", s_repl, text)
    def f_repl(m):
        cat = m.group(1).strip()
        url = f"https://www.fiverr.com/categories/{cat}?source=affiliate_fiverr&aff_id={fid}" if fid else f"https://www.fiverr.com/categories/{cat}"
        return f'<a href="{url}">'
    text = re.sub(r"\{\{FIVERR:([^}]+)\}\}", f_repl, text)
    return text

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

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {site}</title>
<meta name="description" content="{desc}">
<style>{css}</style></head>
<body>
<header><a href="index.html" class="brand">{site}</a>
<nav><a href="index.html">Home</a><a href="tools.html">Tools</a><a href="gumroad.html">Products</a><a href="disclosure.html">Disclosure</a></nav></header>
<main>{body}</main>
<footer><p>{site} — zero-cost autonomous income systems by {company}. Contact {email}.</p>
<p><a href="disclosure.html">Affiliate disclosure</a></p></footer></body></html>"""

CSS = "body{font:16px/1.6 system-ui,Segoe UI,Arial,sans-serif;margin:0;color:#1a1a1a;background:#fafafa}"
CSS += "header{background:#111;color:#fff;padding:14px 20px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap}"
CSS += ".brand{color:#fff;font-weight:700;text-decoration:none;font-size:18px}"
CSS += "nav a{color:#ddd;margin-left:16px;text-decoration:none}"
CSS += "nav a:hover{color:#fff}"
CSS += "main{max-width:820px;margin:30px auto;padding:0 18px}"
CSS += "footer{max-width:820px;margin:40px auto;padding:18px;color:#777;font-size:14px;border-top:1px solid #eee}"
CSS += "h1,h2,h3{line-height:1.25}"
CSS += "a{color:#0a66c2}"
CSS += "ul,ol{margin-left:20px}"
CSS += ".meta{color:#888;font-size:14px;margin-bottom:20px}"

def render_page(cfg, title, body, desc=""):
    return PAGE.format(title=title, site=cfg["site_name"], desc=desc or cfg["tagline"],
                       css=CSS, body=body, company=cfg["company"], email=cfg["contact_email"])

def main():
    cfg = load_config()
    # clean build dir (avoid stale artifacts)
    if os.path.isdir(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(PUBLIC, exist_ok=True)

    articles = []
    if os.path.isdir(CONTENT):
        for fn in sorted(os.listdir(CONTENT)):
            if not fn.endswith(".md"):
                continue
            fm, body = parse_article(os.path.join(CONTENT, fn))
            slug = fm.get("slug", slugify(fm.get("title", fn[:-3])))
            body = expand_affiliate(body, cfg)
            html_body = md_to_html(body)
            meta = f'<p class="meta">Published {fm.get("date","")} · niche: {fm.get("niche","")}</p>' if fm.get("date") else ""
            full = meta + html_body
            open(os.path.join(PUBLIC, slug + ".html"), "w", encoding="utf-8").write(
                render_page(cfg, fm.get("title", slug), full, fm.get("description", "")))
            articles.append({"title": fm.get("title", slug), "slug": slug,
                             "desc": fm.get("description", ""), "date": fm.get("date", "")})

    # index
    cards = "\n".join(
        f'<li><a href="{a["slug"]}.html">{html.escape(a["title"])}</a> — {html.escape(a["desc"])}</li>'
        for a in articles)
    index_body = "<h1>Zero-Cost AI Agent Income Lab</h1><p>" + html.escape(cfg["tagline"]) + "</p>"
    index_body += "<p>An autonomous income system operated by the Paperclip agent company. Every article, product, and tool below is generated and published by Hermes agents at $0 cost.</p>"
    index_body += "<h2>Latest guides</h2><ul>" + cards + "</ul>"
    index_body += "<p><a href='gumroad.html'>Browse digital products</a> · <a href='tools.html'>Free tools</a></p>"
    open(os.path.join(PUBLIC, "index.html"), "w", encoding="utf-8").write(
        render_page(cfg, "Home", index_body))

    # copy static src assets
    if os.path.isdir(SRC):
        for fn in os.listdir(SRC):
            shutil.copy(os.path.join(SRC, fn), os.path.join(PUBLIC, fn))

    # build gumroad products page + copy products into docs/ (self-invoked so
    # rm -rf docs above never leaves a dangling gumroad.html link)
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "gumroad_build", os.path.join(ROOT, "gumroad", "build_page.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()
    except Exception as e:
        print("gumroad build skipped:", e)

    # disclosure
    disc = "<h1>Affiliate Disclosure</h1><p>This site is operated by " + html.escape(cfg["company"]) + \
           ". Some links are affiliate links. If you buy through them we may earn a commission at no extra cost to you. " + \
           "This does not affect our editorial independence. The site is built and published autonomously by AI agents; " + \
           "the human owner only performs free one-time account linking.</p>"
    open(os.path.join(PUBLIC, "disclosure.html"), "w", encoding="utf-8").write(
        render_page(cfg, "Disclosure", disc))

    # sitemap
    urls = [f"{cfg['site_url']}/{a['slug']}.html" for a in articles] + \
           [f"{cfg['site_url']}/index.html", f"{cfg['site_url']}/tools.html",
            f"{cfg['site_url']}/gumroad.html", f"{cfg['site_url']}/disclosure.html"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.s3.org/2000/urlset">\n' + \
         "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls) + "\n</urlset>\n"
    open(os.path.join(PUBLIC, "sitemap.xml"), "w", encoding="utf-8").write(sm)

    # rss
    items = "\n".join(
        f"  <item><title>{html.escape(a['title'])}</title><link>{cfg['site_url']}/{a['slug']}.html</link>"
        f"<description>{html.escape(a['desc'])}</description><pubDate>{a['date']}</pubDate></item>"
        for a in articles)
    rss = f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>{html.escape(cfg["site_name"])}</title>' \
          f'<link>{cfg["site_url"]}</link><description>{html.escape(cfg["tagline"])}</description>\n{items}\n</channel></rss>\n'
    open(os.path.join(PUBLIC, "feed.xml"), "w", encoding="utf-8").write(rss)

    print(f"built {len(articles)} articles + index + tools + gumroad + disclosure -> {PUBLIC}")
    print("sitemap.xml / feed.xml written")

if __name__ == "__main__":
    main()
