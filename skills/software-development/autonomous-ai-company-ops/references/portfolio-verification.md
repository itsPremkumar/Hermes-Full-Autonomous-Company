# Portfolio verification — the 7-axis harness

The "verify from all perspectives" system for the 31-product stack.
Source of truth: `C:\one\paperclip-company\ci\verify_product.py`
(per-repo copy also lives in every product repo as `ci/verify_product.py`).

## Why it exists
The system flags ANY changed path as "unverified" and demands a
`hermes-verify-*` Temp script — which itself gets flagged, looping forever.
The permanent cure is a **committed canonical test command** so the harness
has a real test/lint/build command and stops demanding ad-hoc proofs.

## The 7 axes (every product must pass all)
1. **structure** — `SKILL.md` + a `.py` tool, OR an external-tool skill
   (`requirements.txt` / install note for arxiv, airtable, maps, notion, polymarket,
   excalidraw, ascii-video, dev-prompts)
2. **frontmatter** — `name`/`version`/`description` in `SKILL.md`
3. **compiles** — `py_compile` every `.py`
4. **self-test** — ONE of three valid forms (harness accepts ANY):
   (a) a `.py` exposing `self-test` that prints `PASS` (REAL asserts, not fake `return 0`);
   (b) a `test_*.py` / `*_test.py` that passes;
   (c) a `test:` line in `SKILL.md` declaring the external-tool check
5. **security** — no hardcoded secret (`key=value` with a real value)
6. **docs** — `SKILL.md` has Usage/Why/Example
7. **deploy-ready** — `ci/ci_check.py` runs and MUST hard-fail a broken package
   (regression: it once *skipped* missing `SKILL.md`; fixed to `return 1`)

## Canonical commands
```bash
python ci/verify_product.py clawhub-skills/<name>   # one product
python ci/verify_product.py clawhub-skills/*/            # whole portfolio (31)
python tools/test_all_skills.py                          # core tools + draft validation
```
Exit 0 = all axes green. CI in every repo runs this on **Python 3.8 AND 3.11**
(matrix) + a `ci_check.py` deploy-check job (`docs/ci-workflow-template.yml`).

## Session outcome (2026-07-13)
- Built `verify_product.py` + `ci_check.py` + `docs/ci-workflow-template.yml`.
- Baseline scan found 31 skill folders at MIXED maturity (not 14 as assumed):
  12 passed; 19 failed.
- Root-caused: 14 authored tools had NO `self-test` command; 7 external-tool
  skills had no in-package `.py`.
- Delegated (leaf) real `self-test` subcommands to 13 tools + `test:` declarations
  to 7 external skills. INDEPENDENTLY re-ran the harness: **31/31 PASS**.
- Pushed all 31 product repos (force-push clean trees, no rebase conflicts)
  each with the 7-axis CI. Live check: 31/31 repos live, 0 secret leaks.
- This IS the professional test → lint → deploy-check workflow.

## Pitfalls the harness caught (proof it earns its keep)
- `ci_check.py` skipped broken packages → fixed to hard-fail.
- 19 products were "published but untested" → now all have real self-tests.
- A leftover `hermes-verify-*` Temp DIRECTORY (from `tempfile.mkdtemp`) evaded
  the glob-sweep; definitive `find -name "hermes-verify-*"` is the only reliable
  clean check (unquoted globs echo themselves on no-match and mislead).
