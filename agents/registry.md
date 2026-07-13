# Agent Registry (standard interface)

Every agent follows this schema so it can be swapped without rewriting the OS. Add an
entry per agent. Status: active | standby | deprecated.

## Hermes (Executive)
- Version: local (Hermes Agent, Nous)
- Capabilities: executive reasoning, planning, documentation, coordination, GitHub ops
- Dependencies: Paperclip API, git CLI, OpenRouter (escalation)
- Memory: SQLite/FTS5 session + GitHub
- Tools: terminal, file, browser, delegate, cron, skill
- API: hermes_local / hermes_gateway adapter
- Status: active

## OpenClaw (Comms & Computer-Use)
- Version: openclaw@2026.6.11
- Capabilities: browser automation, GUI/desktop use, messaging, Telegram
- Dependencies: Paperclip API, gateway :18789
- Memory: its own config + GitHub
- Tools: computer_use, browser, messaging
- API: openclaw_gateway adapter
- Status: active

## Coding Agents (Engineering)
- Version: Claude Code / Codex / Gemini CLI (built-in adapters)
- Capabilities: code generation, refactors, GitHub workflows, tests
- Dependencies: Paperclip API, model routing
- Memory: repo context + GitHub
- Tools: terminal, file, git
- API: built-in Paperclip adapters
- Status: active

## To add a new agent
Copy this schema, fill it, place under agents/<name>/AGENTS.md, register here, and run
the §4 validation gate. If a better agent appears, mark old = deprecated (archive, don't
delete) per CONSTITUTION §4.3.
