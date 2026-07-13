# Cron Pipeline Workflow

Operational checklist for the `company-revenue-pulse` cron job. Each 15-minute run
should execute this sequence to keep the issue pipeline moving.

## 0. Pre-Flight: Gather Live Signals (3 Checks)

Before issuing any mutations, collect three lightweight signals to determine
whether the pipeline actually needs intervention. These prevent unnecessary
heartbeat invocations and mistaken status changes.

### 0a. Agent Fleet Status

Get the current status and last heartbeat of every agent:

```bash
TOKEN=$(grep 'paperclip-default.session_token' /c/one/paperclip-company/cj.txt | awk '{print $NF}')
curl -s -H "Cookie: paperclip-default.session_token=$TOKEN" \
  "http://localhost:3100/api/companies/<CID>/agents"
```

Key signals for the Hermes Engineer agent (9eed5712):
- **`status: running` + heartbeat within last 5 min** → agent is actively
  executing work. Skip heartbeat invoke unless you have fresh high-priority
  work that's definitely not being covered.
- **`status: idle` + stale heartbeat (>10 min)** → agent needs a nudge if
  there are ready `in_progress` or newly-assigned issues.
- **`status: error`** → agent fault; reset session before attempting heartbeat.
- **`status: paused`** → agent was manually paused; do NOT invoke heartbeat.

### 0b. Autonomy Loop Log (the 30-min cron, not Paperclip heartbeat)

```bash
tail -10 /c/one/paperclip-company/autonomy-loop.log
```

The autonomy loop and Paperclip's heartbeat scheduler are **independent**. Each
runs on its own cadence (30m vs 30s) and dispatches from different queues:
- `"task board size: 0"` repeated across ticks → the autonomy-level scheduler
  has no queued work. This is **normal** alongside Paperclip issues being
  actively worked — the two systems don't share a queue.
- `"No actionable agent task this tick. Running self-improve pass."` → the
  autonomy loop found no Paperclip issues to dispatch either. Cross-reference
  with the Paperclip agents list (0a): if the Hermes Engineer agent is
  `running` and has a recent heartbeat, the Pipeline is healthy despite the
  loop's "no task" log — Paperclip's independent heartbeat scheduler is
  handling dispatch.

### 0c. Expected-vs-Actual Status Validation

Task context (the cron prompt or user instruction) may claim issues have a
status that differs from the live API. Always trust the API. Common mismatches
found in practice:

| Stated status | Actual API status | Meaning |
|:---|---:|:---|
| `in_progress` | `in_review` | Agent finished work; human review needed. No heartbeat needed. |
| `in_progress` | `blocked` | Issue stalled on a dependency (usually a child). Target the blocker child, not the parent. |
| `in_progress` | `done` | Work completed between prompt-write and cron execution. No action needed. |
| `in_progress` | `backlog` | Issue was deprioritised after the prompt was written. Respect the API state. |

**Rule:** Never mutate an issue's status based on what the prompt expects. If
the API says `in_review` but the prompt says `in_progress`, the API is right
— the agent advanced the state since the prompt was written.

## 1. Probe Server Health

Before any mutation, verify the server is serving:

```bash
curl -s --max-time 5 "http://localhost:3100/api/health"
# Expected: {"status":"ok",...}
```

If health fails but `ps -W | grep node` shows node.exe alive → zombie process
recovery (see `references/continuous-development-loop.md`).

## 2. Fetch All Issues

```bash
TOKEN=$(grep 'paperclip-default.session_token' /c/one/paperclip-company/cj.txt | awk '{print $NF}')
curl -s -H "Cookie: paperclip-default.session_token=$TOKEN" \
  "http://localhost:3100/api/companies/<COMPANY_ID>/issues"
```

## 3. Detect and Cancel Stale Runs

**Signature of a stale run:**
- Issue is `status: done` OR the run was dispatched for an already-completed issue
- `activeRun` exists on the issue with `status: running`
- Run log (in run-logs dir) has **only 2–3 lines** — just startup warnings and
  `[hermes] Starting Hermes Agent` — no tool calls, no output
- The run's `startedAt` is *after* the issue's `completedAt` (the auto-dispatch
  happened after completion, which means the agent loads → sees done → exits)

**Cancellation:**
```bash
curl -s -X POST "http://localhost:3100/api/heartbeat-runs/<RUN_ID>/cancel" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "X-Requested-By: paperclip"
```

**Why this blocks the pipeline:** The stale run occupies one of `maxConcurrentRuns`
slots (default 3). New work won't dispatch until a slot frees up.

## 4. Reset Agent Runtime Session

After cancelling stale runs, always reset the session to wipe stale Hermes state:

```bash
curl -s -X POST "http://localhost:3100/api/agents/<AGENT_ID>/runtime-state/reset-session" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "Content-Type: application/json" \
  -H "X-Requested-By: paperclip" \
  -d '{}'
```

## 5. Create Follow-Up Child Issues for Done Items

For each `done` issue that represents completed work with a next step missing,
create a child issue with `assigneeAgentId` set. This auto-triggers a heartbeat
run immediately — no 30s tick wait.

**Targets (from this session's revenue pipeline):**
| Parent (Done) | Next Step | Priority |
|:---|---|:---:|
| PRE-56 (prompt-executor CLI) | Publish to GitHub/npm + add to showcase | medium |
| PRE-58 (Developer Prompt Pack $14) | Publish on Gumroad with product listing | medium |
| PRE-59 (Revenue dashboard M1) | Month-2 projection, burn analysis, runway update | medium |
| Future: any `done` CODE/DIGITAL PRODUCT/CONTENT issue | Identify the next publication or distribution step | — |

```bash
curl -s -X POST "http://localhost:3100/api/companies/<COMPANY_ID>/issues" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "Content-Type: application/json" \
  -H "X-Requested-By: paperclip" \
  -d '{"parentId":"<PARENT_ISSUE_ID>","title":"Next step title","priority":"medium","assigneeAgentId":"<AGENT_ID>"}'
```

**Important: POST (new issue) vs PATCH (existing issue) auto-trigger asymmetry.**

- **POST** a new issue with `assigneeAgentId` set → **DOES auto-trigger** a heartbeat immediately. The issue flips to `in_progress` with an `activeRun` within <1 second. Do NOT also call heartbeat/invoke after creating — the auto-dispatch handles it.
- **PATCH** an existing issue to set `assigneeAgentId` + `status: "in_progress"` → **does NOT auto-trigger** a heartbeat. The update persists but the agent stays idle until the next scheduler tick (30s) or a manual heartbeat invoke. Always follow a PATCH-assign with an explicit heartbeat invoke (section 8) if you want immediate execution.

**Why the difference:** The server's `assignAgent` route (creation path) fans out to `assignAndDispatchRunImmediately`. The `updateIssue` route (PATCH path) only persists fields and relies on the tick scheduler. This is by design — PATCH via API is not assumed to be a human-wants-it-now action.

## 6. Unblock Timed-Out Issues

Issues that were `in_progress` but timed out appear as `blocked` with an
`activeRecoveryAction` of kind `stranded_assigned_issue` and evidence
`latestRunErrorCode: timeout`.

**Reset them back to in_progress:**
```bash
curl -s -X PATCH "http://localhost:3100/api/issues/<ISSUE_ID>" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "Content-Type: application/json" \
  -H "X-Requested-By: paperclip" \
  -d '{"status":"in_progress","comment":"Unblocked by cron: previous run timed out. Resetting for retry."}'
```

**When to do this:** Only for issues where (a) the work is still relevant,
(b) the timeout was a genuine runtime limit not a logic error, and (c) the
issue still has an assignee. If the timeout was caused by a bug, create a
follow-up issue for the fix first.

## 7. (Optional) Assign Unassigned Todo/Backlog Issues

Check for issues with `status: todo` or `status: backlog` and no
`assigneeAgentId`. If found, assign to the Hermes Engineer:

```bash
curl -s -X PATCH "http://localhost:3100/api/issues/<ISSUE_ID>" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "Content-Type: application/json" \
  -H "X-Requested-By: paperclip" \
  -d '{"assigneeAgentId":"<AGENT_ID>","status":"in_progress"}'
```

**⚠️ PATCH does NOT auto-trigger a heartbeat.** Unlike POST (section 5), PATCHing an
existing issue only persists the fields. You must explicitly invoke a heartbeat
afterwards (section 8) for the agent to pick up the newly assigned work.

## 8. Invoke Heartbeat (if needed)

Invoke a heartbeat explicitly when any of these are true:
- You PATCH-assigned an existing issue (section 7) — the agent needs a nudge
- No new POST-created child issues auto-triggered because maxConcurrentRuns was full
- The agent is idle (`status: "idle"` or stale `lastHeartbeatAt`) and there are `in_progress` issues waiting

```bash
curl -s -X POST "http://localhost:3100/api/agents/<AGENT_ID>/heartbeat/invoke" \
  -H "Cookie: paperclip-default.session_token=$TOKEN" \
  -H "Origin: http://localhost:3100" \
  -H "X-Requested-By: paperclip"
```

This returns a run with `status: "queued"`. The agent transitions to `status: "running"`
immediately (even before the run actually starts executing). Verify actual dispatch
via the run-log directory check in section 9.

**When NOT to invoke:**
- You just POST-created an issue with `assigneeAgentId` — the auto-dispatch already triggered
- `maxConcurrentRuns` is saturated (3/3 slots full) — the invoke will stay queued until a slot frees up

## 9. Verify Dispatch

Check that new runs started:

```bash
ls -lt /c/one/paperclip-company/data/paperclip/instances/default/data/run-logs/<COMPANY_ID>/<AGENT_ID>/*.ndjson | head -5
```

New `.ndjson` files with recent timestamps = agent is dispatching. Each file
growing past initial startup lines = the agent is actively working.

## Diagnostic: Run Log Size Tells the Story

| File Size | Lines | Meaning |
|:---|---:|:---|
| ~700–800 bytes | 2–3 | Run started but agent exited immediately (stale/dispatch-on-done issue) |
| ~1–4 KB | 5–30 | Agent loaded context, made a comment or startup warnings, then exited. **Check for `ENOENT` or `could not read agent instructions file` in the log — if present, the AGENTS.md is missing and the agent runs without company-specific context.** |
| 10–100 KB | 50–500+ | Agent did real work — tool calls, code changes, API interactions |

## Data Processing Mechanics for Cron Jobs

### JSON with multi-line description fields breaks pipe-to-stdin

Paperclip API responses embed newlines in `description` fields. Piping curl output directly to `python -c` delivers **only the first JSON line** to stdin — the rest is lost, causing `JSONDecodeError: Expecting value`.

**Patterns that reliably work:**

1. **Python subprocess** — Write a `.py` script that calls curl via `subprocess.run(['curl', ...], capture_output=True)`. The full response lands in `result.stdout` as a Python string, not through a line-bounded OS pipe.
2. **Save to file, then read** — `curl -o /tmp/issues.json` writes the full response to disk; then `python -c "json.load(open('/tmp/issues.json'))"` reads it whole.
3. **Write script to disk (cron-safe, preferred)** — `execute_code` is blocked in cron mode. Instead: `write_file` the script to a `.py` file on disk, then run it with `python script.py`. This is the canonical cron- job implementation pattern.

### PATCH `/api/issues/:id` may return HTTP 400 with empty body

The PATCH mutation can return HTTP 400 with no error message. Possible causes (check in order):

- **Missing `X-Requested-By: paperclip`** alongside `Origin` — some Paperclip builds deny mutations with Origin alone and require this header.
- **Body validation failure** — `updateIssueRouteSchema` uses strict parsing; extra undocumented fields get silently rejected. Stick to: `assigneeAgentId`, `status`, `title`, `description`, `priority`, `comment`.
- **Agent Bearer token vs cookie** — the GET endpoints accept user-session cookies; PATCH mutations may require `Authorization: Bearer <agent-api-key>` (generated via `POST /api/agents/:id/keys`). A user-session actor may lack privilege for certain mutation paths.

**Fallback:** When PATCH returns 400, create a new child issue with `assigneeAgentId` set (which auto-dispatches work) instead of trying to modify an existing one.

### Read run log summaries for next-step recommendations

Agent run logs end with structured summaries containing explicit follow-up suggestions. Always `tail` the most recent run log for each `done`/`in_review` issue to check for:

- **"I recommend spinning a small child issue for X"** — the agent identified durable work that should be its own issue
- **"The only unfinished part is the human-only publish step"** — the agent deliverable is complete but distribution needs a tracked child issue
- **"Root cause: the script-parser orphan-tag bug"** — the agent worked around a shared bug without fixing it; the fix is a separate issue

From the run log summary, create child issues with `assigneeAgentId` set to auto-trigger execution.

### "Done parent → unassigned child" follow-up (PRE-7 → PRE-74)

When a completed issue's run log says "publishing/shipping is a manual step" AND a child issue already exists tracking that step but is left unassigned (the autonomy gap):

1. Assign the child to the agent so it enters the tracked workflow — the agent may still complete sub-steps (draft instructions, prepare assets, generate thumbnails) even if the final publish action is human-only
2. The agent's status for that child becomes `in_progress` and shows up in liveness checks
3. This prevents orphan issues that stall the pipeline but still correctly flags human-gated steps

### Blocked-chain unwinding pattern

A parent issue at `blocked` may be stalled because of a chain of children, each blocked
by its own child. Only the deepest issue in the chain is actionable:

```
PRE-7 (blocked)  ← blocked by
  └─ PRE-74 (blocked)  ← blocked by
       └─ PRE-76 (in_progress)  ← the actionable item, being worked
```

**Workup rule:** When you find a `blocked` issue, follow its parent-child chain
downwards by checking each child's `status` and `blockerAttention` field
(`blockerAttention.state: "covered"` with `reason: "active_child"` confirms the
blocker is a child issue, not an external dependency). If the deepest child is
`in_progress` and has an `activeRun`, the chain is being handled — no intervention
needed. If the deepest child is `todo` or unassigned, that's where the intervention
should focus.

To find children of a blocked issue in the API response:
```python
for issue in all_issues:
    if issue.get('parentId') == blocked_id:
        print(f"  child: {issue['identifier']} status={issue['status']} assignee={issue.get('assigneeAgentId','?')}")
```

### "No action required" is a valid pipeline outcome

Not every cron check needs to create issues or invoke heartbeats. The pipeline
is healthy when **all** of these are true:

1. All target issues are either `in_progress`, `in_review`, or `done` — no
   stagnating `todo`/`backlog` items that should be active.
2. Done issues already have child issues covering follow-up work, OR the
   deliverable is complete with no durable next step (e.g., a finished ops
   playbook).
3. The Hermes Engineer agent is `running` with a recent heartbeat.
4. No stale runs are occupying `maxConcurrentRuns` slots (run logs < 5 lines
   are the diagnostic).

When these hold, report "Pipeline healthy, no intervention needed" and exit.
This is the expected steady state of a functioning autonomous company — not a
reason to create busywork issues.

### Cross-reference run IDs with issue identifiers

Run log files use UUID filenames (`*.ndjson`). To find which issue a run served:
- The `executionRunId` field on the issue object contains the run UUID (minus `.ndjson`)
- The run log's first lines usually name the issue title and identifier
- A run created *after* an issue's `completedAt` timestamp is a stale/ghost dispatch — `startedAt > completedAt` on the same issue is the diagnostic signature

## Edge Cases Handled This Session

1. **Done issue with fresh running run (PRE-18)**: The issue's `completedAt` was
   `04:32:36.703Z` but the run `startedAt` was `04:32:36.819Z` — a full 116ms
   *after* completion. The system dispatched a new run for an issue that was
   already done. Detected by: issue has `activeRun` + run log has only 2 lines.

2. **maxConcurrentRuns saturation at 3/3**: Creating 3 new child issues with
   `assigneeAgentId` immediately filled all 3 slots. Additional ready work (PRE-7,
   heartbeat invoke) queued waiting for a slot. The 30s tick scheduler handles
   dispatch when slots free up.

3. **Recurring timeout (PRE-7)**: Sample video generation timed out at 1800s.
   The agent had made durable progress (3 video scripts written to AVG) before
   timeout. Resetting to `in_progress` lets it resume from where it left off.

4. **PATCH-assigning an existing issue does NOT trigger a heartbeat**: Patching
   PRE-74 (existing issue, was `todo` with no assignee) to set `assigneeAgentId`
   + `status: in_progress` persisted correctly but the agent remained idle. A
   manual `heartbeat/invoke` was required for the agent to pick up the newly
   assigned work. This is by design: POST triggers auto-dispatch, PATCH does not.

5. **AGENTS.md missing → agent runs without context**: The heartbeat run log
   started with `Warning: could not read agent instructions file`. The agent
   produced output but lacked company-specific context (budget caps, operating
   principles). The instructions directory exists at:
   `<PAPERCLIP_HOME>/instances/default/companies/<CID>/agents/<AGENT_ID>/instructions/`
   — if AGENTS.md is missing, the agent relies solely on its generic system prompt.

6. **Expected-vs-actual status mismatch (PRE-5/6/7/8)**: The cron task context
   stated all four issues were `in_progress`, but the live API showed PRE-5 and
   PRE-6 as `in_review`, PRE-7 as `blocked`, and PRE-8 as `done`. No mutations
   were needed because the agent had already advanced the pipeline beyond what
   the prompt knew. Lesson: always trust the API response over the task prompt's
   stated statuses. A diff between expected and actual is a signal to inspect,
   not to correct.

7. **Empty pipeline check — all follow-ups already tracked**: After checking all
   17 done issues, every deliverable that needed a next step already had a child
   issue assigned (PRE-8 → PRE-11, PRE-56 → PRE-71, PRE-58 → PRE-72). Zero new
   issues needed. This is the healthy steady state and should be reported as such
   without creating busywork.

8. **Blocked chain resolved at deepest level (PRE-7 → PRE-74 → PRE-76)**: The
   top-level PRE-7 was `blocked`, its child PRE-74 was also `blocked`, but the
   grandchild PRE-76 was `in_progress` with an active heartbeat run. The chain
   was being handled at the actionable leaf, so no intervention was needed at any
   ancestor level. This confirmed the rule: only the deepest non-working issue in
   a dependency chain needs attention.
