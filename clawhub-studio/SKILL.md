---
name: clawhub-studio
version: 0.1.0
description: Local-first studio to author, test, version & publish agent skills — with a real backend, auth, test-runner UI, and one-click ClawHub publishing. Zero dependencies.
---

# ClawHub Studio

A local-first **web app** to author, test, version, and publish agent skills.
Replaces a folder of loose scripts with one cohesive, tested product.

## Why
Building agent skills by hand is error-prone and unverified. ClawHub Studio gives
you a real toolchain: SQLite-backed registry, signed auth, a test-runner UI, and
publish-to-ClawHub in one click.

## How to run (agent or human)
```bash
cd clawhub-studio
python -m studio serve --port 8000 --open
# → http://127.0.0.1:8000  (login is automatic)
```
- Create a skill, add a version (manifest), hit **Run self-test**, then **Publish (dry-run)**.
- Verify anytime: `python -m studio self-test` (31 tests) or `python -m unittest discover -s tests`.

## What's inside
- `studio/db.py` — SQLite repository (skill / version / run).
- `studio/auth.py` — HMAC-signed session tokens (no plaintext passwords).
- `studio/skills.py` — manifest parse/validate/version-bump/serialize.
- `studio/testrunner.py` — runs a skill's `self-test`.
- `studio/publish.py` — wraps `clawhub publish`.
- `studio/server.py` — REST API + static SPA host (path-traversal guarded).
- `web/` — single-page UI.

## Repository
https://github.com/itsPremkumar/clawhub-studio

## Tests / CI
GitHub Actions runs the suite on Python 3.8 and 3.11. All 31 tests must pass.
