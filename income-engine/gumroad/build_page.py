#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Render the Gumroad products into docs/gumroad.html and copy each product's
PRODUCT.md into docs/products/<slug>/ so download links resolve.
Call this from build.py (or run standalone). Stdlib only.
"""
import os, json, html, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # income-engine/
PROD = os.path.join(ROOT, "gumroad", "products")
PUBLIC = os.path.join(ROOT, "docs")
CONFIG = os.path.join(ROOT, "config.json")

def load_cfg():
    return json.load(open(CONFIG, encoding="utf-8"))

def main():
    cfg = load_cfg()
    os.makedirs(os.path.join(PUBLIC, "products"), exist_ok=True)
    items = []
    if os.path.isdir(PROD):
        for slug in sorted(os.listdir(PROD)):
            pdir = os.path.join(PROD, slug)
            if not os.path.isdir(pdir):
                continue
            pm = os.path.join(pdir, "PRODUCT.md")
            txt = open(pm, encoding="utf-8").read() if os.path.isfile(pm) else ""
            # strip a leading "# title"
            txt = "\n".join(txt.split("\n")[1:]) if txt.startswith("#") else txt
            dest = os.path.join(PUBLIC, "products", slug)
            os.makedirs(dest, exist_ok=True)
            shutil.copy(pm, os.path.join(dest, "PRODUCT.md"))
            # pull price/title from LISTING.txt
            title, price = slug, ""
            lf = os.path.join(pdir, "LISTING.txt")
            if os.path.isfile(lf):
                for ln in open(lf, encoding="utf-8"):
                    if ln.lower().startswith("title:"):
                        title = ln.split(":", 1)[1].strip()
                    if ln.lower().startswith("price:"):
                        price = ln.split(":", 1)[1].strip()
            items.append({"slug": slug, "title": title, "price": price,
                          "blurb": txt.strip().split("\n")[0] if txt.strip() else ""})
    rows = "\n".join(
        f'<li><a href="products/{i["slug"]}/PRODUCT.md">{html.escape(i["title"])}</a>'
        f' — {html.escape(i["price"])}<br><span style="color:#777">{html.escape(i["blurb"])}</span></li>'
        for i in items) or "<li>No products yet — run generate_gumroad.py.</li>"
    body = "<h1>Digital Products</h1><p>Real, usable products built by the agent team. " \
           "Upload each to Gumroad (free) and set the listed price. You keep 100% minus Gumroad's fee.</p>" \
           f"<ul>{rows}</ul>"
    css = "body{font:16px/1.6 system-ui,Segoe UI,Arial,sans-serif;margin:0;color:#1a1a1a;background:#fafafa}" \
          "header{background:#111;color:#fff;padding:14px 20px;display:flex;justify-content:space-between;flex-wrap:wrap}" \
          ".brand{color:#fff;font-weight:700;text-decoration:none;font-size:18px}" \
          "nav a{color:#ddd;margin-left:16px;text-decoration:none}" \
          "main{max-width:820px;margin:30px auto;padding:0 18px}" \
          "footer{max-width:820px;margin:40px auto;padding:18px;color:#777;font-size:14px;border-top:1px solid #eee}" \
          "a{color:#0a66c2}li{margin:14px 0}"
    page = f"<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>" \
           f"<title>Products — {html.escape(cfg['site_name'])}</title><style>{css}</style></head>" \
           f"<body><header><a href=index.html class=brand>{html.escape(cfg['site_name'])}</a>" \
           f"<nav><a href=index.html>Home</a><a href=tools.html>Tools</a><a href=gumroad.html>Products</a>" \
           f"<a href=disclosure.html>Disclosure</a></nav></header><main>{body}</main>" \
           f"<footer>Prem Autonomous Co — zero-cost autonomous income systems.</footer></body></html>"
    open(os.path.join(PUBLIC, "gumroad.html"), "w", encoding="utf-8").write(page)
    print(f"rendered gumroad.html with {len(items)} products")

if __name__ == "__main__":
    main()
