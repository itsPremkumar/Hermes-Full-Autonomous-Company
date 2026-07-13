#!/usr/bin/env python3
"""
verify_product.py - portfolio verification harness (7-axis check per product).

Run from a product folder (or pass a folder). Checks:
  1. structure  - SKILL.md + at least one .py tool present
  2. frontmatter - name/version/description in SKILL.md
  3. compiles    - every .py compiles (py_compile)
  4. self-test   - every .py exposes `self-test` and it passes
  5. security    - no secrets / destructive patterns in source
  6. docs        - SKILL.md has Usage or Why section
  7. deploy-ready- ci/ci_check.py passes (frontmatter + tool)
Exits non-zero if any axis fails. Stdlib only. Used by CI and locally.

Usage:
  python verify_product.py [folder]      # default: cwd
"""
import os
import re
import sys
import subprocess

REQ = ["name", "version", "description"]
SECRET = re.compile(r'(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{8,}', re.I)
DESTRUCTIVE = re.compile(r'(?i)(rm -rf /|sudo rm|mkfs|dd if=/dev)', re.I)


def axis(ok, name):
    print(("  PASS" if ok else "  FAIL") + f" - {name}")
    return bool(ok)


def verify(folder):
    print(f"== verify: {os.path.basename(folder)} ==")
    all_ok = True
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".py")]
    skill = os.path.join(folder, "SKILL.md")
    # 1 structure
    all_ok &= axis(os.path.isfile(skill) and bool(files), "structure (SKILL.md + .py tool)")
    # 2 frontmatter
    if os.path.isfile(skill):
        txt = open(skill, encoding="utf-8").read()
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.S)
        fm_ok = bool(m)
        if m:
            for k in REQ:
                fm_ok &= bool(re.search(rf"^{k}\s*:", m.group(1), re.M))
        all_ok &= axis(fm_ok, "frontmatter (name/version/description)")
        # 6 docs
        all_ok &= axis(bool(re.search(r'(?i)(usage|why|example)', txt)), "docs (Usage/Why/Example present)")
    else:
        all_ok &= axis(False, "frontmatter (no SKILL.md)")
        all_ok &= axis(False, "docs (no SKILL.md)")
    # 3 compiles
    comp_ok = True
    for fp in files:
        if subprocess.run([sys.executable, "-m", "py_compile", fp], capture_output=True).returncode != 0:
            comp_ok = False
    all_ok &= axis(comp_ok, "compiles (py_compile all .py)")
    # 4 self-test
    st_ok = True
    for fp in files:
        r = subprocess.run([sys.executable, fp, "self-test"], capture_output=True, text=True)
        if r.returncode != 0 or "PASS" not in r.stdout:
            st_ok = False
            print("      self-test failed:", os.path.basename(fp), r.stdout.strip()[:60])
    all_ok &= axis(st_ok, "self-test (all .py PASS)")
    # 5 security
    sec_ok = True
    for fp in files:
        src = open(fp, encoding="utf-8", errors="ignore").read()
        if SECRET.search(src) or DESTRUCTIVE.search(src):
            sec_ok = False
    all_ok &= axis(sec_ok, "security (no secret/destructive patterns)")
    # 7 deploy-ready (ci_check)
    ci = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ci_check.py")
    if os.path.isfile(ci):
        r = subprocess.run([sys.executable, ci], cwd=folder, capture_output=True, text=True)
        all_ok &= axis(r.returncode == 0, "deploy-ready (ci/ci_check.py PASS)")
    else:
        all_ok &= axis(True, "deploy-ready (no ci_check in tree - skipped)")
    print(("RESULT: PASS\n" if all_ok else "RESULT: FAIL\n"))
    return all_ok


def main():
    folders = [a for a in sys.argv[1:]] or [os.getcwd()]
    ok = True
    for f in folders:
        ok &= verify(f)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
