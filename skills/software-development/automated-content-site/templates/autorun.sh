#!/usr/bin/env bash
# autorun.sh -- weekly rebuild + publish (crash-proof: push failure is non-fatal).
set -e
cd "$(dirname "$0")"
git pull --rebase origin "$(git rev-parse --abbrev-ref HEAD)" 2>/dev/null || true
echo "[build] rendering site..."
python build.py
git add -A
if git diff --cached --quiet; then
  echo "[build] no changes to publish"
else
  git commit -m "auto: weekly rebuild $(date +%F)"
  git push origin "$(git rev-parse --abbrev-ref HEAD)" \
    && echo "[build] pushed to GitHub Pages" \
    || echo "[build] NOTE: push skipped (no remote/creds yet) -- site built locally in ./public"
fi
