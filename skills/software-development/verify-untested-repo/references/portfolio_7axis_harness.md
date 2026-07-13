# Portfolio 7-axis verification harness (evolution of the canonical suite)
When the repo is a *portfolio* of many small products (e.g. 31 ClawHub
skill folders under `clawhub-skills/`), one flat `test_all.py` is not enough.
Promote the canonical suite into a **per-product 7-axis harness** so it can be
run on every product folder and wired into each repo's CI.

## The 7 axes (check ALL of these per product)
1. **structure** — `SKILL.md` present AND (a `.py` tool OR an external-tool
   skill: `requirements.txt` / an install note in SKILL.md).
2. **frontmatter** — `name`/`version`/`description` in the SKILL.md YAML block.
3. **compiles** — `python -m py_compile` on every `.py`.
4. **self-test** — satisfied if ANY of:
   (a) a `.py` exposes a `self-test` subcommand that prints `PASS` and rc=0,
   (b) a `test_*.py` / `*_test.py` exists and passes,
   (c) SKILL.md declares a `test:` instruction (for external-tool skills).
5. **security** — NO hardcoded secret (`key=value` with 8+ char value). NOTE:
   do NOT flag a tool that *detects* `rm -rf`/`sudo` as a string — that is a
   false positive. Only flag real leaked credentials.
6. **docs** — SKILL.md has a Usage/Why/Example section.
7. **deploy-ready** — `ci_check.py` passes (frontmatter + tool presence); must
   HARD-FAIL (rc=1) on a missing SKILL.md, not skip.

## Reusable files to commit
- `ci/verify_product.py` — runs all 7 axes on a folder (or many folders).
  Accepts folders as argv; defaults to cwd. `sys.exit(1)` on any FAIL.
- `ci/ci_check.py` — the deploy-check (frontmatter + tool). MUST resolve the
  package from `cwd` when CI invokes it from the repo root, else it always sees
  the repo root and skips broken sub-packages. And it must rc=1 on missing
  SKILL.md (a regression where it returned 0 and let a broken package pass).
- `docs/ci-workflow-template.yml` — GitHub Actions: matrix Python 3.8/3.11,
  calls `python ci/verify_product.py .` in the `test` job, then a `deploy-check`
  job that calls `python ci/ci_check.py`. Quote step `name:` strings that
  contain `:` (YAML chokes). Copy into each repo as `.github/workflows/ci.yml`.

## Adding real self-tests to existing tools (the bulk job)
Most real tools use `argparse` with `sub = p.add_subparsers(dest="cmd", required=True)`.
Add ONE subcommand + ONE helper per tool, do NOT change existing behavior:
```python
sub.add_parser("self-test")
...
def _self_test():
    # exercise the tool's OWN core on a tiny temp input; assert; print "self-test: PASS"
    ...
    return 0 if ok else 1
# in main():
if args.cmd == "self-test":
    sys.exit(_self_test())
```
For external-tool skills (arxiv, airtable, maps, notion, polymarket, excalidraw,
ascii-video): they have SKILL.md but NO in-package `.py`. Append a `test:` line
to SKILL.md declaring the install/import proof, e.g.
`test: python -c "import arxiv; print('ok')"`. The harness axis-4(c) accepts this.
Do NOT fake `return 0` with no assertion — verify the assertion is real.

## MSYS/git-bash glob pitfall (Windows, real this session)
`ls "$TP"/hermes-verify-*` where `$TP` has a path-case mismatch
(`Local/Temp` vs `Local/Temp`) or no match ECHOES the *literal glob pattern*
or unrelated files, making you think a deleted Temp verifier still exists.
DEFINITIVE check is `find "$TP" -maxdepth 1 -name "hermes-verify-*"`.
If `find` returns ZERO, the file is gone — the shell `ls` was lying via glob.
Also: a `tempfile.mkdtemp(prefix="hermes-verify-...")` leaves a DIRECTORY, not a
file — `rm -f` won't remove it; use `rm -rf`.

## Scaling to 30+ products
1. Build `verify_product.py` + `ci_check.py` + `ci-workflow-template.yml`.
2. Run `for d in clawhub-skills/*/; do python ci/verify_product.py "$d"; done`
   to get the true pass/fail matrix (the harness EXPOSES real gaps the flat
   suite hid — e.g. 12/31 passed, 19 needed self-tests).
3. Delegate the mechanical self-test additions to a subagent (well-scoped,
   parallel), then YOU re-run the harness and push corrected repos.
4. The user's standing bar ("verify from all perspectives", "30+ production-grade,
   well-tested") is satisfied only when the harness reports ALL PASS across the
   whole portfolio — not just the few you built this turn.

## Propagating CI to 31 EXISTING repos (force-push clean-tree pattern)
When product repos ALREADY hold older `.github/workflows/ci.yml`, `.gitignore`,
`ci/ci_check.py` (from earlier pushes), a naive `git pull --rebase` + `git push`
**conflicts** on those 3 files (add/add) and a 31-repo loop times out at 60s. CURE:
- Source-of-truth is the MAIN repo; product repos are auto-generated mirrors,
  so a clean **force-push** of a fresh staged tree is correct + safe (no human
  work to lose). Force-push avoids the conflict entirely.
- Stage each folder to a temp dir, COPY the 3 infra files in, strip secrets
  (`find -iname "*moltbook_key*" -delete`, `*.key`, `*.log`), write `.gitignore`,
  `git init` + commit, then `git push --force -q <url> HEAD:main`.
- Run as `terminal(background=true, notify_on_complete=true)` — 31 force-pushes
  take ~3-4 min. Poll sparingly; rely on the completion notice.
- After: verify with `curl .../repos/itsPremkumar/<name>` (200 = live) AND a
  secret-scan of each repo's `git/trees/main?recursive=1` (assert no
  `moltbook_key` in any path). This caught a real bug: `ci_check.py` used to
  SKIP (rc=0) when no SKILL.md existed — fixed to hard-FAIL (rc=1).
- Clean up the transient pusher script (`_push_all_repos.py`) after completion.

Example batched pusher (Python, background):
```python
import os, subprocess
REPO = r"C:\one\paperclip-company"; STAGE = r"C:\one\_stage_all2"
TOK = subprocess.run(["git","credential","fill"], input=b"protocol=https\nhost=github.com\n",
    capture_output=True).stdout.decode().split("password=")[-1].split("\n")[0].strip()
os.system(f'rmdir /s /q "{STAGE}" 2>nul'); os.makedirs(STAGE, exist_ok=True)
def run(cwd, *a):
    return subprocess.run([*a], cwd=cwd, capture_output=True, text=True, timeout=60)
names = sorted(d for d in os.listdir(os.path.join(REPO,"clawhub-skills"))
            if os.path.isdir(os.path.join(REPO,"clawhub-skills",d)))
for name in names:
    d = os.path.join(STAGE, name); os.makedirs(d, exist_ok=True)
    os.system(f'xcopy "{REPO}\\clawhub-skills\\{name}" "{d}" /E /I /Q /Y >nul')
    os.makedirs(os.path.join(d,".github","workflows"), exist_ok=True)
    os.makedirs(os.path.join(d,"ci"), exist_ok=True)
    os.system(f'copy "{REPO}\\docs\\ci-workflow-template.yml" "{d}\\.github\\workflows\\ci.yml" >nul')
    os.system(f'copy "{REPO}\\ci\\ci_check.py" "{d}\\ci\\ci_check.py" >nul')
    os.system(f'copy "{REPO}\\ci\\verify_product.py" "{d}\\ci\\verify_product.py" >nul')
    for root,_,files in os.walk(d):
        for f in files:
            if "moltbook_key" in f.lower() or f.endswith(".key") or f.endswith(".log"):
                os.remove(os.path.join(root,f))
    open(os.path.join(d,".gitignore"),"w").write(".moltbook_key\n*.key\n.env\n*.log\n__pycache__/\n")
    run(d,"git","init","-q"); run(d,"git","checkout","-q","-b","main")
    run(d,"git","config","user.email","premkumar016555@gmail.com")
    run(d,"git","config","user.name","itsPremkumar")
    run(d,"git","add","-A"); run(d,"git","commit","-q","-m",f"prod: {name} + CI")
    url=f"https://{TOK}@github.com/itsPremkumar/{name}.git"
    pr = run(d,"git","push","--force","-q",url,"HEAD:main")
    print(f"PUSHED {name}" if pr.returncode==0 else f"FAIL {name}")
```
