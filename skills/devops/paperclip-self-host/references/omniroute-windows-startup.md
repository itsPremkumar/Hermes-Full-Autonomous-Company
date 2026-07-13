# Omniroute Windows startup gotchas

## Node.js 22: TypeScript polyfill from node_modules blocked

Omniroute's `bin/omniroute.mjs` imports `open-sse/utils/setupPolyfill.ts`. On
Node.js ≥22, importing `.ts` files under `node_modules/` fails with:
```
ERR_UNSUPPORTED_NODE_MODULES_TYPE_STRIPPING
```

**Fix:** Convert the polyfill to plain JS (.mjs) and repoint the import.

1. Download the polyfill source from GitHub:
   `https://raw.githubusercontent.com/diegosouzapw/OmniRoute/main/open-sse/utils/setupPolyfill.ts`

2. Rewrite as plain ESM (`setupPolyfill.mjs`): remove TypeScript type annotations
   (`as any`, `: T`, `: any`), generic parameters, and interface syntax.

3. Save to `node_modules/omniroute/open-sse/utils/setupPolyfill.mjs`.

4. Patch the import in `bin/omniroute.mjs`:
   ```diff
   -await import("../open-sse/utils/setupPolyfill.ts");
   +await import("../open-sse/utils/setupPolyfill.mjs");
   ```

## `serve` subcommand required in start script

Running `node bin/omniroute.mjs` without a subcommand boots the CLI (prints
banner + version), but exits before starting the HTTP server. The `serve`
command is the default (`isDefault: true`) in Commander, so it only starts
when no other subcommand is matched — but without explicit `serve` in the
start script, the process can exit prematurely.

**Fix:** Always pass `serve` explicitly in start scripts:
```
node node_modules\omniroute\bin\omniroute.mjs serve --port 20128 --no-open
```

## `dist/server.js` not found

The server checks `existsSync(join(ROOT, "dist", "server.js"))` and falls back
to `app/server.js`. If neither exists, it errors out with:
```
✖ Server not found at: ...dist/server.js
```

**Causes:**
- pnpm `--config.node-linker=hoisted` strips the pre-built `dist/` bundle.
  Reinstall with default (isolated) linker: `pnpm install --ignore-scripts`.
- npm `TAR_ENTRY_ERROR` on Windows — the tarball has symlinks that can't
  extract. Use pnpm (default linker) instead.

## First-run 500 error

After a clean install, Omniroute starts and listens on port 20128 but returns
`Internal Server Error` (HTTP 500) on all routes. This is expected — the
first-time setup wizard needs a browser visit to `http://localhost:20128` to
create the admin account and init the SQLite database.

**Credentials:** The `INITIAL_PASSWORD` from `.env` (at `~/.omniroute/.env`).
