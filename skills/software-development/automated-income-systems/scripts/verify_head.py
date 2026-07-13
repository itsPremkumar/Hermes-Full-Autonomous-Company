#!/usr/bin/env python
# scripts/verify_head.py — reusable ad-hoc verification harness for money-engine.
# Builds from a CLEAN `git archive` of HEAD (not the live tree), so it proves the
# COMMITTED state is green and catches untracked/gitignored-file bugs.
# Usage: python verify_head.py   (run from the money-engine repo root)
# Self-contained: extracts HEAD to a temp dir, runs all generators + build,
# asserts structure, then rmtree. Reports PASS/FAIL per check as AD-HOC.
import os, re, shutil, subprocess, tempfile, sys, tarfile, io

ROOT = os.path.dirname(os.path.abspath(__file__))
# NOTE: this script lives in the skill dir, not the repo. The repo root is passed
# as arg[1] or cwd. For repo-local use, place a copy in the repo and set ROOT=cwd.
REPO = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
WORK = tempfile.mkdtemp(prefix="hermes-verify-")
print("[setup] git-archive HEAD -> " + WORK)
PY = sys.executable

with subprocess.Popen(["git", "archive", "HEAD"], cwd=REPO, stdout=subprocess.PIPE) as p:
    tar_bytes = p.stdout.read()
with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as tf:
    tf.extractall(WORK)

res = []
def chk(label, ok, detail=""):
    res.append(ok)
    line = "[PASS] " if ok else "[FAIL] "
    line += label + ((" -- " + detail) if detail else "")
    print(line)

chk("build.py tracked in HEAD", os.path.isfile(os.path.join(WORK, "build.py")))
gens = ["gumroad/generate.py", "fiverr/generate.py", "pod/generate.py",
        "promo/generate.py", "support/generate.py", "analytics/generate.py"]
for g in gens:
    r = subprocess.run([PY, g], cwd=WORK, capture_output=True, text=True, timeout=60)
    chk(g + " runs", r.returncode == 0, r.stderr[-80:])
r1 = subprocess.run([PY, "build.py"], cwd=WORK, capture_output=True, text=True, timeout=60)
r2 = subprocess.run([PY, "gumroad/build_page.py"], cwd=WORK, capture_output=True, text=True, timeout=60)
chk("build.py + build_page.py", r1.returncode == 0 and r2.returncode == 0,
     (r1.stderr or r2.stderr)[-100:])
docs = os.path.join(WORK, "docs")
htmls = [os.path.join(docs, f) for f in os.listdir(docs) if f.endswith(".html")]
chk(">=8 html pages", len(htmls) >= 8, "n=" + str(len(htmls)))
chk("support.html self-generated", os.path.isfile(os.path.join(docs, "support.html")))
idx = open(os.path.join(docs, "index.html"), encoding="utf-8").read()
chk("index links support.html", "support.html" in idx)
missing = []
for hp in htmls:
    t = open(hp, encoding="utf-8").read()
    for href in re.findall(r'href="([^"#:]+)"', t):
        tg = os.path.normpath(os.path.join(os.path.dirname(hp), href))
        if not os.path.exists(tg):
            missing.append((os.path.basename(hp), href))
chk("all internal links resolve", not missing, "missing=" + str(missing))
leak = [os.path.basename(h) for h in htmls if "{{" in open(h, encoding="utf-8").read()]
chk("no affiliate token leak", not leak, "leak=" + str(leak))
an = open(os.path.join(WORK, "content", "_analytics.md"), encoding="utf-8").read()
chk("analytics flags empty amazon_tag", "amazon_tag" in an)

passed = sum(1 for x in res if x)
print("\nSUMMARY: " + str(passed) + "/" + str(len(res)) + " passed (AD-HOC)")
shutil.rmtree(WORK, ignore_errors=True)
print("[cleanup] removed " + WORK)
sys.exit(0 if passed == len(res) else 1)
