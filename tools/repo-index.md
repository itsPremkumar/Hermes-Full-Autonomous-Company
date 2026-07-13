# Repository Index

A searchable catalog of repositories this company depends on. More useful than bookmarks.
Keep integration status current. Add new repos via the §4 validation gate.

| Repo | Purpose | License | Maintenance | Integration | Owner | Notes |
|---|---|---|---|---|---|---|
| itsPremkumar/Hermes-Full-Autonomous-Company | **This OS** — single source of truth | MIT | active | core | itsPremkumar | CONSTITUTION lives here |
| itsPremkumar/Hermes-Prompt-Library | Versioned prompts (mirror of /prompts) | MIT | active | core | itsPremkumar | archive/ holds superseded |
| itsPremkumar/Automated-Video-Generator | Remotion video product line (AVG) | MIT | active | product | itsPremkumar | PRs PRE-14..16 |
| paperclipai/paperclip | The company runtime (org/budgets/ticketing) | OSS | active | runtime | Paperclip | embedded Postgres; not forked into this repo |
| hermes-agent (Nous) | Executive agent | OSS | active | runtime | Nous | hermes_local/gateway |
| openclaw | Comms + computer-use | OSS | active | runtime | OpenClaw | gateway :18789 |

## Rule
Before depending on a NEW repo: search GitHub, compare ≥3 mature solutions (§"Never
Reinvent"), validate (§4), then add a row here with integration status. Deprecated repos
stay listed (struck-through) for traceability — never silently dropped.
