# Windows / pnpm / MSYS pitfalls when self-hosting Paperclip + Hermes

Verified on a Windows 10 dev box: Node 22, pnpm 9, git-bash (MSYS), PostgreSQL 17 service,
Hermes Agent installed natively. These are the failure modes that cost the most time.

## 1. pnpm install "stalls" during linking (git-bash)

Symptom: log shows `Lockfile is up to date, resolution step is skipped`, `resolved 1248`,
`reused 1231`, then `added 0` frozen for minutes. `node_modules/.modules.yaml` never appears,
no CPU, 1 node process alive. The default `isolated` linker does hardlink/symlink work that
MSYS + Defender throttle badly on this filesystem.

Fix:
```
pnpm install --ignore-scripts --config.node-linker=hoisted --config.confirmModulesPurge=false
```
`hoisted` avoids the per-package symlink storm. `--ignore-scripts` skips the
`link-plugin-dev-sdk.mjs` postinstall (harmless dev-only symlinks). Once it finishes,
`server/node_modules/@paperclipai/hermes-paperclip-adapter` appears as a symlink to
`packages/adapters/hermes`.

Note: the first run may download ~1248 packages into the pnpm store (slow network → many
minutes). On a second run most are `reused` and it's fast.

## 2. MSYS path mangling breaks absolute Windows paths in bash

Symptom: `node /c/one/paperclip-company/.../tsx/dist/cli.mjs ...` throws
`Cannot find module 'C:\c\one\paperclip-company\...'` — an EXTRA `c:` is prepended by the
MSYS shell when you pass a `C:\` path to a Windows binary through bash.

Fixes:
- Run everything through a `.bat` file: `cmd.exe /c "C:/one/paperclip-company/run-server.bat"`.
  Inside the bat, native `C:\one\...` paths are correct.
- Use the workspace `.bin` shim (`../node_modules/.bin/tsx`) which works from the bash shell
  with a *relative* path. Do NOT call the absolute
  `node_modules/.pnpm/tsx@x/node_modules/tsx/dist/cli.mjs` directly — that triggers the
  mangling.

## 3. `node dist/index.ts` (compiled) crashes at runtime

Symptom: `Error [ERR_MODULE_NOT_FOUND]: Cannot find module '...packages/db/src/client.js'
imported from ...packages/db/src/index.ts`. The workspace `package.json` `exports` point at
`./src/index.ts` (source), and the runtime tries to load `.ts` directly.

Fix: run from source with tsx: `tsx src/index.ts` (from `paperclip/server`). The `pnpm build`
step is still needed to produce `dist/` for other packages and the onboarding/built-ins dirs,
but the SERVER entry should be launched via tsx, not `node dist/index.js`.

## 4. Embedded PostgreSQL refuses a Windows admin account

Symptom: server log:
```
ERROR: Embedded PostgreSQL failed ... "Execution of PostgreSQL by a user with
administrative permissions is not permitted. The server must be started under an
unprivileged user ID ..."
```
Paperclip's `server/src/index.ts` falls back to embedded Postgres when `DATABASE_URL` is unset.
On Windows, embedded Postgres refuses to run under an admin user.

Fix: use an EXTERNAL Postgres. This host already had PostgreSQL 17 installed as a Windows
service (`postgresql-x64-17`) on port 5432. Create a role + database and set:
```
DATABASE_URL=postgres://paperclip:paperclippw@localhost:5432/paperclip
```
(See `scripts/setup-pg-db.bat`.)

## 5. Creating the PG role/db without the postgres superuser password

pg_hba.conf is `scram-sha-256` for `local` AND `host`. `psql -U postgres` hangs on a password
prompt (no password known). Also: on Windows, psql connects over **TCP** (`host`), so changing
only the `local ... trust` line does NOT help — you must change the
`host 127.0.0.1/32 scram-sha-256` line to `trust`.

Procedure (idempotent bat):
1. `copy pg_hba.conf pg_hba.conf.bak` (backup).
2. Replace `host 127.0.0.1/32 scram-sha-256` with `host 127.0.0.1/32 trust`.
3. `net stop postgresql-x64-17` then `net start postgresql-x64-17` (restart loads new hba).
4. `psql -U postgres -h 127.0.0.1 -w -c "CREATE ROLE paperclip LOGIN PASSWORD 'paperclippw' SUPERUSER;"`
   and `CREATE DATABASE paperclip OWNER paperclip;`
5. Restore pg_hba from backup, restart service.

Gotchas:
- Use `ping -n 4 127.0.0.1 >nul` for a short sleep, NOT `timeout /t 2` — MSYS's `timeout`
  intercepts and errors, hanging the bat.
- `net user <name> <pw> /add` with a >14-char password prompts `Y/N` interactively; pipe `echo Y |`
  or use a shorter password.
- Grant the service/user access if needed: `icacls "C:\path" /grant:r user:(OI)(CI)F /T` (put in a
  bat — bash chokes on the parentheses).

## 6. `cmd.exe //c "..."` with a leading `&` orgs the child and exits

When launching a long-lived server, do NOT background inside cmd with `&` (the outer cmd exits
and kills the child; the log never gets server output). Instead run the `.bat` directly as a
background terminal process, or use `cmd.exe /c "C:/path/bat.bat"` with `> logfile 2>&1` and no
inner `&`. If piping to `head` in bash, SIGPIPE kills the server — don't pipe; redirect to a file.

## 7. `cmd.exe /c "C:\one\...\bat.bat"` returns immediately with only a prompt

This happened when the path had `//c` quoting issues from bash. Use forward-slash form:
`cmd.exe /c "C:/one/paperclip-company/run-server.bat"`. That reliably executes the bat body.

## 8. Flaky network causes npm/pnpm to fail mid-download

Symptom: `ECONNRESET`, `ETIMEDOUT`, or `ENOTFOUND` on specific tarballs during
`npm install` or `pnpm add`. Some packages download and link while others stall
permanently. Retries are too few and too slow by default.

Fix: add a `.npmrc` to the project root with aggressive retry settings:

```
fetch-retries=20
fetch-retry-factor=2
fetch-retry-mintimeout=1000
fetch-retry-maxtimeout=60000
fetch-timeout=120000
network-concurrency=4
child-concurrency=2
```

These give pnpm up to 20 retries with exponential backoff (starting at 1s, capping
at 60s), a 2-minute per-request timeout, and low concurrency to avoid saturating
a slow connection. For npm, the equivalent is `npm config set fetch-retries 20`.

On a very slow connection the first pnpm run may download ~1200 packages taking
15+ minutes. Subsequent runs reuse the store (most packages show `reused N`) and
are much faster.

## 9. Hoisted linker skips pre-built `dist/` files in omniroute

**Only for omniroute, not for Paperclip.** The Paperclip monorepo needs
`--config.node-linker=hoisted` to avoid MSYS symlink stalls. But if you apply
the same flag to omniroute's `pnpm install`, the pre-built `dist/server.js`
bundle never lands in `node_modules/omniroute/dist/` — the hoisted linker
prunes tarball entries under `dist/` (it treats them as if they were
already-hoisted top-level deps).

Symptom: omniroute boots past the polyfill, prints its banner, then exits with:
```
✖ Server not found at: C:\...\node_modules\omniroute\dist\server.js
  The package may not have been installed correctly.
```

Fix: install omniroute with the **default** linker, NOT hoisted:
```
pnpm install --ignore-scripts
```
No `--config.node-linker=hoisted`. The pre-built `dist/` and `src/` files
extract correctly. Use `--ignore-scripts` to skip postinstall native-module
copying (which also stalls on MSYS). The resulting install has `dist/server.js`
and boots cleanly.

If you already installed with hoisted, reinstall fresh:
```bash
rm -rf node_modules
pnpm install --ignore-scripts
```
