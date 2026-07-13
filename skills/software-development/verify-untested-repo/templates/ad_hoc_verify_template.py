import ast, os, re, sys

# Copy-modify skeleton for ad-hoc verification of a repo with no test suite.
# Write to %TEMP%/hermes-verify-<name>.py, run `python <path>`, then `rm -f` it.
# Every check must assert BOTH: the fix is present AND the bad pattern is gone.

REPO = r"C:\path\to\repo"          # <-- set this
fails = []

def check(cond, msg):
    print(("[OK] " if cond else "[FAIL] ") + msg)
    if not cond:
        fails.append(msg)

# 1) SYNTAX: parse every .py under src/
for root, _, files in os.walk(os.path.join(REPO, "src")):
    if ".git" in root or "old_code" in root:
        continue
    for fn in files:
        if fn.endswith(".py"):
            p = os.path.join(root, fn)
            try:
                ast.parse(open(p, encoding="utf-8").read())
            except SyntaxError as e:
                check(False, f"{fn} parse: {e}")

# 2) TARGETED: assert a fix exists AND the bug pattern is gone (edit these)
code = open(os.path.join(REPO, "src", "main.py"), encoding="utf-8").read()
check("NEW_PATTERN_MARKER" in code,            "fix present: <describe>")
check("OLD_BUGGY_PATTERN" not in code,        "bug pattern removed: <describe>")

# 3) CONSISTENCY: e.g. no stale version refs anywhere in active tree
stale = re.compile(r"old_thing_v9|run --stop")
hits = []
for root, _, files in os.walk(REPO):
    if any(x in root for x in (".git", "old_code")):
        continue
    for fn in files:
        if fn.endswith((".md", ".py", ".html")):
            for i, line in enumerate(open(os.path.join(root, fn), encoding="utf-8", errors="replace"), 1):
                if stale.search(line):
                    hits.append(f"{fn}:{i}")
check(not hits, f"no stale refs (found {len(hits)}: {hits[:5]})")

print("\n" + ("ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILURES: {fails}"))
# NOTE: this is targeted AD-HOC verification, not a green suite.
sys.exit(1 if fails else 0)
