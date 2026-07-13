#!/usr/bin/env python
"""stdlib-only static site generator for an affiliate content site.
Render:  python build.py   (reads ./content/*.md -> ./public/)"""
import json, os, re, html, datetime, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT, PUBLIC = os.path.join(ROOT, "content"), os.path.join(ROOT, "public")
CONFIG = os.path.join(ROOT, "config.json")


def load_config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def parse_article(path):
    raw = open(path, encoding="utf-8").read()
    fm, body = {}, raw
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            for ln in raw[3:end].split("\n"):
                if ":" in ln:
                    k, v = ln.split(":", 1)
                    v = v.strip()
                    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                        v = v[1:-1]
                    fm[k.strip()] = v
            body = raw[end + 4:].strip()
    return fm, body


def md_to_html(md):
    # minimal: #/##/###, >, -/*, 1., ```code```, **bold**, *em*, `code`, [text](url), ---
    lines, out, in_ul, in_ol = md.split("\n"), [], False, False

    def inline(t):
        t = html.escape(t)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
        return t

    def close():
        nonlocal in_ul, in_ol
        if in_ul: out.append("</ul>"); in_ul = False
        if in_ol: out.append("</ol>"); in_ol = False

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip(): close(); i += 1; continue
        if line.startswith("```"):
            close(); code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(html.escape(lines[i])); i += 1
            i += 1; out.append("<pre><code>" + "\n".join(code) + "</code></pre>"); continue
        if line.startswith("### "): close(); out.append("<h3>" + inline(line[4:]) + "</h3>")
        elif line.startswith("## "): close(); out.append("<h2>" + inline(line[3:]) + "</h2>")
        elif line.startswith("# "): close(); out.append("<h1>" + inline(line[2:]) + "</h1>")
        elif line.startswith("> "): close(); out.append("<blockquote>" + inline(line[2:]) + "</blockquote>")
        elif re.match(r"^\s*[-*] ", line):
            if not in_ul: close(); out.append("<ul>"); in_ul = True
            out.append("<li>" + inline(re.sub(r"^\s*[-*] ", "", line)) + "</li>")
        elif re.match(r"^\s*\d+\. ", line):
            if not in_ol: close(); out.append("<ol>"); in_ol = True
            out.append("<li>" + inline(re.sub(r"^\s*\d+\. ", "", line)) + "</li>")
        elif line.startswith("---"): close(); out.append("<hr>")
        else: close(); out.append("<p>" + inline(line) + "</p>")
        i += 1
    close()
    return "\n".join(out)


def expand_affiliate(text, cfg):
    tag = cfg.get("amazon_tag", "")

    def amz(m):
        kw = m.group(1).strip()
        base = f"https://www.amazon.com/s?k={urllib.parse.quote(kw)}"
        return f'<a href="{base}&tag={tag}">' if tag else f'<a href="{base}">'

    return re.sub(r"\{\{AMAZON:([^}]+)\}\}", amz, text)


def render(title, body, cfg, desc=""):
    return f"""<!DOCTYPE html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<meta name=description content="{html.escape(desc)}"><title>{html.escape(title)}</title>
<style>body{{font:16px/1.7 system-ui,sans-serif;max-width:760px;margin:auto;padding:30px 20px}}
h1,h2,h3{{line-height:1.25}}a{{color:#0a66c2}}code{{background:#f0f0f0;padding:1px 5px;border-radius:3px}}
pre{{background:#0d1117;color:#c9d1d9;padding:14px;border-radius:6px;overflow:auto}}
blockquote{{border-left:3px solid #ccc;margin:0;padding:4px 16px;color:#666}}</style></head>
<body><main>{body}</main>
<footer><p>Contains affiliate links; I may earn a commission at no extra cost to you.</p></footer></body></html>"""


def main():
    cfg = load_config(); site = cfg.get("site_url", "").rstrip("/")
    os.makedirs(PUBLIC, exist_ok=True); arts = []
    for fn in sorted(os.listdir(CONTENT)):
        if not fn.endswith(".md"): continue
        fm, body = parse_article(os.path.join(CONTENT, fn))
        title = fm.get("title", fn[:-3]); slug = fm.get("slug", slugify(title))
        desc = fm.get("description", title)
        page = render(title, md_to_html(expand_affiliate(body, cfg)), cfg, desc)
        open(os.path.join(PUBLIC, slug + ".html"), "w", encoding="utf-8").write(page)
        arts.append({"title": title, "slug": slug, "desc": desc})
        print("  built:", slug + ".html")
    index = md_to_html(f"# {cfg.get('site_name','Site')}\n\n{cfg.get('tagline','')}\n\n") + \
        "\n".join(f'<p><a href="{a["slug"]}.html"><strong>{html.escape(a["title"])}</strong></a><br>'
                  f'<span style="color:#666">{html.escape(a["desc"])}</span></p>' for a in arts)
    open(os.path.join(PUBLIC, "index.html"), "w", encoding="utf-8").write(render(cfg.get("site_name", "Site"), index, cfg))
    urls = "\n".join(f"  <url><loc>{site}/{a['slug']}.html</loc></url>" for a in arts)
    open(os.path.join(PUBLIC, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'<url><loc>{site}/</loc></url>\n{urls}\n</urlset>')
    print("DONE:", len(arts), "articles ->", PUBLIC)


if __name__ == "__main__":
    main()
