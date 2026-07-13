# Windows MSYS path doubling pitfall

## Symptom
On a Windows host where `terminal` runs MSYS/git-bash, calling the `write_file`
tool with an MSYS-style path such as:

    /c/Users/PREM KUMAR/money-engine/build.py

silently lands the file at a DOUBLED path:

    C:\c\Users\PREM KUMAR\money-engine\build.py

The tool emits a warning like "resolved to C:\c\... which is OUTSIDE the active
workspace" but STILL WRITES THE FILE there. The file is invisible to `cd /c/Users/...`
commands, which look in the real `C:\Users\...`.

## Root cause
The write tool normalizes the leading `/c` into a Windows root, then re-prepends
`C:` when computing the absolute path, producing `C:\c\Users\...`.

## Fix / rule
- Pass **native Windows absolute paths** to `write_file` on Windows hosts:
  `C:\Users\PREM KUMAR\money-engine\build.py`
- Reserve MSYS `/c/...` paths for commands INSIDE `terminal`/`bash` only
  (cd, cp, ls, python invocations).
- If you discover doubled files already created:
  `mkdir -p "/c/Users/<user>/<proj>" && cp -r "/c/c/Users/<user>/<proj>/." "/c/Users/<user>/<proj>/" && rm -rf "/c/c"` (the `/c/c` removal needs user approval for recursive delete).

## Detect early
After writing, run `search_files` / `terminal ls` to confirm the file is where you
expect before building on top of it.
