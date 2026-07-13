---
name: open-source-stack-blueprint
description: Research, verify, and document open-source project stacks as structured, evidenced blueprints. Use when the user wants to find free/self-hostable tools for a domain, build an "AI company stack", compare OSS alternatives, or produce a department→tool map. Emphasizes LIVE verification (GitHub API) and honest caveats — never fabricate star counts.
---

# Open-Source Stack Blueprint

## When to use
- "find all the free/open-source projects for an AI company"
- "what tools do I need for the X department?"
- "compare OSS alternatives for video generation"
- building a department↔project matrix / compulsory baseline / gap-fillers

## Workflow
1. **Scope first.** Free-only? Self-hostable? Include experimental? Universal (any company) or domain-specific? Start with a 7-agent MVP, not all 60 departments.
2. **Research via GitHub API** — pull live stars + license. Do NOT trust memory for counts.
   Technique + verified knowledge bank: `references/github-api-research.md`.
3. **Verify links** with an HTTP-200 HEAD check on a sample of repos.
4. **Handle rate limits (403).** GitHub unauthenticated API allows ~20 calls/min per IP. When it 403s, STOP hammering, mark unverified repos as `(canonical)` and note "not re-verified this session." NEVER fabricate star counts.
5. **Structure output** as a folder of markdown:
   - `README.md` — master index + tier structure + 7-agent MVP
   - `ENTERPRISE_STACK.md` — consolidated map
   - `COMPULSORY_BASELINE.md` — the default N-project set every company needs (industry-agnostic)
   - `MASTER_INDEX.md` — department↔project matrix (one-glance)
   - `QUICKSTART.md` — concrete first steps (MVP → memory → infra → expand)
   - `departments/NN-topic.md` — one file per department: role, project, ★, license, link, why, integration
   - `departments/XX-gap-fillers.md` — missing functions (legal/eval/translation/scheduling/RPA/vec-DB)
   - `departments/XX-self-evolving-core.md` — if AI-agent company (Hermes + Mem0 + Graphiti + AgentZero)
6. **Honesty discipline (critical):**
   - ✅ = star count verified live this session
   - (canonical) = well-known repo, not re-verified (rate-limited)
   - Flag concept-only projects explicitly (e.g. "Paperclip Maximus — concept only, no production repo")
   - Note experimental/small repos to evaluate (maintenance, docs, issue backlog, license) before production reliance.

## Pitfalls
- Don't deploy all departments at once — ship a 7-agent MVP, prove value, expand.
- Don't claim a tool "works" without testing it (for MCP servers, actually send JSON-RPC — see `mcp-server-verification` skill).
- GitHub API rate limits WILL hit mid-session — research in batches, space calls (sleep 1–1.5s), mark unverified.
- Star count ≠ production-readiness — check maintenance activity, docs, issue backlog, license.
- Keep it $0 software cost: every tool open-source/self-hostable; compute (VPS/GPU) is the only bill.

## References
- `references/github-api-research.md` — curl+python technique, rate-limit handling, verified project knowledge bank.
