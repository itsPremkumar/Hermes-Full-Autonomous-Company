# MSYS Path-Doubling Bug (Windows Hermes host)

## Symptom
When using the `write_file` or `patch` tools with a `/c/one/...` (MSYS-style)
path on this Windows host, the tool RESOLVES the path to a DOUBLED location:

- You pass: `/c/one/sproutern-cloudflar/.mcp.json`
- Tool writes to: `C:\c\one\sproutern-cloudflar\.mcp.json`  ← wrong, doesn't exist as a real dir

The write "succeeds" but the file lands where neither you nor the project can
find it. Subsequent `ls`/`read_file` at the intended path shows "file not found",
and later steps operate on a stale or missing file. This burned several turns in
a real session (`.mcp.json`, `CLAUDE.md`, `CLOUDFLARE_DEPLOYMENT.md` all landed
in the doubled path before being caught).

## Root cause
The Hermes file tools normalize `/c/...` → `C:\...` but the MSYS shell layer
prepends `C:\` again, yielding `C:\c\...`. The `terminal` tool does NOT have this
bug because it runs through bash natively.

## Fix — write files via the terminal heredoc instead
For any file under `C:\one\...` (or `/c/one\...`), use `terminal` with a heredoc
rather than `write_file`/`patch`:

```bash
cd "C:/one/sproutern-cloudflar" && cat > path/to/file.md <<'EOF'
... content ...
EOF
```

Quoted `<<'EOF'` prevents shell expansion of `$`, backticks, etc. For Python
edits (precise string replace), run `python - <<'PYEOF' ... PYEOF` through the
terminal — it also avoids the doubling.

## When write_file/patch ARE safe
- Reading is fine (`read_file` resolves correctly).
- `patch`/`write_file` work when the path does NOT trigger the MSYS rewrite —
  but since the failure is silent and intermittent-looking, DEFAULT to the
  terminal heredoc for any `C:\one\...` / `/c/one\...` path on this host.
- After any `write_file`/`patch`, VERIFY immediately:
  `ls -la /c/one/<proj>/<file>` — if it's missing, it went to `C:\c\...`;
  move it: `mv "C:/c/one/<proj>/<file>" "C:/one/<proj>/<file>"`.
