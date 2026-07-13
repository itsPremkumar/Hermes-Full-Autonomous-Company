# Ad-hoc verification reference

Used when a repo has no canonical test/lint/build command. Patterns proven in a
Windows (git-bash) session auditing a Fusion 360 MCP robot script (Optimus_Prime).

## OS / shell facts
- Terminal tool runs bash via git-bash even on Windows. User home has a SPACE:
  `C:\Users\PREM KUMAR`. Hardcoded `%TEMP%` paths with spaces break some tools —
  prefer `tempfile.TemporaryDirectory(prefix="hermes-verify-")` so the OS picks a
  safe path and cleanup is automatic.
- `date -r <file> +%s` = file mtime epoch; `date +%s` = now. Diff = seconds since
  last write (detects stalled background processes).
- `grep -c '\[ERROR\]'` counts occurrences; `grep ... | sort | uniq -c` counts
  distinct values (proves a check varies vs is a no-op).

## What to check (targeted)
1. `ast.parse(open(f).read())` for every active module — catches syntax errors.
2. Controller points at the correct canonical file (version triage).
3. Functional fix proof: in a temp dir, write fake artifacts matching the NEW
   glob pattern AND the OLD pattern; assert NEW matches, OLD misses. This converts
   "I think this is a bug" into "OLD glob matched 0 of N real files".
4. Stale-ref sweep: regex over active tree (exclude `old_code/`, `.git`,
   `__pycache__`) for old version strings / nonexistent flags.
5. Doc/code agreement: README title, payload filename, CHANGELOG top entry,
   index.html all report the same version.

## Cleanup discipline
- After running, `rm -f` the temp script (or the whole tempdir) and `ls` to confirm
  zero `hermes-verify-*` remain.
- Report: `kind: ad_hoc`, scope, N/M checks, temp cleaned. NOT a suite.

## Proving a no-op / wrong-scope check (logical verification)
When a simulation module logs a metric per call (e.g. collision count), verify the
values actually vary per input. Command shape:
  grep "collision(s)" log.txt | sed -E 's/.*\[(.*)\] <\-> \[(.*)\].*/\1| \2/' | sort | uniq -c
If only ONE pair type appears for every joint/angle, the check re-tests the rest
pose every time -> it cannot detect motion-induced self-collision. Combined with
reading the source (a `simulate_sweep()` body that only logs, or an `_interfere()`
that builds one ObjectCollection over ALL bodies), this is conclusive.
