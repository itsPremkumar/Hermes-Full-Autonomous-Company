#!/usr/bin/env bash
# verify_freeplan.sh <base-url> <slugs-file>
# Checks, for each tool slug in <slugs-file> (one slug per line, e.g. "currency-converter"):
#   1. ISR caching active  -> X-Vercel-Cache: HIT or PRERENDER
#   2. JSON-LD WebApplication schema present in HTML
# Prints a per-page PASS/FAIL table + a summary count.
# Usage: bash scripts/verify_freeplan.sh https://www.sproutern.com /tmp/tool_slugs.txt
set -u
BASE="${1:?usage: verify_freeplan.sh <base-url> <slugs-file>}"
SLUGS="${2:?usage: verify_freeplan.sh <base-url> <slugs-file>}"
pass=0; fail=0
while read -r slug; do
  [ -z "$slug" ] && continue
  url="$BASE/tools/$slug"
  # cache-bust first hit to populate cache, then read second hit for HIT/PRERENDER
  curl -s -o /dev/null -D - "$url?v=$(date +%s%N)" >/dev/null 2>&1
  cache=$(curl -sI "$url" 2>/dev/null | grep -i "x-vercel-cache" | tr -d '\r' | awk '{print $2}')
  schema=$(curl -s "$url" 2>/dev/null | grep -o '"@type":"WebApplication"' | head -1)
  isr_ok=0; [ "$cache" = "HIT" ] || [ "$cache" = "PRERENDER" ] && isr_ok=1
  schema_ok=0; [ -n "$schema" ] && schema_ok=1
  if [ "$isr_ok" -eq 1 ] && [ "$schema_ok" -eq 1 ]; then
    echo "PASS  $slug  (cache=$cache, schema=yes)"; pass=$((pass+1))
  else
    echo "FAIL  $slug  (cache=${cache:-none}, schema=${schema:-no})"; fail=$((fail+1))
  fi
done < "$SLUGS"
echo "----"; echo "PASS=$pass  FAIL=$fail"
