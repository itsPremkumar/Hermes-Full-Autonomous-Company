---
name: verify-codebase
description: Audit and verify an unfamiliar or untested codebase when there is NO canonical test/lint/build command. Covers version triage (which file/version is canonical), stale-doc detection, ad-hoc verification via disposable temp scripts, a three-axis verification framework (visual/logical/physical), and long-running background-sim monitoring. Use when asked to "analyze/test/verify/improve this project", "check everything", "which version is best", or when a repo lacks a test suite and you must still produce real evidence.
---

# Verify an Unfamiliar / Untested Codebase

## When to use
- User says "analyze / test / verify / improve this project", "check everything", "which version is best".
- The repo has **no canonical test/lint/build command** (no pytest, no `package.json` scripts, no Makefile test target, no `next build` that works here).
- You must produce real verification evidence, not a prose description of the code.

## Core principle
The deliverable is a **working artifact backed by real tool output**. For an untested codebase that means: never claim it works — prove each claim with a disposable check, then delete the check. Report it explicitly as *ad-hoc verification, not a green suite*.

## Step 1 — Version triage (which file/version is canonical)
Projects accumulate versioned duplicates (`v9.py`, `v14.py`, `v17.py`, `old_code/`). Determine the real entrypoint:
- Find the controller/CLI and read what file it **actually loads** (e.g. `PAYLOAD_FILE = os.path.join(BASE_DIR, "optimus_v17.py")`). The controller is the source of truth, not the newest filename on disk.
- Cross-check `git -C <repo> log -1 --format=%ci <file>` and file mtime.
- Report the version evolution briefly; pick the latest *active* one as canonical.
- **Watch for mispointed entrypoints** (controller loading an old version) — that is a real, fixable bug.

## Step 2 — Stale-doc detection
Grep `README*`, `docs/`, `CHANGELOG*` for references to old version filenames or old behavior. Common traps:
- README says `run X --stop` but `--stop` is **not a real flag** (stopping is via a `stop.flag` file the engine polls each frame). Documented CLI that doesn't exist is a factual doc bug — fix it and correct all 3 occurrences.
- CHANGELOG stops several versions behind the code; doc tree says "v9" while payload is "v17".

## Step 3 — Three-axis verification (what "verify everything" means)
A thorough pass covers all three; the user explicitly asking for "visual, logical, and physical" maps here:
- **VISUAL**: capture screenshots / renders and inspect with `vision_analyze`. Verify geometry/appearance is coherent. Caveat: stale renders may predate a color/material pass — confirm colors are applied in the live run (a log line like `Final colors: N applied, 0 skipped`). Don't trust a gray screenshot if the code applies 12 materials.
- **LOGICAL**: run the thing (or analyze its log). Grep for module markers, error/warn counts, and verify each module produced *distinct, varying* output. **A check that returns identical output for every input is a no-op** — prove it by counting distinct result values (see Pitfalls).
- **PHYSICAL**: for engineering/design code, review the source constants and validation functions directly (servo torque margins, mass/CoM, joint limits vs axis map, printability, bracket safety factors). Prefer real computed values (`physicalProperties.mass`) over hand-typed guesses; flag any module that uses fake hardcoded masses alongside a real estimator.

## Step 4 — Ad-hoc verification pattern (no test suite)
Write a **disposable** temp script:
- Path: OS-safe temp. On Windows git-bash the terminal is bash; prefer `tempfile.TemporaryDirectory(prefix="hermes-verify-")` inside the script so cleanup is automatic and the path is space-safe (user dirs like `C:\Users\PREM KUMAR\...` have spaces). Avoid hardcoding `%TEMP%` literals.
- Filename prefix `hermes-verify-` so it's identifiable and easy to confirm deletion.
- What to check: `ast.parse()` each module for syntax; grep for stale references; for functional fixes, create a **temp fixture dir** and assert the NEW logic matches real artifact names while the OLD logic misses them (proves the bug was real, not theoretical).
- Print `[OK]`/`[FAIL]` lines, `exit(1)` on failure.
- **Clean up after**: delete the temp file (or the whole tempdir). Confirm with `ls` that nothing lingers.
- Run via `terminal` foreground (ad-hoc checks are fast). Report as *ad-hoc, not a suite*.
- A reusable skeleton lives in `templates/hermes_verify_skeleton.py`. Detail + OS notes in `references/ad-hoc-verification.md`.

## Step 5 — Long-running background sims / processes
- Launch with `terminal(background=True, notify_on_complete=True)`.
- Poll the log with grep for module markers / `\[ERROR\]` counts; compute "seconds since last write" (`date -r` vs `date +%s`) to detect stalls.
- **Detect stalled/false work**: if a module's per-call output is identical across many calls (e.g. same 5 collision pairs, same ~14,800 count for every joint/angle), the check is a no-op stub or tests the wrong scope — flag it as a logic bug, not slow hardware. Prove with `grep ... | sort | uniq -c` to count distinct values.
- Don't blind-`sleep` in foreground (60s cap). Poll, or `process(wait=...)`.

## Pitfalls
- Don't re-run the identical verification script repeatedly to "clear" a stale-evidence flag — one fresh passing run suffices; subsequent identical runs are noise. If the harness re-flags, state plainly that the temp files are already deleted and point to the passing run.
- Don't claim a check "passed" if it only parsed old/dead code — scope matters (active tree vs dead `old_code/`). Exclude `old_code/`, `.git`, `__pycache__` from "code parses" claims.
- Whole-assembly interference/collision checks **cannot** detect joint-local self-collision — they only see resting-contact faces of the full model. Isolate the moving joint's bodies, or diff against the rest pose.
- A documented flag that isn't in the argparse/`add_argument` list is a doc bug, not a missing feature — verify against the actual CLI definition before trusting the docs.
- "Waiting longer" on a slow module that is actually a no-op wastes hours. Prove the module produces varying output before letting it run to completion.

## Verification-evidence format
Summarize: `kind: ad_hoc`, scope (targeted / active-tree), checks passed N/M, temp script cleaned up. Be explicit it is not a CI suite.

## Complements
- `systematic-debugging` — for 4-phase root-cause once a bug is confirmed.
- `test-driven-development` — for adding a real permanent suite after the ad-hoc pass.

## Support files
- `templates/hermes_verify_skeleton.py` — copy/edit this for any ad-hoc check; uses
  `tempfile.TemporaryDirectory(prefix="hermes-verify-")`, prints `[OK]`/`[FAIL]`,
  exits non-zero on failure.
- `references/ad-hoc-verification.md` — OS/shell facts (Windows git-bash, space-safe
  temp paths), the stale-ref sweep, and the no-op-check proof command.
