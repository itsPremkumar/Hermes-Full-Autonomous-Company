# Paperclip Issue Automation API

Reference for programmatic issue management on a running Paperclip instance. Verified on a Paperclip server at `localhost:3100` with 7 Hermes agents.

## Key Endpoints

### Authentication
```bash
COOKIE="C:/path/to/cj.txt"
API="http://localhost:3100"
HEADERS='-H "Origin: http://localhost:3100" -H "Content-Type: application/json"'
```

### Get All Issues
```bash
curl -s --max-time 10 -b "$COOKIE" \
  "$API/api/companies/<COMPANY_ID>/issues?limit=100" \
  | python -c "import sys,json; d=json.load(sys.stdin); d=d if isinstance(d,list) else d.get('issues',d); [print(f'{i[\"identifier\"]:8} {i[\"status\"]:12} {i[\"title\"][:50]}') for i in d]"
```

### Create a New Issue (and assign to agent)
```bash
curl -s --max-time 10 -b "$COOKIE" $HEADERS \
  -X POST "$API/api/companies/<COMPANY_ID>/issues" \
  -d '{"title":"Issue title","description":"Detailed description","priority":"high","assigneeAgentId":"<AGENT_ID>"}'
```

### Assign Issue to Agent (triggers autonomous execution)
```bash
# Find issue ID by identifier
ISSUE_ID=$(curl -s --max-time 8 -b "$COOKIE" \
  "$API/api/companies/<COMPANY_ID>/issues?limit=50" \
  | python -c "import sys,json; d=json.load(sys.stdin); d=d if isinstance(d,list) else d.get('issues',d); print([i['id'] for i in d if i.get('identifier')=='<PRE-N>'][0])")

# Assign and set status to in_progress
curl -s --max-time 10 -b "$COOKIE" $HEADERS \
  -X PATCH "$API/api/issues/$ISSUE_ID" \
  -d '{"assigneeAgentId":"<AGENT_ID>","status":"in_progress"}'
```

### List All Agents with IDs
```bash
curl -s --max-time 8 -b "$COOKIE" $HEADERS \
  "$API/api/companies/<COMPANY_ID>/agents" \
  | python -c "import sys,json; [print(f'{a[\"name\"]:22} {a[\"role\"]:20} {a[\"id\"]}') for a in json.load(sys.stdin)]"
```

## Known Agent IDs Reference

| Agent Name | Role | ID |
|:-----------|:-----|:---|
| CEO | Strategy/Leadership | b717f92b |
| CMO | Marketing & Content | 1ca47b10 |
| Chief of Operations | Ops & Delivery | f202dd71 |
| CFO | Finance & Tracking | 763ca49f |
| Lead Engineer / CTO | Code & Development | 9eed5712 |
| Head of Product | Product Specs & Design | a3482c7c |
| QA / Tester | Quality Assurance | efa914be |
| Reflection Coach | Paused (optional) | 2cefce47 |

## Key: Agents Do NOT Self-Assign

Paperclip agents work on a heartbeat cycle. They check their open issues on each beat. However, they don't automatically pick up backlog items — you must explicitly assign via the API PATCH endpoint with `assigneeAgentId` to trigger autonomous execution. Once assigned with `status: "in_progress"`, the agent picks it up on its next heartbeat (usually within 30-60 seconds).

## Batch Assignment Pattern (Sprint Launch)

```bash
curl -s --max-time 10 -b "$COOKIE" "$API/api/companies/<COMPANY_ID>/issues?limit=50" | \
python -c "
import sys,json
d = json.load(sys.stdin)
d = d if isinstance(d,list) else d.get('issues',d)
issues = [i for i in d if i.get('identifier','').startswith('PRE-5')]
for i in issues:
    print(i['id'], i['identifier'], i.get('assigneeAgentId','none'))
"
```

## Troubleshooting

| Symptom | Cause | Fix |
|:--------|:------|:-----|
| curl timeout | Server busy/low memory | Use `--max-time 15` |
| "empty" response | Wrong company ID or no cookie | Check COMPANY_ID from web UI URL bar |
| Issue created but agent does nothing | Not assigned | Use PATCH to set assigneeAgentId + status:in_progress |
| "null" agent IDs | Response JSON shape varies | Always handle `isinstance(d,list)` check |
