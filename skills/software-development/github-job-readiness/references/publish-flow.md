# Publishing a Local Repo to GitHub (this Windows env)

## Reality of this environment (verified)
- `gh` CLI is **NOT preinstalled** (`where gh` -> nothing; not in Program Files/AppData; npm global empty).
  **It CAN be installed on demand** (see Path C) — `gh` is available after that.
- **No `GITHUB_TOKEN`** env var. No cached PAT.
- `curl https://api.github.com/user` -> **401** (can't create repos via API unauth).
- `git push` to an **existing** repo works via **cached Windows git credentials** (git authed as
  premkumar016555@gmail.com). So: push works, but *creation* does not — unless `gh` is installed
  and the user logs in via the browser device-code flow.

## The publish flow (only viable paths)
### Path A - user creates the empty repo, agent pushes (zero secrets)
1. Tell user: go to https://github.com/new -> Name `<repo>` -> **Public** ->
   **UNCHECK** "Initialize with README" -> Create.
2. Agent runs (in repo dir):
   ```bash
   git remote add origin https://github.com/<u>/<repo>.git
   git branch -M main            # if local branch is 'master', rename to 'main'
   git push -u origin main
   ```
   Uses cached creds -> succeeds without token.
3. Confirm via API: `curl -s https://api.github.com/repos/<u>/<repo>`

### Path B - user provides a fine-grained PAT (repo scope)
1. Agent uses curl/git with the token:
   ```bash
   curl -X POST "https://api.github.com/user/repos" -H "Authorization: Bearer <PAT>" \
     -H "Accept: application/vnd.github+json" \
     -d '{"name":"<repo>","description":"...","public":true}'
   git remote add origin https://github.com/<u>/<repo>.git
   git push -u origin main
   ```
2. User revokes the PAT afterward.

### Path C - install gh, user auths via device-code, agent runs gh (PROVEN THIS SESSION)
`gh` is not preinstalled, but the official Windows binary installs cleanly. The agent runs the
install + the `gh repo create --push`; the USER does the browser approval (agent never sees the
password/2FA). This is the cleanest "use the GitHub command" path.

**Install (agent runs this — no sudo needed):**
```bash
# WRONG: `npm install -g github-cli` installs an unrelated deprecated package, NOT gh.
# RIGHT: download the official release zip and unpack:
cd /c/Users/PREM KUMAR/Downloads            # or any temp dir
curl -sL -o gh.zip "https://github.com/cli/cli/releases/download/v2.65.0/gh_2.65.0_windows_amd64.zip"
powershell -NoProfile -Command "Expand-Archive -Force -Path gh.zip -DestinationPath gh-bin"
# gh.exe lands at: gh-bin/bin/gh.exe
```
Note: `winget` is ALSO not on PATH in the MSYS/bash shell here (Start-Process can't find it),
so the direct-zip method is the reliable one. `tar -xzf` on the zip also failed (it's a zip, not
tar) — use PowerShell `Expand-Archive`.

**Auth (agent starts it in background, user approves in browser):**
```bash
# Run in background so the agent can surface the one-time code instead of blocking:
"/path/to/gh-bin/bin/gh.exe" auth login --web -p https -h github.com
```
- Poll the background process output for: `! First copy your one-time code: XXXX-XXXX` and the
  `https://github.com/login/device` URL.
- Give the code to the USER; they open the URL, paste it, approve. The `gh` process completes
  auth automatically (token writes to `~/.config/gh/`, NOT the project folder — so the project
  can be moved before/after without breaking auth).
- Agent CANNOT run `gh auth login` interactively itself — it needs the user's browser session.

**Create + push (agent runs, after auth succeeds):**
```bash
cd /c/path/to/repo
"/path/to/gh-bin/bin/gh.exe" repo create <repo> --public --source . --push \
  --description "one-line description"
```
This single command creates the repo AND pushes the current branch. CI goes green on GitHub
automatically (assuming ci.yml is present and passes locally).

## Pitfalls
- Do NOT claim the repo was "published to GitHub" until `git push` actually succeeded AND you
  verified the repo exists via the API. A committed-local repo is NOT published.
- Don't waste turns retrying `gh`/`curl-create` without auth - they 401 deterministically (before
  `gh` is installed + authed).
- If local branch is `master` but GitHub default is `main`, `git branch -M main` before push,
  or the push creates a stray `master` branch. (`gh repo create --push` pushes the current branch;
  rename first if it's `master`.)
- Keep flagship job-hunt repos **public** (private can't be cloned/verified unauth).
- Moving the repo folder (e.g. robocopy to `C:\one\`) is safe — `gh` auth token lives in the home
  dir, and git internals stay intact. Kill any in-flight `gh auth login` background process before
  moving, then re-run login from the new path if needed.
- `npm install -g github-cli` is a TRAP — it installs the wrong package. Use the official zip.
