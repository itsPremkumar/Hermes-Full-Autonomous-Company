#!/usr/bin/env python3
"""Generate marketing layer:
  - marketing/showcase.html  (SEO/AEO/GEO optimized showcase landing page)
  - marketing/moltbook-drafts/<slug>.md  (31 Moltbook announcement drafts)
Driven by the same per-skill COPY used for docs + the real inventory.
"""
import os, json, re

BASE = r"C:\one\paperclip-company"
INV = os.path.join(BASE, "tools", "_seo_inventory.json")
inv = json.load(open(INV, encoding="utf-8"))

BRAND = "itsPremkumar"
STACK = "Hermes / OpenClaw / Paperclip"
GITHUB = "https://github.com/itsPremkumar"
PROFILE = "https://clawhub.ai/itspremkumar"
LICENSE = "MIT-0"

COPY = {
"agent-caps": dict(title="Agent Capability Manifest Toolkit", one="Validate, scaffold, and cross-check AI-agent capability manifests so agents stay swappable, auditable, and safe.", cat="Agent safety"),
"agent-cost-tracker": dict(title="LLM Cost & Token Tracker", one="Estimate and tally LLM API spending per agent/session with budget alerts and CSV export.", cat="FinOps"),
"agent-guardrails": dict(title="Agent Action Guardrails", one="Pre-flight safety gate for planned agent actions: permission checks, allowlists, and an audit trail.", cat="Agent safety"),
"agent-health": dict(title="Agent Endpoint Health Monitor", one="Probe agent dependency endpoints for up/down status and latency.", cat="Observability"),
"agent-logger": dict(title="Agent Run Log Analyzer", one="Analyze agent run logs for errors, token spikes, and failures with JSON output.", cat="Observability"),
"agent-sentinel": dict(title="Skill Security Sentinel", one="Scan OpenClaw/Hermes skills for risky permission patterns before you install them.", cat="Security"),
"airtable-cli": dict(title="Airtable API CLI", one="Full Airtable client: bases, tables, records with pagination, CSV import/export, and rate-limit awareness.", cat="Automation"),
"arxiv-search": dict(title="arXiv Research Search", one="Search arXiv papers by keyword, author, or category with citation export.", cat="Research"),
"ascii-art-creator": dict(title="ASCII Art Creator", one="Generate banners, boxes, cowsay-style art, tables, and image-to-ASCII in your terminal.", cat="Creative"),
"ascii-video": dict(title="ASCII Video Converter", one="Convert video to ASCII animation with dithering modes, color output, and framerate control.", cat="Creative"),
"codebase-inspection": dict(title="Codebase Inspector", one="Walk any directory and report language breakdowns, line counts, HTML reports, git-aware diffs, trend tracking, SVG badges, CSV export.", cat="DevTools"),
"company-ops": dict(title="Autonomous Company OS", one="Run a self-improving autonomous company from a single CONSTITUTION plus a confidence-gated loop.", cat="Agent ops"),
"cron-doctor": dict(title="Cron Doctor", one="Validate and diagnose a scheduled-task file: parse errors, unsafe commands, collisions, missed/overlapping runs.", cat="DevTools"),
"dev-prompts": dict(title="Developer Prompts Pack", one="150 curated developer-productivity prompts you can paste into any agent.", cat="Prompts"),
"doc-extractor": dict(title="Document Text Extractor", one="Extract text from PDF, DOCX, and TXT with encoding detection and page/paragraph structure.", cat="Documents"),
"excalidraw-cli": dict(title="Excalidraw Diagram CLI", one="Generate Excalidraw diagrams — flowcharts, sequences, architecture — as valid .excalidraw JSON.", cat="Diagrams"),
"file-watcher": dict(title="File Watcher", one="Monitor directories for changes: snapshots, diffs, glob filtering, and event detection.", cat="Automation"),
"gif-search": dict(title="GIF Search (Tenor)", one="Search and download GIFs from Tenor with caching, bulk download, and format conversion.", cat="Creative"),
"json-tools": dict(title="JSON Toolkit", one="Validate, format, query, diff, filter, flatten, and merge JSON with dot-notation paths.", cat="Data"),
"manifest-diff": dict(title="Manifest Diff", one="Diff two agent/skill manifests and report capability, permission, and version changes.", cat="Agent safety"),
"maps-cli": dict(title="Maps CLI (OpenStreetMap)", one="Geocode, reverse-geocode, route, POI search, and timezone lookup via OpenStreetMap, with CSV export.", cat="Location"),
"md-linter": dict(title="Markdown Linter & Formatter", one="Lint and auto-format Markdown: trailing whitespace, frontmatter validation, TOC generation, external link checks.", cat="Docs"),
"notion-api": dict(title="Notion API CLI", one="Complete Notion client: pages, databases, blocks, and search with config file and dry-run mode.", cat="Productivity"),
"polymarket-cli": dict(title="Polymarket CLI", one="Query Polymarket prediction markets: search, price history, trending, categories, and stats.", cat="Data"),
"prompt-lint": dict(title="Prompt Linter", one="Lint AI prompts for clarity, safety, injection risk, and template validity — scored 0-100.", cat="Prompts"),
"prompt-templates-cli": dict(title="Prompt Templates CLI", one="Manage reusable prompt templates: create, render, and validate with {{variables}}.", cat="Prompts"),
"secret-scanner": dict(title="Secret Scanner", one="Detect API keys, tokens, and credentials in code with 50+ patterns, entropy analysis, and SARIF reports.", cat="Security"),
"skill-benchmark": dict(title="Skill Benchmark", one="Composite quality score (A-F) for OpenClaw/Hermes skills: structure, docs, safety, self-test.", cat="Quality"),
"skill-lint": dict(title="Skill Linter", one="Validate ClawHub/OpenClaw skill folders before publishing: frontmatter, structure, command docs, thin-content detection.", cat="Quality"),
"web-research": dict(title="Web Research Toolkit", one="Route search, research, and lookups through one CLI — DuckDuckGo, Wikipedia, and URL fetch — zero dependencies.", cat="Research"),
"youtube-content": dict(title="YouTube Content Toolkit", one="Extract transcripts, summaries, and metadata from YouTube videos for content repurposing.", cat="Content"),
}

CATS = {}
for slug, c in COPY.items():
    CATS.setdefault(c["cat"], []).append(slug)

def clawhub_url(slug):
    return f"{PROFILE}/skills/{slug}"

# ---------- 1) Showcase landing page ----------
links_html = []
for slug, c in COPY.items():
    links_html.append(
        f'      <article class="card">\n'
        f'        <span class="tag">{c["cat"]}</span>\n'
        f'        <h3><a href="{clawhub_url(slug)}">{c["title"]}</a></h3>\n'
        f'        <p>{c["one"]}</p>\n'
        f'        <a class="btn" href="{clawhub_url(slug)}">View on ClawHub &rarr;</a>\n'
        f'      </article>'
    )
links_html = "\n".join(links_html)

cats_html = "".join(f'<li><a href="#{cat.lower().replace(" ","-")}">{cat}</a></li>' for cat in CATS)

faqs = [
    ("What are these tools?", "31 free, open-source, MIT-0 licensed command-line tools for AI agents, automation, research, security, and content — built and maintained by itsPremkumar."),
    ("Do they need API keys or internet?", "Most run fully offline on Python 3.8+ stdlib. A few (arxiv, maps, gif, notion, polymarket, youtube, web-research) call public APIs; none require paid keys for basic use."),
    ("How do I install one?", "Open its ClawHub page and run the shown curl/install command. No pip needed — each tool is a single self-contained Python file."),
    ("Are they CI-tested?", "Yes. Every tool ships a self-test and a GitHub Actions pipeline that runs a 7-axis verification harness on Python 3.8 and 3.11."),
    ("Who maintains them?", f"{BRAND}, based in Chennai, India, serving developers worldwide as part of the {STACK} autonomous product stack."),
]

faq_html = "\n".join(
    f'    <div class="faq">\n      <h3>{q}</h3>\n      <p>{a}</p>\n    </div>' for q, a in faqs
)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>31 Free AI Agent Tools — ClawHub Skills by itsPremkumar</title>
<meta name="description" content="31 free, open-source MIT-licensed CLI tools for AI agents, automation, research, security, and content. Zero-dependency Python. Install in one command from ClawHub." />
<meta name="keywords" content="AI agent tools, CLI tools, open source, Python, automation, ClawHub, OpenClaw, Hermes, agent safety, LLM cost tracker, secret scanner, web research, arXiv search" />
<meta name="author" content="itsPremkumar" />
<meta name="robots" content="index, follow" />
<meta property="og:title" content="31 Free AI Agent Tools by itsPremkumar" />
<meta property="og:description" content="Zero-dependency, MIT-licensed CLI tools for agents, automation, research, and security." />
<meta property="og:type" content="website" />
<meta property="og:url" content="{PROFILE}" />
<link rel="canonical" href="{PROFILE}" />
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "31 Free AI Agent Tools by itsPremkumar",
  "description": "A curated collection of 31 MIT-licensed command-line tools for AI agents, automation, research, security, and content.",
  "url": "{PROFILE}",
  "author": {{ "@type": "Person", "name": "itsPremkumar", "url": "{GITHUB}" }},
  "mainEntity": {{
    "@type": "ItemList",
    "numberOfItems": 31,
    "itemListElement": [
''' + ",\n".join(
    f'      {{ "@type": "SoftwareApplication", "name": "{c["title"]}", "url": "{clawhub_url(slug)}", "applicationCategory": "DeveloperApplication", "operatingSystem": "Windows, macOS, Linux", "license": "{LICENSE}" }}'
    for slug, c in COPY.items()
) + '''
    ]
  }}
}}
</script>
<style>
:root{{--bg:#0b0e14;--card:#141925;--fg:#e6e9ef;--mut:#9aa4b2;--acc:#ff5b5b;--bd:#26303f}}
*{{box-sizing:border-box}}
body{{margin:0;font:16px/1.6 system-ui,Segoe UI,Roboto,Arial,sans-serif;background:var(--bg);color:var(--fg)}}
header{{padding:48px 20px 28px;text-align:center;background:linear-gradient(180deg,#11151d,#0b0e14)}}
h1{{font-size:2.4rem;margin:0 0 8px}}
.sub{{color:var(--mut);max-width:720px;margin:0 auto}}
.wrap{{max-width:1100px;margin:0 auto;padding:0 20px 60px}}
nav.cats{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:22px 0;list-style:none;padding:0}}
nav.cats a{{color:var(--acc);text-decoration:none;border:1px solid var(--bd);padding:4px 10px;border-radius:999px;font-size:.85rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-top:24px}}
.card{{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:18px}}
.card h3{{margin:.2em 0 .4em;font-size:1.1rem}}
.card h3 a{{color:var(--fg);text-decoration:none}}
.card p{{color:var(--mut);font-size:.92rem;min-height:62px}}
.tag{{display:inline-block;font-size:.72rem;color:var(--acc);border:1px solid var(--acc);border-radius:6px;padding:1px 7px}}
.btn{{display:inline-block;margin-top:8px;color:var(--acc);text-decoration:none;font-weight:600}}
.faq{{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:14px 18px;margin-top:14px}}
.faq h3{{margin:0 0 6px;font-size:1rem;color:var(--acc)}}
footer{{text-align:center;color:var(--mut);padding:30px;border-top:1px solid var(--bd)}}
footer a{{color:var(--acc)}}
</style>
</head>
<body>
<header>
  <h1>31 Free AI Agent Tools</h1>
  <p class="sub">Zero-dependency, MIT-licensed command-line tools for AI agents, automation, research, security, and content. Built by <a href="{GITHUB}" style="color:var(--acc)">itsPremkumar</a> as part of the {STACK} stack. Install any tool in one command.</p>
  <p class="sub"><a href="{PROFILE}" style="color:var(--acc)">View the full ClawHub profile &rarr;</a></p>
</header>
<div class="wrap">
  <ul class="cats">{cats_html}</ul>
  <section class="grid">
{links_html}
  </section>
  <h2 style="margin-top:40px">Frequently asked questions</h2>
{faq_html}
</div>
<footer>
  <p>&copy; itsPremkumar &middot; <a href="{GITHUB}">GitHub</a> &middot; <a href="{PROFILE}">ClawHub</a> &middot; MIT-0 licensed</p>
  <p>Built in Chennai, India — serving developers worldwide.</p>
</footer>
</body>
</html>
'''

os.makedirs(os.path.join(BASE, "marketing"), exist_ok=True)
open(os.path.join(BASE, "marketing", "showcase.html"), "w", encoding="utf-8").write(html)

# ---------- 2) Moltbook drafts ----------
drafts_dir = os.path.join(BASE, "marketing", "moltbook-drafts")
os.makedirs(drafts_dir, exist_ok=True)
for slug, c in COPY.items():
    text = (
        f"🚀 {c['title']} — now live on ClawHub\n\n"
        f"{c['one']}\n\n"
        f"✅ Free & open-source (MIT-0)\n"
        f"✅ Zero dependencies — Python 3.8+, single file\n"
        f"✅ CI-tested with self-test + 7-axis verification\n\n"
        f"👉 Install / docs: {clawhub_url(slug)}\n\n"
        f"Part of 31 free agent-native tools by @itsPremkumar: {PROFILE}\n\n"
        f"#buildinpublic #opensource #aiagents #cli #devtools #automation"
    )
    open(os.path.join(drafts_dir, f"{slug}.md"), "w", encoding="utf-8").write(text)

# ---------- 3) master index ----------
index = "# Moltbook Announcement Drafts\n\n"
index += f"Profile: {PROFILE}\n\n"
index += "One file per skill. Post one per autonomy tick (rate-limited to ~1/min; cron runs 30-min cadence).\n\n"
for slug, c in COPY.items():
    index += f"- [{c['title']}]({clawhub_url(slug)}) — `moltbook-drafts/{slug}.md`\n"
open(os.path.join(drafts_dir, "README.md"), "w", encoding="utf-8").write(index)

print("showcase.html +", len(COPY), "Moltbook drafts written to marketing/")
