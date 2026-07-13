# Paperclip operations monitoring — detailed observations

Session date: 2026-07-12
Company context: Prem Autonomous Co (company ID 3056c999-...)
Primary agent: Hermes Engineer (agent ID 9eed5712-...)

This file captures ground-truth operational patterns discovered while monitoring
a live Paperclip company with 7 agents and ~60 issues. Use alongside the
"Operations monitoring" section in the SKILL.md for concrete examples.

## 1. Run log directory structure

```
<PAPERCLIP_HOME>/data/paperclip/instances/default/data/run-logs/<COMPANY_ID>/<AGENT_ID>/
```

Each file is `<RUN_UUID>.ndjson` — streaming NDJSON of stdout/stderr from Hermes.
Files are never deleted; old runs accumulate. The directory is the only real-time
progress indicator (the API's `stdoutExcerpt` stays empty until the run exits).

### Inspecting the latest runs

```bash
# Most recent first
ls -lt /c/one/paperclip-company/data/paperclip/instances/default/data/run-logs/3056c999-*/9eed5712-*/

# What issue is this run for? (lines 1-3 show the init)
head -3 <run_id>.ndjson

# Is it actively doing work?
tail -5 <run_id>.ndjson
# "review diff"     → agent is applying a change (good sign)
# "Exit code: 0"    → completed successfully
# "Exit code: null, timed out: true" → timed out at 1800s

# How much work was done?
wc -l <run_id>.ndjson
# >100 lines → substantive work
# 4 lines with "timed out" → agent produced nothing useful
```

## 2. Key issue lifecycle behaviors observed

### Auto-advance from `todo` → `in_progress`

PRE-34 (PRE-19-A: Burn guard + revenue ledger) was `todo` when first fetched.
On the next API poll (~5 min later), it was `in_progress` with an active run.
The heartbeat system auto-advanced it without manual PATCH.

**Implication**: You don't need to PATCH `status: "in_progress"` after assigning
an issue. Just set `assigneeAgentId` + `status: "todo"` and the heartbeat cycle
handles the rest.

### Run timeout → auto-respawn

Run e978e29a (PRE-34/PRE-19-A) started at 2026-07-12T15:00:53Z and timed out
at 15:31:11Z (30 min / 1800s — the Hermes `timeoutSec`). Despite the timeout,
the run log showed substantive code being written:
- `burn-guard.ts` (173 lines) — complete module with shell-escalation blocking
- `revenue-ledger.ts` (~139 lines) — complete ledger with record/list/sum
- `workspace-runtime.ts` — integration of the burn guard

A new run (bc5e04ff) was automatically spawned for the same issue. The code
changes were persisted despite the timeout (the git/filesystem writes happened
before the timeout).

**Implication**: A timed-out run does NOT lose work. Writes to the local
filesystem are durable. The auto-respawn ensures the agent continues.

### `in_review` status ≠ no active work

PRE-6 (Pricing tiers) was `in_review` with an active run actively editing
documents (CEO review feedback being incorporated). PRE-5 (Showcase repo) was
also `in_review` with a new run just starting.

**Implication**: `in_review` does not mean the issue is waiting — check for
an `activeRun` before assuming it needs a nudge.

### `blocked` status after failure

PRE-7 (Sample videos) went from `in_progress` to `blocked`. Its run log:
```
seq 1-3: init (agent load + startup)
seq 4: [hermes] Exit code: null, timed out: true
```
A 4-line run — the agent loaded, started, and timed out with zero output.
The system marked the issue `blocked` instead of re-spawning.

**Implication**: A `blocked` issue means the auto-respawn mechanism did NOT
trigger. This indicates the failure mode was different from a normal timeout
(the run may have failed before producing any output, or the timeout happened
before the agent wrote anything). Needs human triage.

### Active run vs API state discrepancy

PRE-7's run 86935249 showed as `status: "running"` in the API response's
`activeRun` object, but the log file clearly showed `timed out: true` at
15:00:43Z. The API still reported it as running 20+ minutes later.

**Implication**: `activeRun.status == "running"` may be stale. Cross-check with
the run log file's last line. The file-system is the source of truth for
liveness.

## 3. Done-issue audit walkthrough (PRE-12 example)

### Step 1: Identify done issues

```
GET /api/companies/:id/issues
→ filter status == "done"
```

Results from this session:
- PRE-12: Implement and publish monetization assets
- PRE-8: Direct outreach on free job boards
- PRE-3: Product analysis and zero-investment monetization plan
- PRE-41: AVG features spec
- PRE-44: PRE-13 follow-up: publish COMPANY_PLAN artifact

### Step 2: Read the completion note

For PRE-12, run 7eaf03f8 (the completion run) ends with:

```
Done. PRE-12 is complete, published, and verified.
...
One honest note for the board: the site currently uses placeholder contact
handles (prem-autonomous.co / hello@prem-autonomous.co) that are not yet
registered domains/inboxes. Next step (owner: CMO, per PRE-9's launch plan)
is to stand up the free business email and LinkedIn company page, then run
the week-2 outreach.
```

### Step 3: Check if follow-up is already captured

Search for existing issues that cover the stated next steps:
- PRE-5 (Showcase repo / LinkedIn page) — title includes "LinkedIn page"
- PRE-5 is `in_review` and assigned to the Hermes Engineer

Also check via `parentId`:
- PRE-12's `parentId` = PRE-9 (cancelled) — no child issues link back
- But PRE-5 is a sibling, not a child — it was created independently

### Step 4: Decision

In this case: **No new child issue needed.** PRE-5 already captures the LinkedIn
scope. The domain registration is a founder-only action (payment required) that
no agent can do.

For the other done issues:
- PRE-8 → PRE-11 (monitoring) is already set up. No action.
- PRE-3 → Spawned PRE-5,6,7,8. All accounted for. No action.
- PRE-41 → Spawned PRE-45,46. Both are `todo` and **unassigned** → needs
  follow-up assignment.
- PRE-44 → PRE-47 (follow-up) is `in_progress`. No action.

## 4. Reading multi-agent orchestration state

### Getting the full agent roster

```bash
GET /api/companies/:id
```
Returns `agents` array with each agent's `id`, `name`, `role`, `status`,
`lastHeartbeatAt`, and `runtimeConfig`. In this session, 7 of 8 agents were
`running` (1 paused).

### Identifying active runs across all agents

The API doesn't have a bulk "all running runs" endpoint. Instead, iterate
through all issues and check for `activeRun`:

```python
# Pseudo-code
for issue in GET /api/companies/:id/issues:
    ar = issue.get('activeRun')
    if ar and ar.get('status') == 'running':
        print(f"{issue['identifier']} | agent={ar['agentId'][:8]} | started={ar['startedAt']}")
```

In this session, 19 active runs were found across 7 agents — the system was
fully occupied.

### Python env on Windows

On this Windows host, `python3` does NOT exist (Command not found / exit 127).
Use `python` instead (Python 3.11.15). In git-bash/MSYS:
```bash
python -c "..."  # works
python3 -c "..."  # fails
```

For JSON processing of large API responses, write a helper script to a temp file
and run it with `python <script.py>` — avoids the memory/encoding issues that
occur with inline `python -c` on large payloads.

## 5. Cookie authentication detail

The cookie file at `C:\one\paperclip-company\cj.txt` is a Netscape-format jar.
The session token is rotated between sessions (compare token values before and
after server restarts). To use it:

```bash
# Option A: read the cookie file inline (works, but some curl versions fail on MSYS paths)
curl -s -b /c/one/paperclip-company/cj.txt ...

# Option B: extract the token and pass inline (more reliable)
TOKEN="paperclip-default.session_token=<value>"
curl -s --cookie "$TOKEN" ...
```

Only `GET` requests work with the cookie alone. Mutations (`POST`, `PUT`, `DELETE`)
return `{"error":"Board mutation requires trusted browser origin"}` (HTTP 403/404).
This is a server-side anti-CSRF measure — mutations require the `Origin` header
to match `http://localhost:3100` AND a valid session cookie. Even with both,
some curl builds may still be blocked depending on the Express middleware version.

## 6. The auto-assigner cron pattern (bridging the autonomy gap)

When an agent creates child issues, they are always left with
`assigneeAgentId: null`. To keep the pipeline flowing without manual PATCH:

```bash
# Hermes cron pseudo-code (run every 5-15 min, no_agent=true):
# GET /api/companies/:id/issues?status=todo
# For each issue where assigneeAgentId is null:
#   Determine correct agent (from title/description/labels)
#   PATCH /api/issues/:id { assigneeAgentId: "<ID>", status: "in_progress" }
```

Without this bridge, each completed issue creates orphans that stall. The
`scripts/watchdog.py` can be extended to include this logic in its 5-min cycle.
