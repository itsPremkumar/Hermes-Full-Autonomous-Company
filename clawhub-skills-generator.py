#!/usr/bin/env python3
"""Batch-generate ClawHub skill folders."""

import os
import json

SKILLS_DIR = r"C:\one\paperclip-company\clawhub-skills"

SKILL_DEFS = [
    {"slug": "codebase-inspection", "name": "Codebase Inspector", "description": "Analyze codebases: lines of code, language breakdowns, file-type ratios, and complexity metrics. Zero deps (Python stdlib).", "tags": ["codebase", "analysis", "metrics", "devtools"]},
    {"slug": "web-research", "name": "Web Research Toolkit", "description": "Route internet search, research, and lookup tasks through a unified CLI. DuckDuckGo + Wikipedia + fallback. Zero deps.", "tags": ["research", "web", "search", "cli"]},
    {"slug": "doc-extractor", "name": "Document Text Extractor", "description": "Extract text from PDFs, DOCX, and text files using stdlib tools. Convert scans to readable text with zero paid APIs.", "tags": ["ocr", "documents", "pdf", "text-extraction"]},
    {"slug": "ascii-art-creator", "name": "ASCII Art Creator", "description": "Generate ASCII art banners, boxes, cowsay messages, and image-to-ASCII conversions. Zero deps (Python stdlib).", "tags": ["ascii", "art", "text", "fun", "cli"]},
    {"slug": "json-tools", "name": "JSON Power Tools", "description": "Query, validate, diff, format, filter, and transform JSON files from the CLI. Zero deps (Python stdlib).", "tags": ["json", "data", "cli", "devtools"]},
    {"slug": "md-linter", "name": "Markdown Linter & Fixer", "description": "Lint, format, and fix common Markdown issues: broken links, inconsistent headings, missing frontmatter, and more. Stdlib.", "tags": ["markdown", "lint", "format", "documentation"]},
    {"slug": "file-watcher", "name": "File System Watcher", "description": "Watch directories for file changes (create, modify, delete) using polling. Python stdlib, no inotify needed.", "tags": ["file", "watch", "monitor", "fsnotify"]},
    {"slug": "secret-scanner", "name": "Secret Scanner", "description": "Scan files and directories for potential secrets, API keys, tokens, and credentials. Stdlib, offline, regex-based.", "tags": ["security", "secrets", "scan", "devtools"]},
]

def main():
    os.makedirs(SKILLS_DIR, exist_ok=True)
    for d in SKILL_DEFS:
        slug = d["slug"]
        sdir = os.path.join(SKILLS_DIR, slug)
        os.makedirs(sdir, exist_ok=True)
        tags_str = json.dumps(d["tags"])
        body = "# " + d["name"] + "\n\n" + d["description"] + "\n\nOne CLI tool to handle this task with zero dependencies."
        md = """---
name: {}
version: 1.0.0
description: {}
tags: {}
---
{}
""".format(slug, d["description"], tags_str, body)
        with open(os.path.join(sdir, "SKILL.md"), "w") as f:
            f.write(md.lstrip())
        print("  Created: {} -> {}".format(slug, sdir))
    print("\nDone! {} skill folders created.".format(len(SKILL_DEFS)))

if __name__ == "__main__":
    main()
