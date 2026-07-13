# Agent Activity Detection

How to determine whether the Hermes Engineer agent is actually working, idle, or stuck — by cross-referencing multiple signals rather than relying on a single endpoint.

## The Multi-Signal Problem

The Paperclip API exposes several signals about agent activity, but **none alone is sufficient**:

| Signal | What it tells you | Limitation |
|---|---|---|
| `GET /api/agents/<ID>` → `status` | `"idle"` / `"running"` | `"running"` just means "was nudged" — the agent may have no active run. |
| `GET /api/agents/<ID>` → `activeRunId` | Non-null when a run is tracked at agent level | Can be `null` even when an issue-level run is active. |
| `GET /api/agents/<ID>` → `lastHeartbeatAt` | When the scheduler last dispatched work | Recent timestamp = scheduler is healthy, but doesn't prove the agent is executing. |
| `GET /api/issues/...` → `activeRun` on each issue | Per-issue run tracking | Only shows runs bound to a specific issue. Quick check-out-and-exit runs may not leave one. |
| Run log files (`.ndjson`) | Actual agent output (tool calls, code, summaries) | Can lag by 30+ seconds behind real-time. Empty log = run just started or already stalled. |

## Decision Tree

### Step 1: Quick health check (always)
```bash
curl -s --max-time 5 "http://localhost:3100/api/health"
```
If not `{"status":"ok"}` → stop and recover the server first (see `continuous-development-loop.md`).

### Step 2: Agent endpoint snapshot
```bash
TOKEN=$(grep 'paperclip-default.session_token' /c/one/paperclip-company/cj.txt | awk '{print $NF}')
curl -s -H "Cookie: paperclip-default.session_token=$TOKEN" \
  "http://localhost:3100/api/agents/<AGENT_ID>" | python -c "
import json,sys
d=json.load(sys.stdin)
print(f\"status={d.get('status')}, activeRunId={d.get('activeRunId')}, lastHeartbeat={d.get('lastHeartbeatAt')}\")
"
```

### Step 3: Per-issue activeRun scan (more reliable than agent endpoint)
The agent-level `activeRunId` can be `null` while individual issues still have active runs. Always scan the issues:

```bash
curl -s -H "Cookie: paperclip-default.session_token=$TOKEN" \
  "http://localhost:3100/api/companies/<COMPANY_ID>/issues?assigneeAgentId=<AGENT_ID>" | python -c "
import json,sys
data=json.load(sys.stdin)
if isinstance(data, list):
    for i in data:
        ar = i.get('activeRun')
        if ar:
            print(f\"{i['identifier']}: run={ar.get('id')[:12]}... status={ar.get('status')} started={ar.get('startedAt')}\")
else:
    print('No issues found or response is not a list')
"
```

**If any issue has `activeRun` with `status: "running"` and a recent `startedAt`** (<30 min ago) → the agent IS active, regardless of what the agent-level endpoint says.

### Step 4: Run log directory check
```bash
ls -lt /c/one/paperclip-company/data/paperclip/instances/default/data/run-logs/<COMPANY_ID>/<AGENT_ID>/*.ndjson | head -5
```

**Signals from log files:**
| Observation | Meaning |
|---|---|
| New file with recent timestamp (within 60s) | Agent is actively being dispatched |
| Large file (>10 KB) | Agent did real work (tool calls, code) |
| Small file (<1 KB, 2-3 lines) | Run started but agent exited immediately (stale run or done-issue dispatch) |
| File of ~1–4 KB with startup warnings | Agent loaded but check the content: if it says `could not read agent instructions file` the AGENTS.md is missing — agent runs without company-specific context. The file is small because the agent had no instructions to follow. |
| No new files for >5 min | Scheduler may be stuck or saturated |
| File growing between checks | Agent is actively working right now |

### Step 5: Parse run log content with Python (ndjson streaming)
For a deeper look at what the agent actually accomplished:

```bash
cat /c/one/paperclip-company/data/paperclip/instances/default/data/run-logs/<COMPANY_ID>/<AGENT_ID>/<LATEST>.ndjson | python -c "
import json,sys
for line in sys.stdin:
    line=line.strip()
    if not line: continue
    d=json.loads(line)
    chunk = d.get('chunk','')
    # Extract key lifecycle signals
    if 'Exit code' in chunk or 'session_id' in chunk or 'Summary' in chunk \
       or 'maximum iterations' in chunk or 'timed out' in chunk or 'Starting' in chunk \
       or 'Warning:' in chunk:
        print(chunk[:250])
# Extract just the summary block for a quick status check
" 2>&1 | head -20
```

This extracts the start/end lifecycle of a run and its summary block in one pass. The summary block (generated when the agent reaches max iterations or exits) contains:
- What issue was being worked on
- What was accomplished
- What's still pending
- What the next heartbeat should do

### Step 6: Synthesize — is the agent idle?

**Agent is WORKING** if ANY of:
- Any issue assigned to the agent has `activeRun: {status: "running", startedAt: <recent>}`
- The run-log directory has a file <60s old with >1 KB
- A log file's `summary` block ends with "live continuation" or "in_progress" disposition
- Agent shows `lastHeartbeatAt` within the last 2 minutes AND a new run-log file appeared after that timestamp

**Agent is IDLE** if ALL of:
- No issue has an active run (all `activeRun: null`)
- Run-log directory has no files younger than 5 minutes
- Agent's `status` is `"idle"` OR `"running"` with a stale `lastHeartbeatAt` (>5 min old)
- At least one issue is `in_progress` (work waiting to be picked up)

**Agent is STUCK** if ANY of:
- Run-log file is only 2-3 lines (>2 min old) and the issue has `activeRun: {status: "running"}`
  → stale run occupying a slot (cancellation needed, see cron-pipeline-workflow.md)
- Agent `status: "running"` but no issue has an activeRun AND no new run-logs for >10 min
  → scheduler is hung (reset session + re-invoke heartbeat)
- Agent's `lastHeartbeatAt` is >30 min old
  → heartbeat scheduler may have stopped

## Common Patterns Seen In Practice

### Pattern A: Agent is truly working
```
Agent status: running
  activeRunId: null          ← agent-level may be null
  lastHeartbeatAt: 05:11:34  ← recent
Issue PRE-7: activeRun={status:running, startedAt:05:11:59}  ← per-issue confirms work
Run logs: 5 files in last 10 min, largest is 76 KB
```
**Verdict:** Working. The agent-level activeRunId being null is misleading — the per-issue activeRun is the real signal.

### Pattern B: Agent completed work but didn't update issue
```
Agent status: running
  activeRunId: null
  lastHeartbeatAt: <recent>
No issues have activeRun
Issue PRE-14: status=in_progress, activeRun=null
Latest run log: 13 KB, ends with "needed to commit + update issue" but ran out of iterations
```
**Verdict:** Idle with pending work. The last run exhausted tool-call iterations before updating the issue. A heartbeat should be invoked to let the agent finish the commit + status update.

### Pattern C: Stale run occupies a slot
```
Agent status: running
Issue with activeRun: {status:running, startedAt: <30 min ago>}
Run log: 700 bytes, 3 lines, just startup warnings — no growth
```
**Verdict:** Stale run. The agent process died/crashed but Paperclip didn't detect it. Cancel the run, reset session, re-invoke heartbeat.

### Pattern D: Queue saturated (all slots full)
```
Agent status: running
3 issues each have activeRun: {status:running}
No new run-log files for >5 min
Agent's lastHeartbeatAt is stale
```
**Verdict:** maxConcurrentRuns (default 3) is saturated. No slots available. Wait for a slot to free up (one of the active runs must finish or be cancelled).
