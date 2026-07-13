#!/usr/bin/env bash
# verify-openrouter-model.sh — probe an OpenRouter model for tool-call support.
# Usage: OPENROUTER_API_KEY=sk-... ./verify-openrouter-model.sh tencent/hy3:free
# Exit 0 = model returns tool_calls (usable for autonomous Hermes agents).
# Exit 1 = no tool_calls / errored (do NOT use for self-executing agents).
# Exit 2 = missing key.
set -euo pipefail
MODEL="${1:-tencent/hy3:free}"
KEY="${OPENROUTER_API_KEY:-}"
if [ -z "$KEY" ]; then
  echo "ERROR: set OPENROUTER_API_KEY (export it, or it lives in run-server.bat)" >&2
  exit 2
fi
RESP=$(curl -s -m 40 "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer $KEY" -H "Content-Type: application/json" \
  -d '{
    "model":"'"$MODEL"'",
    "messages":[{"role":"user","content":"What is 2+2? Use the add tool."}],
    "tools":[{"type":"function","function":{"name":"add","description":"add two numbers","parameters":{"type":"object","properties":{"a":{"type":"number"},"b":{"type":"number"}},"required":["a","b"]}}}],
    "tool_choice":"auto"
  }')
echo "$RESP" | python -c '
import sys,json
try:
    d=json.load(sys.stdin)
except Exception as e:
    print("PARSE_FAIL", e); sys.exit(1)
msg=d.get("choices",[{}])[0].get("message",{})
fr=d.get("choices",[{}])[0].get("finish_reason")
tc=msg.get("tool_calls")
if tc:
    print("OK: model", d.get("model"), "returned tool_calls:", tc[0]["function"]["name"])
    sys.exit(0)
else:
    print("NO_TOOL_CALLS: finish_reason=",fr,"content=",(msg.get("content") or "")[:120])
    sys.exit(1)
'
