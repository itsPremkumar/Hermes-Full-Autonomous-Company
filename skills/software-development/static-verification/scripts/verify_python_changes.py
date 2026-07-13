#!/usr/bin/env python3
"""Reusable scaffold for STATIC verification of Python edits when the program
can't be run here. Copy to a temp path (hermes-verify-*.py), extend the CHECKS
list, run it, then delete it. See skill: static-verification."""
import ast, os, sys

TARGETS = [  # (path, [required-substring-or-false-to-skip])
    (r"C:\one\Optimus_Prime\src\optimus_v17.py", []),
]
# Add caller-supplied string-presence checks here, e.g.:
CHECKS = [
    # ("BUG fixed: no stray *10.0", 'M_Nmm = torque_kgcm * 98.0665' in code and '* 98.0665 * 10.0' not in code),
]

fails = []
for path, _ in TARGETS:
    try:
        code = open(path, encoding="utf-8").read()
        ast.parse(code)
        print(f"[OK] parses: {os.path.basename(path)}")
    except SyntaxError as e:
        print(f"[FAIL] parse {path}: {e}"); fails.append(str(path)); continue
    for label, cond in CHECKS:
        ok = bool(cond)
        print(("[OK] " if ok else "[FAIL] ") + label)
        if not ok: fails.append(label)

print("\n" + ("ALL CHECKS PASSED" if not fails else f"{len(fails)} FAILURES: {fails}"))
sys.exit(1 if fails else 0)
