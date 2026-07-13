# Multi-version CAD/simulation script triage

When a project has many versioned copies of the same engine (e.g.
`src/optimus_v14.py` … `optimus_v17.py`, plus duplicates and an `old_code/`
folder) and the user asks "which version is best?" or "run the vN":

## Steps
1. **List the real code, ignore `.git` internals**
   `search_files pattern="*.py" path=src target=files`
   Also grab docs: `*.md` (README, CHANGELOG, command.md).
2. **Size + recency signal**
   `wc -l src/*.py` and `git log --oneline -20` (+ `git log --format='%ci %s'`).
   Newest commit that names a version ("v17") is usually the intended latest.
3. **Confirm each candidate parses**
   `for f in src/*.py; do python -c "import ast;ast.parse(open('$f',encoding='utf-8').read())" && echo OK $f; done`
   (Fusion `adsk` imports won't resolve locally — syntax check only.)
4. **Read in-file version markers to see what each version ADDED**
   `grep -n "V17 NEW\|V16 NEW\|V15 NEW\|V14 NEW" src/optimus_v17.py`
   Newest file typically carries all prior markers = it's a superset.
5. **De-dupe check**
   `diff -q src/optimus_v_14.py src/optimus_prime_v14.py` etc. Flag near-identical
   copies as cleanup candidates; recommend keeping newest + one prior.

## Judgment
- **Best = newest that (a) compiles, (b) is a strict superset of earlier
  markers, (c) is the last git commit.** These engines evolve additively — each
  version keeps prior features and fixes, so latest-clean wins almost always.
- **README/CHANGELOG are frequently stale** (saw README claim "v9.0" while real
  code was v14–v17). Never answer a version question from the README alone;
  cross-check against `src/` + `git log` + in-file markers.
- Offer, but don't auto-do: update stale README/CHANGELOG, delete duplicate
  version files.

## Example (this project — Optimus_Prime, Fusion 360 robot)
Files v14–v17; README/CHANGELOG stuck at v9. v17 (5319 lines, last commit,
superset) = best. v16 controller pin meant `run_simulation.py` would have run
v16 unless `PAYLOAD_FILE` was repointed to v17 first. Three v14 files were
near-duplicate clutter.
