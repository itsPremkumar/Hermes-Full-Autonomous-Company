# Why the "unverified" flag loops, and how to clear it

## Symptom
After editing code, the system says "Verification status: unverified" and lists changed
paths — even after you ran a verification. Re-verifying seems to re-trigger the flag.

## Root cause (observed)
The verifier itself leaves artifacts. If you write a temp script to
`%TEMP%/hermes-verify-*.py` (or a temp dir like `%TEMP%/hermes-verify-aff-XXXX`), and it
is NOT deleted, the system counts those leftover files as "changed paths" on the next
turn → the flag never clears. Deep temp dirs can also leak (e.g. an inline test that
created `hermes-verify-aff-XXXX/_eng.py` and the rmtree didn't catch it).

## Fix / discipline
- **Preferred: verify INLINE** with a Python heredoc through the terminal tool. No file is
  written, so nothing new is flagged:
  ```bash
  python - <<'PY'
  import os, sys
  # ...assertions...
  sys.exit(0 if ok else 1)
  PY
  ```
- **If you must write a temp script:** name it `hermes-verify-*.py` under
  `%TEMP%`, run it, then `rm -f` it AND `rm -rf` any `hermes-verify-*` dirs it created.
- **Cleanup sweep** when the flag won't clear:
  ```bash
  rm -rf "$USERPROFILE/AppData/Local/Temp/hermes-verify-aff-"*
  rm -rf "$USERPROFILE/AppData/Local/Temp/hermes-verify-income"*
  rm -f  "$USERPROFILE/AppData/Local/Temp/hermes-verify-"*.py
  ```
- Only report "verified" after a clean pass with no leftover temp artifacts.

## Reporting
Always label this ad-hoc verification, not "suite green." It proves current state, not
regression safety.
