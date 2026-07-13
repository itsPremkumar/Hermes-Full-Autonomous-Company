---
name: Markdown Linter & Fixer
version: 1.0.0
description: Lint, check, and auto-fix Markdown files — table of contents, broken links, YAML frontmatter validation, and formatting. Zero dependencies (Python stdlib).
tags: markdown, lint, format, documentation, python
---

# Markdown Linter & Fixer

A zero-dependency CLI tool to lint, validate, and auto-fix Markdown documentation. Checks heading consistency, generates tables of contents, validates links, verifies YAML frontmatter, and normalizes formatting.

Perfect for docs-heavy repos, static sites (Jekyll, Hugo, MkDocs), and CI pipelines where installing Node.js toolchains (markdownlint, prettier) is overkill.

## Install

```bash
# No dependencies needed — Python 3.8+ stdlib only
python md_linter.py --help

# Make it a system command
chmod +x md_linter.py
sudo cp md_linter.py /usr/local/bin/md-linter
```

## Commands

| Command | Description |
|---------|-------------|
| `check` | Lint a Markdown file for heading, whitespace, and formatting issues |
| `toc` | Generate and optionally insert a table of contents |
| `links` | Check for broken links (file-local and HTTP 200 validation) |
| `frontmatter` | Validate YAML frontmatter fields |
| `format` | Auto-fix common formatting issues (trailing spaces, heading spacing) |

## Usage

```bash
# Lint a file
python md_linter.py check README.md

# Generate a table of contents
python md_linter.py toc docs/guide.md

# Insert TOC into the file (after frontmatter)
python md_linter.py toc docs/guide.md --insert

# Check links
python md_linter.py links documentation.md

# Validate frontmatter
python md_linter.py frontmatter post.md --require title,date,tags

# Auto-format
python md_linter.py format README.md --write
```

## Features

- **Zero dependencies** — pure Python stdlib, no npm/pip installs
- **TOC generation** — builds ordered lists from `#` headings with proper nesting
- **Broken link detection** — checks local file references and HTTP links (HEAD requests)
- **Frontmatter validation** — verifies YAML frontmatter has required fields
- **Format auto-fix** — trailing whitespace removal, heading spacing, consistent list markers
- **CI-friendly** — exits with status code 1 when issues are found
- **Glob support** — lint multiple files at once

## Examples

```bash
# Lint all markdown files in a project
python md_linter.py check README.md CHANGELOG.md CONTRIBUTING.md

# Validate frontmatter on blog posts
python md_linter.py frontmatter _posts/*.md --require title,date,categories

# Generate a TOC and preview before inserting
python md_linter.py toc long-doc.md
python md_linter.py toc long-doc.md --insert

# Format-check in CI
python md_linter.py check --verbose README.md
if [ $? -ne 0 ]; then echo "Docs need fixing!"; exit 1; fi
```

## Why Markdown Linter & Fixer?

Existing Markdown linters (markdownlint-cli, prettier) require Node.js and a `node_modules` directory. In CI, Docker, or constrained environments, that's a heavy dependency for what should be a simple text parsing job. This tool is a single Python file you can audit, vendor, or curl into any environment with Python 3.8+. It handles the 80% case — TOC generation, link validation, frontmatter checks, and formatting — without any ceremony.

## Support

- File an issue on the [ClawHub registry](https://clawhub.nousresearch.com)
- MIT License — free to use, modify, and share
