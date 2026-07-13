---
name: codebase-inspection
version: 2.0.0
description: Advanced codebase analysis with HTML reports, git-aware diffs, trend tracking, SVG badges, CSV export, and CI/CD integration. Zero deps (Python stdlib).
tags: ["codebase", "analysis", "metrics", "devtools", "python", "cli", "ci", "reports"]
---

# Codebase Inspector v2 🚀

A zero-dependency Python CLI that walks any directory tree and delivers **production-grade codebase intelligence** — language breakdowns, line counts, complexity metrics, visual HTML reports, historical trend tracking, and CI-ready output formats.

## 🆕 What's New in v2

| Feature | Description |
|---------|-------------|
| 📊 **HTML Reports** | Full-color bar charts, summary cards, top-files table |
| 📈 **Trend Tracking** | `--snapshot` + `--trend` to watch your codebase grow over time |
| 🔍 **Git-aware Diff** | `--diff <dir>` compare two branches/checkouts |
| 🏷️ **SVG Badge** | `--badge` generates a shields.io badge URL for your README |
| 📋 **CSV Export** | `--csv` for spreadsheet import |
| 📂 **File-level Detail** | Top 20 largest files with location + language |
| ⚙️ **Exclusion Patterns** | `--exclude "target,.build"` skip custom dirs |
| 🧪 **Built-in Self-test** | `self-test` subcommand with 13 checks |

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/codebase-inspection/main/codebase_inspector.py

# Or copy the file anywhere — it's self-contained.
```

## Commands

| Command | Description |
|---------|-------------|
| `python codebase_inspector.py <dir>` | Analyze and print human-readable report |
| `python codebase_inspector.py <dir> --json` | JSON output for pipelines |
| `python codebase_inspector.py <dir> --html report.html` | Generate visual HTML report |
| `python codebase_inspector.py <dir> --csv` | CSV for spreadsheet import |
| `python codebase_inspector.py <dir> --badge` | SVG badge URL for README |
| `python codebase_inspector.py <dir> --snapshot` | Save as trend data point |
| `python codebase_inspector.py <dir> --trend` | Show historical trends |
| `python codebase_inspector.py <dir> --diff <dir2>` | Compare two codebases |
| `python codebase_inspector.py <dir> --exclude "dir1,dir2"` | Skip custom directories |
| `python codebase_inspector.py self-test` | Run built-in tests (13 checks) |

## Example Output

### Text Report
```
Codebase: /home/user/projects/my-app

Language             Files    Lines    Blank  Comments    Code
Python                  42     3845      412       189    3244
JavaScript              18     2104      198        76    1830
TypeScript               7     1567      145        34    1388
Markdown                12      845      210         0     635
HTML                     5      423       42         5     376
JSON                     8      312        0         0     312
CSS                      3      189       24         8     157
YAML                     4       78       12         3      63
------------------------------------------------------------------------
TOTAL                   99     9363     1043       315    8005

Avg lines/file: 94.6
Comment density: 3.4%

Top 10 largest files:
   1. src/app.py (245 lines, Python)
   2. src/components/Header.tsx (189 lines, TypeScript)
```

### HTML Report
```
python codebase_inspector.py /path/to/project --html report.html
→ HTML report: /cwd/report.html
```
The HTML report includes: 6 summary cards (Files, Lines, Avg L/file, Comments%, Code Lines, Blank Lines), a color-coded language breakdown table with visual bars, and a top-10 largest files table.

### Trend Tracking
```bash
# First run (baseline)
python codebase_inspector.py . --snapshot

# After some development
python codebase_inspector.py . --snapshot

# View the trend
python codebase_inspector.py . --trend
```

### Diff Two Checkouts
```bash
python codebase_inspector.py ./branch-a --diff ./branch-b
```

## Features

- **Automatic language detection** — 40+ extensions mapped to 30+ languages
- **Smart directory skipping** — `.git`, `node_modules`, `__pycache__`, `venv`, `dist`, `.next`, `target`, `.idea` + custom via `--exclude`
- **Blank line and comment counting** — identifies comment prefixes: `#`, `//`, `/*`, `--`, `;`, `%` and others
- **HTML visual report** — bar charts, summary statistics, mobile-friendly
- **Historical trend tracking** — snapshot-based, inspect codebase growth over time
- **Codebase diffing** — compare two directories for migration/refactor analysis
- **SVG badge** — copy-paste a shields.io badge into your README
- **CSV export** — import into Google Sheets or Excel
- **JSON mode** — machine-readable for CI/CD pipelines and dashboards
- **Cross-platform** — Windows, macOS, Linux
- **Offline** — no network calls, no telemetry
- **13 built-in self-tests** — verify integrity with `self-test`

## CI Integration

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
      - name: Generate HTML report
        run: |
          python codebase_inspector.py . --html codebase-report.html
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: codebase-report
          path: codebase-report.html
```

## Use Cases

- **Due diligence** — before refactoring, know which languages dominate
- **CI gating** — enforce file-type ratio rules in pull requests
- **Migration planning** — track language adoption over time with `--trend`
- **Cost estimation** — rough project size for quotes or timelines
- **Portfolio display** — generate language-breakdown badges for README
- **Code review** — `--diff` to see what a PR branch added/removed

## Support

Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/codebase-inspection)
