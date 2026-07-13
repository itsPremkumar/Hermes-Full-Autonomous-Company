---
name: autonomous-company-ops
description: Run the Paperclip+Hermes+OpenClaw zero-budget AI company — server launch, GitHub-as-truth sync, memory discipline, and the 24/7 autonomy loop.
---

# Skill: Autonomous Company Operations

## When to use
Operating the "Hermes-Full-Autonomous-Company" (Paperclip 7-agent company) on this
low-RAM Windows box: launching the server, keeping GitHub as source of truth, running
the scheduled autonomy loop, and respecting the human-in-the-loop + memory rules.

## Environment facts
- GitHub pushes as `itspremkumar` via cached git creds — run git CLI directly, NO token
  or approval prompt needed.
- Paperclip server: `C:\one\paperclip-company\run-server.bat` (Postgres already on :5432;
  starts server on :3100). A Windows Scheduled Task `PaperclipServer` launches it on boot.
- OpenClaw gateway on :18789 (loopback). OmniRoute→OpenRouter on :18789 too (config).
- Low RAM: ~644MB free typical, can drop to ~100MB. Never spawn >2-3 heavy procs.

## Launch the company server (if down)
```
terminal(background=true): cmd.exe //c "C:\one\paperclip-company\run-server.bat"
then poll http://127.0.0.1:3100/api/health until 200
```

## Keep GitHub as source of truth
- Local folder `C:\one\paperclip-company` is a git repo tracking
  `github.com/itsPremkumar/Hermes-Full-Autonomous-Company` (branch `master`).
- Never commit secrets. `run-server.bat`/`watchdog.sh` read OPENROUTER_API_KEY from env
  only. NEVER hardcode it (GitHub secret scanning blocks the push).
- `paperclip/` (server source, ~200MB) and `node_modules/` are gitignored.
- Commit + push every change: `git add -A && git commit -m "..." && git push`.

## The 24/7 autonomy loop
- Cron job "Company Autonomy Loop" runs every 30 min, forever.
- Each tick: RAM check → git pull → read tasks.md + data/paperclip/issues → do the next
  AGENT-ACTIONABLE, NON-HUMAN-GATED task → commit + push.
- HUMAN-GATED (skip, flag user): Gumroad publish, payouts, bank/PayPal link, account
  signup, tax, any money movement, approving spend.

## Gotchas
- `find /c` deep scans hang under memory starvation — scope searches tightly.
- `write_file` with absolute `/c/...` paths gets a `C:\` prefix; that resolves to the
  same MSYS path, so the file lands correctly, BUT verify with `ls` after writing.
- If a `git reset --hard` is needed, back up untracked real files first (the live
  company folder holds the actual products).
