---
name: codebase-inspection
version: 1.0.0
description: Analyze codebases: lines of code, language breakdowns, file-type ratios, and complexity metrics. Zero deps (Python stdlib).
tags: ["codebase", "analysis", "metrics", "devtools", "python", "cli"]
---

# Codebase Inspector

A zero-dependency Python CLI tool that walks any directory tree and reports detailed codebase statistics — lines of code per language, blank lines, comment lines, file counts, and language distribution ratios.

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/codebase-inspection/main/codebase_inspector.py
# Or copy the file anywhere — it's self-contained.
```

## Usage

### Basic scan
```bash
python codebase_inspector.py /path/to/project
```

### JSON output (for programmatic consumption)
```bash
python codebase_inspector.py /path/to/project --json
```

### Example output
```
Codebase: /home/user/projects/my-app

Language             Files    Lines    Blank  Comments
Python                  42     3845      412       189
JavaScript              18     2104      198        76
TypeScript               7     1567      145        34
Markdown                12      845      210         0
HTML                     5      423       42         5
JSON                     8      312        0         0
CSS                      3      189       24         8
YAML                     4       78       12         3
------------------------------------------------------------------------
TOTAL                   99     9363     1043       315
```

## Features

- **Automatic language detection** — recognizes 25+ file extensions from `.py` to `.toml`
- **Smart directory skipping** — ignores `.git`, `node_modules`, `__pycache__`, `venv`, `dist`, `.next`, and other build artifacts
- **Blank line and comment counting** — identifies comment lines (starting with `#`, `//`, `/*`, etc.)
- **JSON mode** — machine-readable output for CI/CD pipelines and dashboards
- **Cross-platform** — works on Windows, macOS, Linux
- **Offline** — no network calls, no telemetry

## Commands

| Command | Description |
|---------|-------------|
| `python codebase_inspector.py <dir>` | Analyze directory and print human-readable report |
| `python codebase_inspector.py <dir> --json` | Output results as JSON |
| `python codebase_inspector.py <dir> --sort` | Sort by line count (default) |

## How it works

The tool walks the directory tree using `os.walk()`, reads each text file, and categorizes it by file extension. For every file it counts:
1. **Total lines** — all lines in the file
2. **Blank lines** — lines that are empty or contain only whitespace
3. **Comment lines** — lines starting with `#`, `//`, `/*`, `*`, or `--`

Languages are mapped from file extensions (`.py` → Python, `.js` → JavaScript, `.ts` → TypeScript, etc.). Unrecognized extensions are grouped under "Other".

## Use cases

- **Due diligence** — before refactoring, know which languages dominate
- **CI gating** — enforce file-type ratio rules in pull requests
- **Migration planning** — track language adoption over time
- **Cost estimation** — rough project size for quotes or timelines
- **Portfolio display** — generate language-breakdown badges for README

## Example: CI integration

```yaml
# .github/workflows/codebase-metrics.yml
name: Codebase Metrics
on: [push]
jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Analyze codebase
        run: |
          python codebase_inspector.py . --json > metrics.json
      - name: Check Python ratio
        run: |
          python -c "
          import json
          d = json.load(open('metrics.json'))
          py = d['stats'].get('Python', {}).get('lines', 0)
          total = d['total_lines']
          ratio = py / total * 100 if total else 0
          print(f'Python: {ratio:.1f}%')
          assert ratio > 30, 'Python ratio too low'
          "
```

## Support

Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
