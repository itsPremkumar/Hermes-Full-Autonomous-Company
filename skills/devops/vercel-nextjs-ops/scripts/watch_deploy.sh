#!/usr/bin/env bash
# watch_deploy.sh — poll a Vercel project until the newest deploy is Ready or Error.
# Usage: bash watch_deploy.sh <project> <scope>   (scope optional)
# Prints "READY at +Ns (<deployid>)" or "FAILED at +Ns (<deployid>)".
set -u
PROJECT="${1:?usage: watch_deploy.sh <project> [scope]}"
SCOPE_FLAG=""
if [ -n "${2:-}" ]; then SCOPE_FLAG="--scope $2"; fi
for i in $(seq 1 26); do
  sleep 30
  raw=$(vercel ls "$PROJECT" $SCOPE_FLAG 2>&1)
  newest=$(echo "$raw" | grep -oE "${PROJECT}-[a-z0-9]+-prems-projects" | head -1)
  if echo "$raw" | grep -E "$newest.*Ready" >/dev/null; then
    echo "READY at +$((i*30))s ($newest)"; exit 0
  fi
  if echo "$raw" | grep -E "$newest.*(Error|Failed)" >/dev/null; then
    echo "FAILED at +$((i*30))s ($newest)"; exit 1
  fi
done
echo "wait-timeout"
