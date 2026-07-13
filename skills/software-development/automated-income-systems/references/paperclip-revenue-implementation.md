# Paperclip Revenue Implementation Reference

Verified workflow for building a zero-investment revenue engine using Paperclip + Hermes + Claude Code + OpenCode.

## Architecture Overview

```
Paperclip Server (localhost:3100)          External Builders
├── CEO (b717f92b) ── GitHub Sponsors      ├── Claude Code ── complex builds
├── CMO (1ca47b10) ── Gumroad + Medium     ├── OpenCode ── docs + reviews
├── COO (f202dd71) ── Fiverr + Ops         └── Hermes Agent ── orchestration
├── CFO (763ca49f) ── Financial tracking
├── Engineer (9eed5712) ── Code tools
├── HoP (a3482c7c) ── Product specs
└── QA (efa914be) ── Quality checks
```

## Paperclip Issue API (Verified Working)

### Authentication
```bash
# Cookie jar authentication
COOKIE="C:/one/paperclip-company/cj.txt"
API="http://localhost:3100"
COMPANY_ID="3056c999-62ba-4321-ae69-799a61286bad"
HEADERS="-H \"Origin: http://localhost:3100\" -H \"Content-Type: application/json\""
```

### Create a Revenue Issue
```bash
# Creates a new issue assigned to a specific agent
curl -s --max-time 10 -b "$COOKIE" $HEADERS \
  -X POST "$API/api/companies/$COMPANY_ID/issues" \
  -d '{
    "title":"List 3 products on Gumroad",
    "description":"...",
    "priority":"high",
    "assigneeAgentId":"1ca47b10"
  }'
```

### Assign an Existing Issue to an Agent (triggers execution)
```bash
# Get issue ID first
ISSUE_ID=$(curl -s --max-time 10 -b "$COOKIE" \
  "$API/api/companies/$COMPANY_ID/issues?limit=50" \
  | python -c "import sys,json; data=json.load(sys.stdin); \
    print([i['id'] for i in data if i.get('identifier')=='PRE-52'][0])")

# Assign and set in_progress
curl -s --max-time 10 -b "$COOKIE" $HEADERS \
  -X PATCH "$API/api/issues/$ISSUE_ID" \
  -d '{"assigneeAgentId":"1ca47b10","status":"in_progress"}'
```

### Check All Issues (with identifiers)
```bash
curl -s --max-time 10 -b "$COOKIE" $HEADERS \
  "$API/api/companies/$COMPANY_ID/issues?limit=100" \
  | python -c "import sys,json; data=json.load(sys.stdin); \
    [print(f'{i[\"identifier\"]:8} {i[\"status\"]:12} {i[\"title\"][:50]}') \
    for i in data]"
```

### List All Agents
```bash
curl -s --max-time 10 -b "$COOKIE" $HEADERS \
  "$API/api/companies/$COMPANY_ID/agents" \
  | python -c "import sys,json; [print(f'{a[\"name\"]:22} {a[\"role\"]:20} {a[\"id\"]}') \
    for a in json.load(sys.stdin)]"
```

## Digital Product Categories & Pricing

| Category | Price | Lines | Agent | Target Audience |
|:---------|:-----:|:-----:|:-----:|:----------------|
| Prompt Packs | $9-$19 | 93-1,277 | CMO | Sales/Dev teams |
| Blueprint Kits | $47-$97 | 1,500-2,000 | Claude Code | Indie hackers |
| Ebooks | $19-$29 | 2,000+ | OpenCode | Aspiring entrepreneurs |
| CLI Tools | Free + $29 Pro | ~500 JS | Engineer | Developers |
| Video Templates | $29 each | 278-358 | AVG pipeline | Content creators |

## Revenue Stream Prioritization

```
Priority 1: Gumroad (highest margin, zero listing fee, direct sales)
Priority 2: Fiverr (free to list, 20% fee, recurring orders)
Priority 3: Medium Partner Program (passive, Tier-1 readers best)
Priority 4: GitHub Sponsors (low effort, builds credibility)
Priority 5: NPM Packages (lead gen → Pro upsell)
```

## Revenue Tracking Cron

```bash
# Creates a cron that checks revenue progress every 2h
cronjob (
  action='create',
  name='revenue-engine-pulse',
  schedule='every 2h',
  prompt='Check revenue status, read financial dashboard, check Paperclip board...',
  enabled_toolsets=['terminal','file','web']
)
```

## Tier-1 Country Targeting
- 🇺🇸 USA (primary — best Medium rates, highest avg. order)
- 🇬🇧 UK (secondary)
- 🇨🇦 Canada (secondary)
- 🇦🇺 Australia (secondary)
- 🇩🇪 Germany (European anchor)
- 🇪🇺 Other EU

Price in USD only. INR conversion: $1 ≈ ₹83. Monthly target: ₹5,00,000 ≈ $6,000.

## Build Pattern for Maximum Velocity

1. Create Paperclip issues (one per product) — assign to right agent
2. Dispatch Claude Code/OpenCode as parallel delegate_task for heavy builds
3. Write small products (prompts, guides) directly with write_file
4. Set up platform copy (Gumroad, Fiverr, Medium) as reference files
5. Activate cron for automated revenue tracking
6. Agents continue building via heartbeat cycle
