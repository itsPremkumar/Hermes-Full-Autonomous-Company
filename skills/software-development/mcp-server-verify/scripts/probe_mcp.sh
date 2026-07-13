#!/usr/bin/env bash
# probe_mcp.sh — verify an MCP server over stdio (handshake + tools/list).
# Usage: bash probe_mcp.sh "npx tsx src/mcp-server.ts" [unsafe]
# With "unsafe" as 2nd arg, sets ALLOW_UNSAFE_MCP_TOOLS=1 (enables write tools).
set -euo pipefail
CMD="${1:?Usage: probe_mcp.sh '<server command>' [unsafe]}"
if [ "${2:-}" = "unsafe" ]; then export ALLOW_UNSAFE_MCP_TOOLS=1; fi
printf '%s\n%s\n%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized"}' \
  '{"jsonrpc":"2.0","id":9,"method":"tools/list"}' \
  '{"jsonrpc":"2.0","id":10,"method":"resources/list"}' \
  '{"jsonrpc":"2.0","id":11,"method":"prompts/list"}' \
  | timeout 30 ${CMD} 2>/dev/null \
  | python -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try: d = json.loads(line)
    except: continue
    i = d.get('id')
    if i == 1:
        print('initialize :', 'OK' if d.get('result') else 'FAIL', '|', (d.get('result') or {}).get('serverInfo', {}).get('name', '?'))
    elif i == 9 and 'result' in d:
        print('tools      :', len(d['result'].get('tools', [])))
    elif i == 10 and 'result' in d:
        print('resources  :', len(d['result'].get('resources', [])))
    elif i == 11 and 'result' in d:
        print('prompts    :', len(d['result'].get('prompts', [])))
"
