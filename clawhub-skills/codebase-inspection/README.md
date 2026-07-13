# Codebase Inspector v2 🚀

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)]()
![Lines](https://img.shields.io/badge/codebase-20K%20lines%20%E2%80%A2%205%20langs-brightgreen)

**Analyze any codebase: lines of code, language breakdowns, file-type ratios, complexity metrics.**  
Zero dependencies (Python stdlib only). Works on Windows, macOS, Linux.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Language Breakdown** | 40+ extensions → 30+ languages with file/line/blank/comment/code counts |
| 🎨 **HTML Reports** | Full-color visual report with bar charts + summary cards |
| 📈 **Trend Tracking** | `--snapshot` + `--trend` to watch your codebase grow over time |
| 🔍 **Git-aware Diff** | `--diff <dir>` — compare branches, checkouts, or releases |
| 🏷️ **SVG Badge** | `--badge` generates a shields.io badge URL for README |
| 📋 **CSV Export** | `--csv` for spreadsheets and dashboards |
| 📂 **File-level Detail** | Top 20 largest files with relative path + language |
| ⚙️ **Exclusion Patterns** | `--exclude "target,.build"` to skip custom dirs |
| 🧪 **Self-test** | `codebase_inspector.py self-test` — 13 built-in checks |

## Quick Start

```bash
# Download (no pip needed)
curl -O https://raw.githubusercontent.com/itsPremkumar/codebase-inspection/main/codebase_inspector.py

# Run
python codebase_inspector.py /path/to/project
python codebase_inspector.py /path/to/project --html report.html
python codebase_inspector.py ./branch-a --diff ./branch-b
python codebase_inspector.py self-test
```

## Sample Output

```
Language             Files    Lines    Blank  Comments    Code
Python                  42     3845      412       189    3244
JavaScript              18     2104      198        76    1830
TypeScript               7     1567      145        34    1388
Markdown                12      845      210         0     635
HTML                     5      423       42         5     376
------------------------------------------------------------------------
TOTAL                   84     8784      807       304    7673
```

## Why Codebase Inspector?

- **CI-ready** — `--json` for pipelines, `--html` for visual reports, `--diff` for PR analysis
- **Zero deps** — works in any Python environment, no `pip install` needed
- **Privacy-first** — fully offline, no telemetry, no uploads
- **Cross-platform** — same output on Windows, macOS, Linux

---

📦 Also available on [ClawHub](https://clawhub.ai/skills/skills/codebase-inspection)  
⭐ Star on [GitHub](https://github.com/itsPremkumar/codebase-inspection)  
☕ [Buy Me a Coffee](https://buymeacoffee.com/itsPremkumar)
