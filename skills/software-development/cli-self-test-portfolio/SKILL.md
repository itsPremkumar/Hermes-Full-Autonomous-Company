---
name: cli-self-test-portfolio
version: 1.0.0
description: >-
  Add REAL, asserting `self-test` subcommands to a portfolio of existing Python CLI
  tools and make a product/portfolio verification harness pass — without changing
  existing tool behavior. Use when a user says "add a self-test to N tools",
  "make the portfolio harness pass", "each tool needs a self-test subcommand", or
  when a verify_product/verify_portfolio script reports "self-test: none found"
  across many folders. Covers argparse vs manual argv parsing, the 7-axis harness
  contract, and the non-obvious traps that make self-tests silently FAIL.
---

# cli-self-test-portfolio

Add a `self-test` subcommand (or `--self-test`/`self-test` argv guard) plus a
`_self_test()` helper to each target Python CLI, then drive the portfolio harness
to green. The hard rule: **only ADD** — never change existing command behavior.
The self-test must be **REAL**: it must exercise the tool's own core (a pure
function on temp input, or a stubbed side-effect with asserted output). NO fake
`return 0` with no assertion.

## When this fires
- "Add a self-test subcommand to these 14 tools and a `test:` line to these skills."
- A portfolio harness (`ci/verify_product.py`, `verify_portfolio.py`, etc.) reports
  `FAIL - self-test (none found)` for many folders at once.
- You are shipping a bundle of CLIs and each needs an in-process smoke test.

## Core pattern (applies to every tool)
1. Read the whole file first (some are large; use `read_file` with offset/limit, then
   re-read before overwriting — the patch tool warns if you only saw a partial view).
2. Add `def _self_test():` near the other commands. It returns `0` on pass, `1` on
   fail, and prints plain `self-test: PASS` / `self-test: FAIL` (the harness greps for
   `PASS` in stdout and checks `returncode == 0`).
3. Wire it into `main()` and register the subparser.
4. Keep every assertion meaningful — assert the actual computed result, not just that
   the function ran.

## Wiring by CLI style
### argparse with `sub = p.add_subparsers(dest="cmd", required=True)`
```python
sub.add_parser("self-test", help="Run built-in self tests")
# in main(), after parsing:
if args.command == "self-test":
    sys.exit(_self_test())
```
**PITFALL:** the harness runs `python tool.py self-test`. If `self-test` is not a
registered subparser, argparse rejects it *before* your dispatch code runs
(`error: invalid choice: 'self-test'`). Always register the subparser — don't rely on
a manual `sys.argv[1] == "self-test"` guard in an argparse tool.

### Manual `sys.argv` parsing (no argparse)
These tools check `sys.argv` by hand. Just add a guard at the top of `main()`:
```python
def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "self-test":
        sys.exit(_self_test())
    if len(sys.argv) < 3:
        ...
```

### `parse_known_args()` / dispatch-dict styles
Add a `self-test` subparser AND handle it before the dispatch table (the table may
`KeyError` on an unregistered key).

## What a REAL self-test exercises (by tool shape)
- **Pure function (validate/lint/scan/diff/parse):** call it on a tiny temp file/dict
  and assert the result.
  - json validate → build a valid + invalid doc, assert both verdicts.
  - md linter → write a file with a known defect (trailing whitespace, `#NoSpace`),
    assert `lint_file()` reports it.
  - secret scanner → write a temp file with a **fake** key, assert `scan_file()` flags
    it; assert a clean file yields zero findings.
  - codebase inspector → `analyze()` on a temp dir with a `.py` + `.md`; assert counts.
  - ascii art → `cmd_banner()/cmd_box()` with `redirect_stdout`; assert block glyphs
    (`█`) / border chars (`┌`) appear.
- **Side-effecting / network-only CLI (fetch, gif, youtube-search):**
  stub the network layer (monkeypatch the `_get`/`_fetch` helper to return a fixture)
  and assert the parsing/formatting command renders the right fields. This satisfies
  "skip the network but exercise the core". See references/harness-and-traps.md for the
  exact stub recipe.

## The 7-axis portfolio harness contract
A typical `verify_product.py` checks (see references/harness-and-traps.md for the real
source):
1. **structure** — `SKILL.md` + (a `.py` tool OR an external-tool skill marker).
2. **frontmatter** — `name`/`version`/`description` in `SKILL.md`.
3. **compiles** — `py_compile` every `.py`.
4. **self-test** — ANY of: (a) a `.py` exposes `self-test` AND it passes; (b) a
   `test_*.py`/`*_test.py` passes; (c) `SKILL.md` declares a `test:` line (external
   tool skill).
5. **security** — no hardcoded secret matching `api_key|secret|token|... = <longval>`.
6. **docs** — `SKILL.md` mentions Usage/Why/Example.
7. **deploy-ready** — `ci/ci_check.py` frontmatter check passes.

### External-tool / doc skills (no `.py`)
Append a `test:` declaration line to `SKILL.md`:
```
test: python airtable_cli.py --help   # install first: curl -O .../airtable_cli.py
```
For a doc pack with no install step, the line alone may NOT satisfy the **structure**
axis. The harness treats a folder as external when `SKILL.md` matches an install keyword
(`pip install`/`npm i`/`requirements\.txt`/`brew install`/`go install`/`cargo install`)
OR a `requirements.txt` file exists. So:
- If `SKILL.md` already has an install keyword (e.g. "pip install Pillow") → the `test:`
  line is enough.
- If it does NOT (a pure-doc skill like "prompts live in PROMPTS.md") → also add a
  `requirements.txt` marker file (even just a comment), or the structure axis FAILS.

## Non-obvious traps (caught the hard way this session)
All detailed in references/harness-and-traps.md. TL;DR:
1. **argparse ordering** — register the `self-test` subparser or argparse aborts first.
2. **Secret-scanner fixture filtering** — its `is_likely_test_fixture()` drops any line
   containing "example", "fake", "test", "placeholder", "sample", "dummy", etc. So a
   *fake* AWS key written as `aws_key = AKIAIOSFODNN7EXAMPLE` (contains "example") is
   silently ignored. Use a clearly-fake key with NO fixture keyword, e.g.
   `AKIAAB12CD34EF56GH78`, and a comment like `# token for selftest only`.
3. **Regex input collisions in your own test** — `extract_video_id()` matches an 11-char
   ID; a test string like `not-a-video` is 11 chars and falsely matches. Use a longer,
   obviously-non-ID string for the "should return None" case.
4. **Whitespace in fixtures** — if you feed `Hello  World` (double space) to a parser
   that collapses whitespace, assert the *collapsed* form, not the literal input.
5. **`self-test` printed line** — the harness greps stdout for `PASS`. Your helper MUST
   print `self-test: PASS` (or similar containing PASS); a bare `sys.exit(0)` fails the
   assertion check.
6. **Security axis vs your test fixtures** — keep fake tokens OUT of source where they
   could match the hardcoded-secret regex; prefer writing them only to a temp file at
   runtime inside `_self_test()`.

## One-shot verification habit
The repo's harness is the source of truth. After editing, run it per folder:
```bash
cd /c/one/paperclip-company && python ci/verify_product.py clawhub-skills/<folder>
```
For many folders, loop and tally PASS/FAIL; fix each FAIL by axis (read which axis
failed from the output). Do NOT claim done until `RESULT: PASS` for every target folder.

## Overlap note
`verify-untested-repo` / `verify-codebase` are the READ-ONLY counterparts (audit an
existing untested repo). Use them when you must *verify without writing*; use this skill
when you must *add* self-tests to make a harness green.
