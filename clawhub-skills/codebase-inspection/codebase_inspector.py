#!/usr/bin/env python3
"""codebase_inspector.py — Analyze a codebase directory for LOC, languages, ratios.

Usage:
  python codebase_inspector.py <directory> [--json] [--sort]

Stdlib only. No external dependencies.
"""
import os, sys, json
from collections import defaultdict
from pathlib import Path

EXT_LANG = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".jsx": "JavaScript", ".go": "Go", ".rs": "Rust", ".java": "Java",
    ".rb": "Ruby", ".php": "PHP", ".c": "C", ".h": "C", ".cpp": "C++",
    ".hpp": "C++", ".cs": "C#", ".swift": "Swift", ".kt": "Kotlin",
    ".sh": "Shell", ".bash": "Shell", ".md": "Markdown",
    ".json": "JSON", ".yaml": "YAML", ".yml": "YAML", ".toml": "TOML",
    ".html": "HTML", ".css": "CSS", ".sql": "SQL",
}
IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".next", "target", ".cache"}

def analyze(path):
    stats = defaultdict(lambda: {"files": 0, "lines": 0, "blank_lines": 0, "comment_lines": 0})
    total_files = total_lines = 0
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for fn in files:
            if fn.startswith(".") or fn in {".gitignore", ".DS_Store", "package-lock.json", "yarn.lock"}:
                continue
            fp = Path(root, fn)
            ext = fp.suffix.lower()
            lang = EXT_LANG.get(ext, "Other")
            try:
                text = fp.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            lines = text.splitlines()
            nlines = len(lines)
            blanks = sum(1 for l in lines if l.strip() == "")
            comments = sum(1 for l in lines if l.strip().startswith(("#", "//", "/*", "*", "--")))
            stats[lang]["files"] += 1
            stats[lang]["lines"] += nlines
            stats[lang]["blank_lines"] += blanks
            stats[lang]["comment_lines"] += comments
            total_files += 1
            total_lines += nlines
    return {"stats": dict(stats), "total_files": total_files, "total_lines": total_lines}

def print_report(result):
    items = sorted(result["stats"].items(), key=lambda x: x[1]["lines"], reverse=True)
    print(f"{'Language':<20} {'Files':>8} {'Lines':>8} {'Blank':>8} {'Comments':>8}")
    print("-" * 60)
    for lang, s in items:
        print(f"{lang:<20} {s['files']:>8} {s['lines']:>8} {s['blank_lines']:>8} {s['comment_lines']:>8}")
    print("-" * 60)
    print(f"{'TOTAL':<20} {result['total_files']:>8} {result['total_lines']:>8}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__.strip())
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.isdir(path):
        print(f"Error: {path} is not a directory", file=sys.stderr)
        sys.exit(1)
    result = analyze(os.path.abspath(path))
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
    else:
        print(f"Codebase: {os.path.abspath(path)}")
        print_report(result)
