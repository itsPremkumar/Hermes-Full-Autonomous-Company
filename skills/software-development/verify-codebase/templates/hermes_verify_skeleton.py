#!/usr/bin/env python3
"""Reusable skeleton for ad-hoc verification of an untested codebase.

Drop in a tempfile.TemporaryDirectory(prefix="hermes-verify-") so the OS gives a
space-safe path (user dirs like C:\\Users\\PREM KUMAR have spaces) and cleanup is
automatic. Edit REPO + the check() calls. Run: python <this_file>; exit 1 on fail.
"""
import ast, os, re, sys, tempfile
from pathlib import Path

REPO = r"C:\path\to\repo"          # <-- set
ACTIVE_SRC = ("a.py", "b.py")      # <-- set: files that must parse
STALE_PAT = re.compile(r"old_v9|run_x --stop|Engine v9")  # <-- set

fails = []
def check(cond, msg):
    print(("[OK] " if cond else "[FAIL] ") + msg)
    (fails.append(msg) if not cond else None)

# 1. syntax
for f in ACTIVE_SRC:
    p = os.path.join(REPO, f)
    try:
        ast.parse(open(p, encoding="utf-8").read()); check(True, f"parses: {f}")
    except SyntaxError as e:
        check(False, f"parses: {f} -> {e}")

# 2. functional fix proof (example: version-agnostic glob)
with tempfile.TemporaryDirectory(prefix="hermes-verify-") as d:
    vd = Path(d)
    (vd/"BOM_v17_20260101_000000.csv").write_text("x")
    (vd/"ASSEMBLY_GUIDE_v17_20260101_000000.txt").write_text("x")
    new_glob_ok = len(list(vd.glob("BOM_v*_*.csv"))) == 1
    old_glob_ok = len(list(vd.glob("BOM_v14_*.csv"))) == 1   # expect False -> proves bug
    check(new_glob_ok, "NEW glob matches real v17 artifacts")
    check(not old_glob_ok, "OLD v14 glob MISSED real v17 artifacts (bug was real)")

# 3. stale-ref sweep over active tree only
hits = []
for root, dirs, files in os.walk(REPO):
    if any(x in root for x in (".git", "old_code", "__pycache__")):
        continue
    for fn in files:
        if fn.endswith((".md", ".html", ".py", ".json")):
            for i, line in enumerate(open(os.path.join(root, fn), encoding="utf-8", errors="replace"), 1):
                if STALE_PAT.search(line):
                    hits.append(f"{os.path.relpath(os.path.join(root, fn), REPO)}:{i}")
check(not hits, f"no stale refs in active tree (found {len(hits)}: {hits[:5]})")

print("\n" + ("ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILURES"))
sys.exit(1 if fails else 0)
# cleanup: if run inside TemporaryDirectory, the dir auto-removes on exit.
# If you wrote the script itself to %TEMP%, `rm -f` it after running.
