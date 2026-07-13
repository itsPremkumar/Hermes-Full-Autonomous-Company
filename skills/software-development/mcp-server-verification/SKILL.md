---
name: mcp-server-verification
description: Verify an MCP (Model Context Protocol) server actually works over stdio — not just that it starts, but that it speaks JSON-RPC, lists tools/resources/prompts, and executes tool calls returning real data. Use when auditing, debugging, or proving an MCP server's connectivity ("check if the MCP connection works", "client connected but tools fail").
---

# MCP Server Verification

## When to use
- "check if the MCP connection works" / audit an MCP server
- debugging "client connected but every action fails"
- proving a server is functional before claiming it

## Technique (stdio JSON-RPC)
MCP servers speak JSON-RPC 2.0 over stdin/stdout. Drive them by piping a request file:

```bash
cat > /tmp/mcp_session.txt <<'EOF'
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized"}
{"jsonrpc":"2.0","id":100,"method":"tools/list"}
{"jsonrpc":"2.0","id":101,"method":"resources/list"}
{"jsonrpc":"2.0","id":102,"method":"prompts/list"}
EOF
npx tsx src/mcp-server.ts < /tmp/mcp_session.txt 2>/dev/null | python -c "
import sys,json
for line in sys.stdin:
    line=line.strip()
    if not line: continue
    try: d=json.loads(line)
    except: continue
    if d.get('id')==100: print('tools:', len(d['result']['tools']))
    if d.get('id')==101: print('resources:', len(d['result']['resources']))
    if d.get('id')==102: print('prompts:', len(d['result']['prompts']))
"
```

## Deep test: actually CALL a tool
Don't stop at initialize. Send a `tools/call` and confirm real output:
```json
{"jsonrpc":"2.0","id":20,"method":"tools/call","params":{"name":"list_output_videos","arguments":{}}}
```
Parse `result.content[0].text`. For write tools, set `ALLOW_UNSAFE_MCP_TOOLS=1` (see pitfall).

## Pitfalls
- **Safe-mode blocks mutations.** Many MCP servers run `safeMode:true` for the `mcp` runtime — ALL write tools throw `ForbiddenError: safe mode` by default. Read tools work; writes need `ALLOW_UNSAFE_MCP_TOOLS=1`. If "connection works but every action fails," check safe-mode + document the flag in README.
- **npx tsx, not node.** `node node_modules/.bin/tsx` fails (shim). Use `npx tsx src/file.ts`.
- **Cleanup test artifacts.** Write-tool tests mutate files (e.g. `input/input-scripts.json`). Restore with `git checkout -- <file>` after testing so the repo stays clean.
- **Don't claim "works perfectly" from initialize alone.** A server can handshake but have broken tool handlers — call at least one read + one write (with flag) tool.
