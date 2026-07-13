# Ad-hoc verification recipe (auto-income-system)

The session harness enforced real verification after each code change. Use this
pattern; never claim "done" without it.

## Steps
1. Write a temp script in `%TEMP%` named `hermes-verify-<topic>.py`.
2. COPY the repo to a temp dir (exclude `.git` and the built `docs/`):
   ```python
   for root, dirs, files in os.walk(SRC):
       if ".git" in dirs: dirs.remove(".git")
       if "docs" in dirs and os.path.abspath(root)==os.path.abspath(SRC):
           dirs.remove("docs")
       for fn in files:
           copy to WORK/relpath
   ```
3. Replicate bash steps DIRECTLY in Python — do NOT `subprocess.run(["bash", ...])`.
   `bash` is NOT on PATH in the WSL/relay sandbox and fails with
   "CreateProcessCommon: execvpe(/bin/bash) failed". So instead of calling
   `autorun.sh`, run its steps inline:
   `shutil.rmtree(docs, ignore_errors=True); subprocess.run([PY,"build.py"]);
    subprocess.run([PY,"gumroad/build_page.py"])`.
4. WIPE `docs/` between builds when testing stale-artifact removal — the real
   `autorun.sh` does `rm -rf docs` first. A re-build WITHOUT the wipe will
   wrongly leave deleted-source `.html` files (test-harness artifact, not a
   real bug). Prove the wipe removes them.
5. Assertions to make: build scripts return code 0; `docs/` has >=N html
   pages; every `href="..."` internal link resolves on disk; no `{{` token
   leaks into html; calculators/products present; affiliate tag applies when set.
6. `shutil.rmtree(WORK, ignore_errors=True)` at the end. Report as ad-hoc
   verification, explicitly NOT a committed suite green.

## Why temp-copy + wipe
The live workspace is the source of truth and must stay untouched by tests.
The wipe replicates production `autorun.sh`, so the test exercises the exact
deploy path — this caught a corrupted `build.py`, stale html, and an
unexpanded `{{FIVERR}}` token in one session.
