# Ad-hoc verification checklist (automated-content-site)

Run this BEFORE claiming the engine works. Use a temp copy so the live `content/`
and `config.json` are never touched.

## Method
1. Write to `%LOCALAPPDATA%\Temp\hermes-verify-<name>.py` (OS-safe tempfile dir).
2. `shutil.copytree` the project (skip `public/` and `.git`) into a `tempfile.mkdtemp(prefix="hermes-verify-")`.
3. Assert the behaviors below, print PASS/FAIL per check, `sys.exit(1)` if any fail.
4. `shutil.rmtree(WORK)` at the end (cleanup is mandatory).
5. Report as AD-HOC verification, not "suite green".

## Checks that caught real bugs in v1
- `build.py` runs with **stdlib only** (no pip install).
- All outputs exist: `index.html`, per-article `.html`, `sitemap.xml`, `feed.xml`, `disclosure.html`.
- Frontmatter `slug: "best-x"` parses to `best-x` with NO quotes (the doubled-quote
  bug produced `"best-x".html` → `OSError [Errno 22] Invalid argument`).
- Affiliate expansion WITH tag: `{{AMAZON:Product}}` →
  `amazon.com/s?k=...&tag=<yourtag>` (valid URL, no raw `{{AMAZON}}` left).
- Affiliate expansion WITH EMPTY tag: still renders a valid clickable
  `amazon.com/s?k=...` link and does NOT append a stray `&tag=`.
- HTML well-formed: starts `<!DOCTYPE`, ends `</html>`, no leaked Python `Traceback`.
- `autorun.sh` invokes `build.py` and runs `git push`.

## False-negative gotcha
A check like `assert 'href="https://www.amazon.com' in art` FAILS even when correct,
because (a) the rendered URL omits `www.` and (b) `&` is HTML-escaped to `&amp;`.
Match on the real substring `amazon.com/s?k=` instead. In v1 this produced a
17/18 "failure" that was actually a bad assertion, not a code bug — verify with a
direct grep before trusting a FAIL.
