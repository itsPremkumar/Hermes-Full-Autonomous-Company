# Debugging heavy Node CLIs on this low-RAM Windows box

## Symptom cluster (this host)
- 6 GB RAM total, often **70–150 MB free**, 565+ processes.
- A Paperclip / Omniroute cluster consumes ~100 MB each (several node.exe@~100MB).
- Heavy Node CLIs (`openclaw gateway`, `openclaw --help`) **hang** — the runtime
  can't finish loading plugins under memory starvation.
- git-bash shell throws `fork: Resource temporarily unavailable` (EAGAIN) on
  deep/recursive filesystem scans.

## Confirm a Windows-native node.exe is actually running
git-bash `/proc/<pid>/cmdline` does NOT expose Windows-native processes. Use WMIC:
```bash
wmic.exe process where "name='node.exe'" get ProcessId,CommandLine
```
Filter the output (e.g. `| grep -i "gateway --port"`). This is the only reliable
way to see what a node.exe is doing from the bash shell.

## Check RAM
```bash
grep MemFree /proc/meminfo          # in KB; <200000 = expect hangs
grep -E "MemFree|MemAvailable" /proc/meminfo
```
Also: `tasklist.exe /NH /FO CSV` piped to python to sum working sets (the CSV
memory column is field 5, but the header row's field 5 is wrong — skip it / sort
by numeric column 5).

## Bound every command with `timeout`
A hung call eats the 60s tool budget. Wrap everything:
```bash
timeout 8 curl -s ...
timeout 5 netstat -ano | grep :18789
timeout 25 openclaw gateway status
```
If it times out, the process is stuck (usually RAM), not silently fine.

## Avoid deep recursive greps
`grep -rIl` over `$HOME` or `C:\` triggers EAGAIN fork failures and 60s timeouts.
Target specific dirs/files instead. To find where a key/env var is set, scan known
config dirs explicitly (e.g. `C:\one\omniroute\start-omniroute.bat`).

## Free RAM before retrying a heavy boot
1. Find the stale gateway: `netstat -ano | grep :18789` → PID in last column.
2. `taskkill.exe /PID <n> /F`
3. Optionally free Paperclip/Omniroute node procs you don't need right now
   (identify via the wmic command above; ~500 MB recoverable).
4. Re-run the heavy command — should bind within ~30s once free RAM > ~200 MB.

## Port-in-use red herring
If a gateway is LISTENING but on an OLD config (wrong model/key), a fresh launch
can't bind and silently hangs. Always `netstat` first; kill the old PID; relaunch.

## Config re-read only on restart
OpenClaw (and similar Node gateways) read their JSON config at startup. Editing
`openclaw.json` does nothing until you restart the gateway process.
