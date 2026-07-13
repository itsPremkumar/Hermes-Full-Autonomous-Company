#!/usr/bin/env python
"""
REUSABLE verify template for money-engine (copy + adapt per change).

Builds from a CLEAN `git archive HEAD` checkout (not the live tree) so it proves
the COMMITTED state is green. Runs generators, rebuilds, checks links/tokens, then
self-cleans. Run: python scripts/verify-archive.py  (from the money-engine repo root)

Current streams A-M (12 generators). Keep GEN in sync with the repo when adding one.
"""
import os, re, shutil, subprocess, tempfile, sys, tarfile, io

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = tempfile.mkdtemp(prefix="hermes-verify-")
print("[setup] git-archive HEAD -> " + WORK)
PY = sys.executable

with subprocess.Popen(["git", "archive", "HEAD"], cwd=SRC, stdout=subprocess.PIPE) as p:
    tar_bytes = p.stdout.read()
with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as tf:
    tf.extractall(WORK)

res = []
def chk(label, ok, detail=""):
    res.append(ok)
    print(("[PASS] " if ok else "[FAIL] ") + label + ((" -- " + detail) if detail else ""))

# All 12 generators (A-M). Keep in sync with repo.
GEN = ["gumroad/generate.py", "fiverr/generate.py", "pod/generate.py",
       "promo/generate.py", "support/generate.py", "analytics/generate.py",
       "newsletter/generate.py", "research/intake.py", "lead/subscribe.py",
       "research/scanner.py", "service/generate.py", "fiverr/lister.py"]
for g in GEN:
    r = subprocess.run([PY, g], cwd=WORK, capture_output=True, text=True, timeout=60)
    chk(g + " runs", r.returncode == 0, r.stderr[-60:])

r1 = subprocess.run([PY, "build.py"], cwd=WORK, capture_output=True, text=True, timeout=60)
r2 = subprocess.run([PY, "gumroad/build_page.py"], cwd=WORK, capture_output=True, text=True, timeout=60)
chk("build.py + build_page.py", r1.returncode == 0 and r2.returncode == 0, (r1.stderr or r2.stderr)[-100:])

docs = os.path.join(WORK, "docs")
htmls = [os.path.join(docs, f) for f in os.listdir(docs) if f.endswith(".html")]
chk(">=10 html pages", len(htmls) >= 10, "n=" + str(len(htmls)))
chk("subscribe.html present (Stream K)", os.path.isfile(os.path.join(docs, "subscribe.html")))

missing = []
for hp in htmls:
    t = open(hp, encoding="utf-8").read()
    for href in re.findall(r'href="([^"#:]+)"', t):
        tg = os.path.normpath(os.path.join(os.path.dirname(hp), href))
        if not os.path.exists(tg):
            missing.append((os.path.basename(hp), href))
chk("all internal links resolve", not missing, "missing=" + str(missing))

leak = [os.path.basename(h) for h in htmls if "{{" in open(h, encoding="utf-8").read()]
chk("no token leak", not leak, "leak=" + str(leak))

# Stream L/M must stay de-crypto'd but Fiverr-routed
svc = open(os.path.join(WORK, "service", "generate.py"), encoding="utf-8").read()
chk("Stream L de-crypto'd", "mltl" not in svc and "stablecoin" not in svc and "MPP" not in svc)
chk("Stream L routes to Fiverr", "Fiverr" in svc)
fiv = os.path.join(WORK, "fiverr", "lister.py")
if os.path.isfile(fiv):
    fl = open(fiv, encoding="utf-8").read()
    chk("Stream M de-crypto'd", "crypto" not in fl.lower())
    chk("Stream M routes to Fiverr", "Fiverr" in fl)

# gitignore sanity
gi = open(os.path.join(WORK, ".gitignore"), encoding="utf-8").read()
chk(".gitignore ignores docs/ + scanner state", "docs/" in gi and "research/.scanner_state.json" in gi)

passed = sum(1 for x in res if x)
print("\nSUMMARY: " + str(passed) + "/" + str(len(res)) + " passed")
shutil.rmtree(WORK, ignore_errors=True)
print("[cleanup] removed " + WORK)
sys.exit(0 if passed == len(res) else 1)
