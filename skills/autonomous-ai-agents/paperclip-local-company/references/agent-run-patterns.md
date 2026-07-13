# Agent Run Patterns — Diagnosis & Lifecycle

## Run Lifecycle States

Each heartbeat run follows this lifecycle:

QUEUED → DISPATCHED → RUNNING → COMPLETED / FAILED / TIMED_OUT

Runs are visible in three places:
- Issue `activeRun` field (per-issue) — set while the agent is processing that issue
- Agent `status` field — `idle`, `running`, `error`
- Run log files — `.ndjson` files in `run-logs/<COMPANY_ID>/<AGENT_ID>/`

## Failure Mode Diagnosis

The agent can fail in three distinct ways.

### Mode 1: Connection Error (immediate, after 3 retries)

**Symptoms:**
- Run log has only 4-6 lines total (~700-800 bytes)
- Lines: workspace fallback, missing-AGENTS.md warning, "Starting Hermes Agent",
  "API call failed after 3 retries: Connection error.", exit code 1
- Run duration: < 1 minute

**Cause:** Model provider returning connection errors. Transient provider issue,
rate limiting, or network interruption. NOT a Paperclip config problem.

**Response:**
- Check provider key validity and model name
- Wait for provider to recover (recovery system auto-retries)
- **Do NOT** cancel runs or reset sessions unnecessarily
- If persistent (>30 min), change model in `adapterConfig`

**Example log:**
```
[hermes] Starting Hermes Agent (model=tencent/hy3:free)
API call failed after 3 retries: Connection error.
[hermes] Exit code: 1, timed out: false
```

### Mode 2: Timeout (30 min, no output)

**Symptoms:**
- 3-4 startup lines, then silence for 30 minutes
- `[hermes] Exit code: null, timed out: true`
- File size ~500-800 bytes

**Cause:** Model never responded within timeoutSec (default 1800s). Overloaded
free models or stuck API connection.

**Response:**
- Recovery system handles retries
- Consider lowering `timeoutSec` (e.g. 300s)
- Consider switching to a more reliable model

### Mode 3: Successful Completion

- Run log has many lines (10KB+) with tool output
- `[hermes] Exit code: 0`
- Issue status updated, artifacts produced

## The Recovery Action Loop

When a run fails, Paperclip auto-creates a `stranded_assigned_issue` recovery with
a `wake_owner` policy. This can cascade into a failure loop if the root cause
(provider failure) hasn't resolved.

**Diagnosing recovery loop:**
1. `activeRecoveryAction.attemptCount` climbing rapidly
2. Runs failing every 30-60 seconds at ~700 bytes each
3. Agent `status: "error"` with null `errorReason`

**Breaking the loop:**
1. Fix underlying issue (switch models, provide working key)
2. Reset agent session: `POST /api/agents/<ID>/runtime-state/reset-session`
3. Cancel stale recovery actions if needed

## Agent Status Values

| Status    | Meaning                     | Has Active Run? | Action                      |
|-----------|-----------------------------|-----------------|-----------------------------|
| `idle`    | Ready to accept work        | No              | If backlog, invoke heartbeat|
| `running` | Nudged or actively working  | Maybe           | Check run-logs for progress |
| `error`   | Last run(s) failed          | No (usually)    | Diagnose, fix root cause    |

`status: "error"` with null `errorReason` and null `pauseReason` = "soft error" state.
Agent CAN still be woken (recovery system likely will).

## When to Invoke Heartbeat vs Not

**Do NOT invoke when:**
- Agent status is `error` — fix the cause first
- Last heartbeat <5 min ago — agent already being scheduled
- Recovery action has `attemptCount > 0` — system already waking agent
- No unassigned or blocked issues for the agent

**DO invoke when:**
- Agent status is `idle` with unassigned backlog work
- A recovery action completed but issue still needs processing
- After resetting an agent session (to start fresh)

## Cross-Referencing Run Logs to Issues

Run log filenames are UUIDs, not issue IDs. To find which issue a run served:
1. Run logs are created before issue selection — startup lines have no issue context
2. Check `lastActivityAt` on issues near the run log's file modification time
3. After run completes, the issue's `activeRun` or recovery `evidence.latestRunId`
   may reference the run UUID

## "Done Issue Still Gets Dispatched" Pattern

An issue marked `done` can still receive a heartbeat if the scheduler dispatches
before status propagation.

**Symptoms:**
- `completedAt` is BEFORE run's `startedAt`
- Run log is minimal (agent exits immediately)

**Response:**
- Cancel stale run, reset session
- No data loss (issue was already done)
- Wait a few seconds between marking done and assigning new work
