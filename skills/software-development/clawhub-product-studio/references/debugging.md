# ClawHub Product Studio — debugging & technique bank

## 1. write_file token-corruption (the #1 quality trap)
`write_file` mangles Python identifiers in this environment. The linter says
OK because the mangled form is still a valid identifier — it's just the WRONG name.

Mangled → correct:
- `makedir` / `makesdir` → `makedirs`
- `web` (in `open(path, "web")`) → `wb`
- `tolen_hex` / `tolen_hx` → `token_hex`
- `sha26` → `sha256`
- `compare_digst` → `compare_digest`
- `hexdigst` → `hexdigest`
- `nonce` ↔ `nonce` (inconsistent across lines)

**Detect (run AFTER every write_file; do NOT trust lint):**
```bash
# exact-word regex; excludes correct 'makedirs' (makedir ⊂ makedirs)
grep -nE '\bmakedir\b|\btolen_hex\b|\bweb"\b|\bsha26\b|\bcompare_digst\b|\bhexdigst\b' file.py
# ZERO matches = clean. ANY match = corruption, fix via read_file + patch.
```

**Functional-proof every module before claiming done:**
```bash
cd /c/one/paperclip-company/clawhub-studio
python - <<'PY'
import sys, tempfile, os
sys.path.insert(0, r"C:\one\paperclip-company\clawhub-studio")
import studio.db as db
p = tempfile.mktemp(suffix=".db"); con = db.connect(p)
sid = db.create_skill(con, "d", "D")
vid = db.add_version(con, "d", "1.0.0", '{"name":"d"}')
rid = db.record_run(con, vid, "t", True, "PASS")
print("ok", sid, vid, rid); os.remove(p)
PY
```

## 2. The ad-hoc Temp-verifier infinite-flag loop
The system flags every changed path. Writing `hermes-verify-X.py` to
`AppData\Local\Temp` makes THAT file a flagged path next turn → you
delete it → next turn it's a stale flag → loop.

**Resolution: establish a canonical in-repo test command; never use Temp verifiers.**
- `python -m unittest tests.test_backend -v` (the suite)
- `python -m <pkg> self-test` (package entry that runs the suite)
- `ci/verify_product.py <folder>` (7-axis harness for skill pkgs)
Wire these into `.github/workflows/ci.yml`. The harness IS the
"verify from all perspectives" system.
If you must ad-hoc check, run INLINE (terminal heredoc) and don't write a
Temp `hermes-verify-*` file. State blockers honestly instead of faking green.

## 3. 7-axis portfolio harness (ci/verify_product.py)
Per product: structure (SKILL.md + .py | external-tool decl), frontmatter
(name/version/description), compiles (py_compile), self-test (real;
`python x.py self-test` rc=0 + "PASS", OR test_*.py, OR `test:` in SKILL.md),
security (no hardcoded secret), docs (Usage/Why), deploy-ready (ci_check.py).
NOTE: it expects `SKILL.md` — a *product app* (pyproject.toml +
package + tests) fails its structure axis by design. For apps, rely on
`python -m pkg self-test`, not the skill harness.

## 4. Moltbook rate-limit quirk
- Burst (6 posts at once): all return `201` but DON'T persist. A
  single spaced post persists.
- New agents: tight trust window, every post `429 "You can only post…"`.
  Loosens as the agent earns trust.
- Correct pattern: post ONE per tick (autonomy loop 30-min cadence), or a
  background poster with exponential backoff (90s → 5 → 10 → 20 → 30 min
  on 429; reset to 90s on success). Log to `.posted.json` for resume.
- Key: repo-root `.moltbook_key` (gitignored), never exported to product repos.

## 5. GitHub staging force-push (avoid rebase conflicts)
Repos that already had older `.github/workflows/ci.yml` / `ci/ci_check.py`
conflict on `git pull --rebase`. Force-push clean trees from a staging dir
(main repo = source of truth; mirrors are auto-generated):
```bash
STAGE=/tmp/stage; rm -rf $STAGE; mkdir -p $STAGE/x
cp -r clawhub-skills/<name>/. $STAGE/x/
cp docs/ci-workflow-template.yml $STAGE/x/.github/workflows/ci.yml
cp ci/ci_check.py ci/verify_product.py $STAGE/x/ci/
cd $STAGE/x; git init -q; git checkout -q -b main
git add -A; git commit -q -m "prod: <name> + CI"
git push --force -q https://<TOK>@github.com/itsPremkumar/<name>.git HEAD:main
```
Strip secrets first: `find . -iname '*moltbook_key*' -delete`.

## 6. ClawHub publish (auth as itsPremkumar)
```bash
clawhub publish "C:/one/.../folder" --slug <slug> --name "<Name>" --version 1.0.0 \
  --tags "openclaw,hermes,agent" --changelog "Initial release"
# Use ABSOLUTE path (relative "." can fail "SKILL.md required").
# Definitive success = returned id (k9…) + "✔ OK. Published".
# Do NOT trust curl 200 — clawhub.ai is a client-side SPA (see verify-live.md).
```
**Slug pitfalls:** `--slug clawhub-studio` → PROTECTED namespace error; use
`skill-studio`/`agent-skill-studio`. Relative `.` can fail "SKILL.md required";
absolute path always works. `--version` REQUIRED + semver.
**Verify live — `clawhub inspect <slug>`:** prints `Owner:`/`Created:`/`Latest:`.
`Owner: itspremkumar` = your live skill. Web URL is **owner-namespaced**:
`https://clawhub.ai/itspremkumar/skills/<slug>` (bare `clawhub.ai/skills/skills/<slug>`
404s even though curl returns 200 — SPA trap). See `references/verify-live.md`.

## 7. GitHub push: rebase-failure resolution (real miss)
`git init` in a staging dir then `git push` to a repo that ALREADY has history
fails: `! [rejected] (fetch first) / hint: 'git pull' before pushing again.`
`git pull --rebase` then CONFLICTS (`.github/workflows/ci.yml`, etc.) and
aborts — so nothing gets pushed. **Fix: clone the REAL remote, copy new files
in, commit, push (shared history, clean apply):**
```bash
TOK=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill | sed -n 's/^password=//p')
STAGE=/c/one/_stage_x; rm -rf "$STAGE"; mkdir -p "$STAGE"
git clone -q "https://$TOK@github.com/itsPremkumar/<repo>.git" "$STAGE/repo"
cp -r /c/one/src/clawhub-studio/. "$STAGE/repo/"   # overwrite, preserves .git
cd "$STAGE/repo"; git add -A
git commit -q -m "v0.2.0: ..." && git push -q origin main
# verify: git ls-remote shows new HEAD sha; curl contents API 200 for new file
```
Never `git init` + push to an existing remote — always clone-and-copy.

## 8. End-to-end product loop (the v0.1→v0.2 evolution)
A product isn't "complete" until its test/publish steps run on REAL generated
artifact code, not empty folders. Pattern: when a version is created, **scaffold
real files on disk** (`SKILL.md` + a `<tool>.py` with a real `self-test`
subcommand). Then:
- `POST /api/.../test` runs the generated tool's `self-test` → real PASS output.
- `POST /api/.../publish` (dry-run) operates on the actual skill folder.
This turned ClawHub Studio from "core loop works on empty dirs" into a
publishable product. Verify the scaffold with a subprocess self-test in
`tests/test_workspace.py`.
