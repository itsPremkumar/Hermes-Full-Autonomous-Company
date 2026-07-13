# Windows MSYS / write_file Path Mismatch

## The problem

On a Windows host, the `terminal` tool runs under **git-bash (MSYS)** which translates
POSIX-style paths like `/c/one/project` to `C:\one\project`. However, the `write_file`
and `patch` tools resolve relative paths against the Hermes workspace
(`C:\Users\<user>`). This means:

| Tool | Input | Resolves to |
|------|-------|-------------|
| `terminal` | `cd /c/one/project` | `C:\one\project` ✅ |
| `write_file` | `/c/one/project/file.js` | `C:\c\one\project\file.js` ❌ |

## Symptoms

- A file written by `write_file` is not visible to `terminal` commands at the expected path.
- `ls -la /c/one/project/` shows it empty, but an equivalent `ls` at
  `C:/c/one/project/` finds the file.
- `npm install` inside the terminal fails with `ENOENT` because `package.json` isn't
  where the terminal expects it.

## Fixes

1. **Use `terminal` for all file operations under `/c/...` paths** when the file
   must be accessible to bash/Node commands. Redirect output with `>` or use
   `cat > file << 'EOF'` for content.

2. **Pass native Windows paths** to `write_file`/`patch`:
   ```
   C:\Users\PREM KUMAR\project\file.js
   ```
   These resolve directly against the filesystem without MSYS or workspace mediation.

3. **Recovery** when files have already landed in the wrong location:
   ```bash
   cp -r "C:/c/one/project/"* /c/one/project/
   rm -rf "C:/c/one"
   ```

## Prevention

If you're working on a project under `/c/...` on Windows:
- **Write the project structure first** with `mkdir -p` via `terminal`, then verify
  the directory tree.
- **Prefer `write_file` with paths that start with `C:\`** (full native Windows path)
  over `/c/...` POSIX-style paths.
- **Or use `terminal`** with heredocs (`cat > file << 'EOF'`) for files that live
  under `/c/...` trees and must be accessible to the shell.
- After writing critical files (package.json), verify with `ls -la` via terminal
  before doing `npm install`.
