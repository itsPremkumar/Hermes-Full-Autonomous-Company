# Harness semantics & self-test traps (cli-self-test-portfolio)

Concrete detail behind the SKILL.md. Captured July 2026 on the
`paperclip-company/clawhub-skills` portfolio with `ci/verify_product.py`.

## The 7-axis harness (verify_product.py), distilled
The harness iterates folders and for each runs 7 checks, printing
`  PASS - <name>` / `  FAIL - <name>` and a final `RESULT: PASS|FAIL`.

- `has_self_test(fp)`: `subprocess([python, fp, "self-test"])`, pass iff
  `returncode == 0 and "PASS" in stdout`.
- self-test axis passes if ANY of:
  (a) any `.py` exposes `self-test` and it passes, OR
  (b) a `test_*.py` / `*_test.py` exists and passes, OR
  (c) `SKILL.md` matches `^(?im)test\s*:` (a declared `test:` line).
- `is_external` (structure axis) = `SKILL.md` matches
  `(?i)(pip install|npm i|requirements\.txt|brew install|go install|cargo install)`
  OR a `requirements.txt` file exists.
- `security` axis matches `(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*["']?[A-Za-z0-9_-]{8,}`.
- `deploy-ready` runs sibling `ci/ci_check.py` (frontmatter check) from the harness's
  own dir; passes if `returncode == 0`.

## Trap 1 — argparse rejects `self-test` before your guard
For argparse tools, a manual `if sys.argv[1] == "self-test"` guard does NOT help:
argparse parses known args first and dies with
`error: argument command: invalid choice: 'self-test'`. Fix: always
`sub.add_parser("self-test", ...)` and handle `args.command == "self-test"`.

## Trap 2 — secret-scanner drops fixture keywords
`secret_scanner.is_likely_test_fixture(line, matched_text)` returns True (skips the
finding) if the line contains any of: example, placeholder, test_token, fake_key,
your-key-here, your_api_key, changeme, xxxx, sample, dummy, test-, test_, mock_,
00000000-0000-0000-0000, xxxxxxxx.

So writing `aws_key = AKIAIOSFODNN7EXAMPLE` (has "example") yields ZERO findings and the
test fails with "aws key not detected". Use a key with no fixture keyword:
`AKIAAB12CD34EF56GH78`, and a comment like `# token for selftest only`.

## Trap 3 — regex input collision inside your own test
`youtube_content.extract_video_id` matches `^([A-Za-z0-9_-]{11})$`. A test string
`"not-a-video"` is exactly 11 chars → falsely matches. Use a clearly non-ID string for
the None case, e.g. `"this is definitely not a url"`.

## Trap 4 — whitespace fixtures vs collapsing parsers
`arxiv_search._parse_entry` collapses runs of whitespace (`.strip().replace("\n"," ")`
plus `re.sub(r'\s+',' ')`). Feeding `<title>Hello  World</title>` (double space) makes
the parser return `"Hello World"` (single space). Assert the *collapsed* form.

## Real network-stub recipe (gif-search style)
`_get(endpoint, params)` builds a URL and does the real HTTP call. Stub it:
```python
def _self_test():
    import io, contextlib
    def fake_get(endpoint, params):
        return {"results": [{"content_description": "funny cat",
                              "id": "abc123",
                              "media_formats": {"gif": {"url": "http://x/cat.gif"}}}]}
    global _get
    saved, _get = _get, fake_get
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cmd_search("cat", limit=1)
        out = buf.getvalue()
        assert "funny cat" in out and "abc123" in out and "http://x/cat.gif" in out
    finally:
        _get = saved
    print("self-test: PASS")
    return 0
```
This exercises the real response-parsing path with zero network.

## Pure-function recipe (md-linter style)
```python
def _self_test():
    fm, body = split_frontmatter("---\nname: x\n---\n# H\n\nbody\n")
    assert fm and "name: x" in fm and "# H" in body
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "bad.md")
        open(p, "w").write("#NoSpace   \n\nok\n")
        msgs = " ".join(i["message"] for i in lint_file(p))
        assert "Trailing whitespace" in msgs and "space after heading" in msgs
    print("self-test: PASS")
    return 0
```

## Ad-hoc verification snippet (throwaway, not a suite)
Write a temp script under %TEMP% named `hermes-verify-*.py`, run it, then delete it.
It should (a) subprocess each `tool.py self-test` and grep stdout for PASS + rc==0,
and (b) subprocess `verify_product.py <folder>` per target and tally RESULT lines.
This produces fresh evidence without committing a test suite.
