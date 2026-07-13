# Project Maturity Levels

Every internal project carries a maturity level. The autonomy loop reads this to decide
what may change automatically vs. what needs human sign-off.

```
Idea → Research → Prototype → MVP → Production → Stable → Maintenance → Archived
```

| Level | Meaning | Autonomy allowed |
|---|---|---|
| Idea / Research | Not built / investigating | Agent may research + draft only |
| Prototype | Rough, untested | Agent may build; no publish |
| MVP | Works for first user | Agent may iterate; human approves publish |
| Production | Live, real users/revenue | Agent maintains; human approves changes to price/scope |
| Stable | Proven, low churn | Agent maintains autonomously within budget |
| Maintenance | Sunset pending | Agent fixes only; no new features |
| Archived | Retired | Read-only; kept for knowledge (never deleted) |

## Current levels
- 8 digital products: **MVP** (built, not yet published — Gumroad publish = human, PRE-52)
- income-engine: **Production** (generates the products)
- autonomy-loop: **MVP** (running every 30m)
- CONSTITUTION / prompts: **Stable**
- Automated-Video-Generator: **Production** (separate repo)
