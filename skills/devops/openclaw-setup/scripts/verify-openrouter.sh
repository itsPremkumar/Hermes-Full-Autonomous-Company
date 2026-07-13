#!/usr/bin/env bash
# verify-openrouter.sh — lightweight probe: confirm the key works and that
# tencent/hy3:free returns non-empty content at max_tokens=200 (it is a
# reasoning model and returns empty at low max_tokens). No gateway needed.
set -euo pipefail

KEYFILE="$HOME/.openrouter_key"
MODEL="${1:-tencent/hy3:free}"

[ -s "$KEYFILE" ] || { echo "NO_KEY_FILE ($KEYFILE)"; exit 1; }
KEY="$(cat "$KEYFILE")"

echo "=== 1) chat completion (max_tokens=200) ==="
REPLY=$(timeout 25 curl -sS -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d "{\"model\":\"$MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"Reply with exactly: OK\"}],\"max_tokens\":200}" \
  | python -c "import sys,json;print(json.load(sys.stdin)['choices'][0]['message']['content'])" 2>&1 || echo "CURL_OR_PARSE_FAILED")

if [ -n "$REPLY" ]; then
  echo "OK -> model returned: '$REPLY'"
  echo "RESULT: PASS"
else
  echo "RESULT: FAIL (empty content — try raising max_tokens; hy3 is a reasoning model)"
  exit 1
fi
