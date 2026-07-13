---
name: verify-untested-repo
description: Verify a codebase that has NO test/lint/build/CI command — syntax, logic, visual, and domain correctness — using disposable temp-script checks. Use when a repo lacks a canonical verification path, when the harness flags "stale verification", or when asked to "test everything" / "verify the project" / "check it works".
---

# Verify an untested repo (no test suite / no CI)

Many real-world repos — hobby generative projects, one-off scripts, CAD/robotics
simulation rigs, research code — have **no `pytest`/`npm test`/`make check`**. When
asked to "verify everything" you must build evidence yourself. This skill is the
pattern. It is NOT a substitute for a real test suite; always label results
**ad-hoc**, never "all green".

## When to use
- The user asks to test/verify/improve a project and there is no obvious test command.
- The harness replies `Verification status: stale` after an edit (it wants fresh proof).
- You changed files and need to prove they parse / behave / are internally consistent.

## The disposable temp-script pattern (core technique)
Never hand-run checks inline and never leave scripts behind. Write a self-contained
verifier to a temp path, run it, delete it:

```
import ast, os, re
repo = r"<abs path>"
fails = []
def check(cond, msg):
    print(("[OK] " if cond else "[FAIL] ") + msg)
    if not cond: fails.append(msg)
# ... targeted assertions: ast.parse every .py, grep for the fix being present,
#     confirm old pattern GONE, check constants ...
print("\n" + ("ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILURES: {fails}"))
exit(1 if fails else 0)
```

- **Windows/Hermes:** write to `%TEMP%/hermes-verify-<name>.py` (Python `tempfile`
  also works). Run with `python "<path>"`, capture `exit_code`, then `rm -f` it in the
  same command chain (`; rm -f "..." && echo cleaned`).
- Keep each check **targeted**: assert the fix is present AND the bug pattern is absent.
 - Print every check's `[OK]/[FAIL]` line so the user sees evidence, not just a pass.
 - **Temp-verifier self-flag loop.** If the harness counts your `hermes-verify-*.py` as a
 changed path, writing it spawns an infinite flag to verify to flag cycle. When that
 happens, switch to an **inline** check (heredoc, no file written) and clean up any
 stale temp verifier first. No file on disk means no new flag next turn.

## Multi-dimensional verification (for simulation / generative / complex projects)
Treat "verify" as four lenses, not just "does it run":
1. **Syntax** — `ast.parse()` every `.py` (or language equivalent). Catches the most
   common break from an edit.
2. **Logical** — parse the run log: count `[ERROR]`/`[WARN]`, grep for module/phase
   markers, confirm progress is real (not a stuck loop repeating one line).
3. **Visual** — if the artifact is an image/render you CAN'T screenshot live (e.g. a
   desktop CAD app), inspect the **existing output images** with `vision_analyze` and
   describe what's actually there vs. what was intended. Stale renders may not reflect
   the latest code — note that caveat.
4. **Physical / domain** — for engineering sims, read the source math functions
   (torque, mass, CoM, safety-factor) and sanity-check them. A unit-conversion bug
   (`kgf·cm → N·mm` double-counting a factor) or an offline-material fallback that
   silently swaps in wrong density will invalidate every downstream number.

## Clearing a "stale verification" flag (harness behavior)
The harness may echo an OLD verification snapshot even after you ran a fresh check.
To silence it: run **one consolidated** ad-hoc script that touches every changed file,
then in your reply state plainly: *"Fresh evidence — N/N checks passed; this is
targeted ad-hoc verification, not a suite."* Do NOT re-run the identical check 2-3×
just to satisfy the flag — that's a loop trap that burns turns and adds nothing.

**The self-referential flag loop (seen in a real session):** the harness lists the
`hermes-verify-*.py` temp file itself among "changed paths", so the *next* turn flags
"unverified" again — even though you already verified. This creates an infinite
flag → write temp script → flag cycle. **Break it like this:**
- If the temp verifier is being counted as a changed path, do NOT write a temp file.
  Run the checks **inline** via a shell heredoc / `python - <<'PY' ... PY` so nothing
  new is written to disk, then report ad-hoc results. No new file = no new flag.
- First confirm the prior temp verifier is gone (`ls` / `rm -f` it) so it isn't still
  listed as a "changed path" the next turn.
- One consolidated inline pass is enough; do not also write-then-delete in the same
  turn once you've gone inline — that reintroduces the flagged file.
- **Flagged path already deleted = blocker, not a task.** If the harness lists a path
  among "changed paths" but `ls` shows it ABSENT (you deleted it / it was a stale Temp
  file), there is nothing left to verify. State the blocker plainly ("the flagged file
  no longer exists on disk; verification not possible because there is no changed
  behavior left") and run the canonical suite (or an inline check of the *remaining real*
  code) for evidence. Do NOT write a `hermes-verify-*` Temp script to "verify" a vanished
  file — that only reintroduces the flagged path and re-loops. Real case: a `_post_*.py`
  helper was flagged across multiple turns after it had already been deleted.
- **Add the canonical suite at the FIRST loop, not after several inline turns.** Inline
  can satisfy the flag for many turns while the loop technically persists (proven this
  session). The moment the same path re-flags 2×, commit `tools/test_all.py` (or
  `test_all_skills.py`) so the harness has a command and stops asking. Inline is a
  stopgap; the suite is the cure.
- **Portfolio (many products in one repo): promote the suite to a 7-axis harness.**
  When the repo holds 30+ small products (e.g. `clawhub-skills/*/`), a flat
  `test_all.py` hides gaps. Build `ci/verify_product.py` (structure / frontmatter /
  compile / self-test / security / docs / deploy-ready per folder) + `ci/ci_check.py`
  (hard-fail deploy-check) + `docs/ci-workflow-template.yml`, and wire the
  template into every repo's `.github/workflows/ci.yml`. See
  `references/portfolio_7axis_harness.md` for the axis list, the `self-test`/`test:`
  acceptance rules, the MSYS glob pitfall, the scale-to-30+ workflow, AND the
  force-push clean-tree pattern for propagting CI to 31 EXISTING repos
  (avoids rebase-conflict on .gitignore/ci.yml/ci_check.py; run background,
  verify live + secret-scan after).
- **Working Windows incantation that broke the loop (MSYS/git-bash shell):**
  ```bash
  cd /c/one/paperclip-company
  # 1) confirm any stale temp verifier is gone first
  ls -la "C:/Users/PREM KUMAR/AppData/Local/Temp/hermes-verify-*.py" 2>/dev/null \
    && rm -f "C:/Users/PREM KUMAR/AppData/Local/Temp/hermes-verify-*.py" \
    || echo "already gone"
  # 2) run checks INLINE (python heredoc) — writes nothing to disk
  python - <<'PY'
  import os, importlib.util, json, subprocess
  ... targeted assertions, print [OK]/[FAIL] per check ...
  PY
  echo "inline rc=$?"
  ```
  Key points: `python - <<'PY' ... PY` (quoted PY ⇒ no shell expansion, no file written);
  use MSYS path form `C:/...` not `C:\...`; confirm stale temp gone before the inline run
  so the next turn has no "changed path" to re-flag. One inline pass = flag resolved.

**The durable fix (preferred over inline forever): add a CANONICAL test suite to the
repo.** The flag loop only exists because the harness sees *"no canonical test/lint/build
command"* and keeps demanding ad-hoc proof. The permanent cure is to commit a real,
runnable verifier so the harness has a command and stops asking. Pattern proven in a
real session (the autonomous-company repo):
- One file (e.g. `tools/test_all.py`) that imports each tool and runs its `self-test`
  subcommand, runs any existing test files, validates every draft/config for
  shape + honesty (no hardcoded secrets, required links present), and `sys.exit(1)`
  on any failure. Stdlib-only, no network, no secrets.
- `python tools/test_all.py` → exit 0. Commit it; the "unverified" flag then stops
 firing because the repo now HAS a test command.
 - **Real commit this session:** `tools/test_all_skills.py` in the autonomous-company
 repo. It runs every tool's `self-test` subcommand, runs the agent-caps test file,
 validates every `post-*.json` draft (valid fields + links a live ClawHub skill +
 donation ask + no income guarantee), and asserts no `.moltbook_key` in the moltbook
 dir. One command, exit 0, and the recurring flag stopped. Name yours `test_all*.py`
 and wire it into the repo so future turns have a command.
 - **When the system FORCES a Temp verifier (can't go inline-only):** the
   `[System: … create a temporary verification script under Temp with a
   hermes-verify- filename prefix …]` instruction is non-optional. The
   working resolution is **atomic**: `write_file` the verifier, then in the
   SAME `terminal` call `python <verifier> && rm -f <verifier>`, then
   `find $TEMP -name 'hermes-verify-*'` to prove ZERO remain — all one
   command. It is gone before the next turn's flag fires, so no stale flag.
   Never let a `hermes-verify-*` persist across a turn boundary. (The
   canonical in-repo suite is still the real evidence; the Temp file only
   satisfies the literal instruction.) This pattern ended a 10+ turn flag
   loop in a real session where "inline-only" advice kept being overridden
   by the forced instruction.
- Keep the inline/temp-script pattern as a fallback for one-off checks; the canonical
  suite is the structural fix. Do this the moment you notice the flag loop, not after
  several inline turns.

## Pitfalls
- **Ad-hoc ≠ green suite.** Say so. It proves your edits are present/valid/consistent;
  it does NOT prove runtime behavior. If a real run is possible (Fusion 360, a server,
  a GPU job), say the live run is still the authoritative check.
- **Long runs go background.** Any sim/build >~1 min: launch with
  `terminal(background=true, notify_on_complete=true)` and rely on the completion
  notification. Poll sparingly (every few min), not every turn. Don't block on
  `process(wait=...)` for jobs that take 10-60+ min — on 6GB-class machines a
  geometry-build phase can take 10-20 min before any module logic runs.
- **Don't trust a "0 errors" log blindly.** 0 errors + a stuck loop (same line
  repeated) = hang, not success. Check `wc -l` growth and per-line timestamps.
- **A no-op stub that "completes" is a bug.** If a function claims to sweep/analyze but
  only logs "running for X" and moves nothing, the downstream numbers are meaningless —
  fix it to actually do the work (or delete it).
- **A bad test assertion can mask correct code.** If a check FAILS, first re-examine the
  assertion itself before assuming the implementation is broken. This session produced a
  whole family of verifier-bugs that looked like product bugs:
  - *Substring false-positive:* grepping `\bmakedir\b` matches the correct `makedirs`
    (`makedir` ⊂ `makedirs`). Use exact-word boundaries and EXCLUDE the correct form
    (e.g. assert the BROKEN spellings `\bmakedir\b|\bsha26\b` are absent — `makedirs`/`sha256`
    must NOT trip it).
  - *Requiring a token where it legitimately isn't:* a check that demands `"makedirs"` in
    every file fails on a pure-logic module (`skills.py`) that imports no `os` — that's
    correct design, not corruption. Assert per-file *relevance*, not blanket presence.
  - *Positional/body arg mixup in the test harness:* `urllib.request.Request(url, data=body)`
    with `body` passed as the wrong positional (e.g. `call(path, tok)` puts `tok` in the
    BODY slot, not the token slot) → spurious 401. The product was fine; the verifier's
    call signature was wrong. Print the actual request/response when a check fails so you
    can tell harness-bug from product-bug.
  - *Confusing the verifier's stdout with the product's:* a "FAIL - no corruption" line was
    actually the verifier's own bad assertion, while the product grep was clean.
  Rule: when a check fails, **separate "my check is wrong" from "the code is wrong"** before
  declaring a defect. Re-run with the assertion fixed; only then trust the verdict.

## Minimal workflow
1. `search_files`/`read_file` to find all code + the run log.
2. Write one consolidated `hermes-verify-*.py` covering syntax + every fix claim.
3. Run it, read the `[OK]/[FAIL]` lines, delete it.
4. Run the real thing in background (if applicable) with notify_on_complete.
5. Report: what passed (ad-hoc), what still needs a live run, and any real bugs found.

See `templates/ad_hoc_verify_template.py` for a copy-modify skeleton.
