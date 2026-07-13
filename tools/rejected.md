# Rejected / Not-Used Tools

Tools referenced by earlier prompt drafts but NOT adopted — kept so we don't re-test dead ends.

| Tool | Why rejected / not used |
|---|---|
| n8n | Not installed; not needed — Paperclip + cron + scripts cover our automation. Avoids RAM cost on this low-memory machine. |
| Mem0 | Not installed; GitHub knowledge base + Hermes session memory cover memory. Skip to save RAM. |
| CrewAI / AutoGen | Not used; Paperclip's multi-agent orchestration replaces them. One less heavy Python dep. |
| OpenHands | Not installed; Hermes delegates coding to Claude Code / Codex / Gemini CLI adapters instead. |
| Standalone "OmniRouter" (omnilabs-ai/OmniRouter) | Smaller, less-established than OpenRouter. We use OmniRoute→OpenRouter. Re-evaluate only if OpenRouter free tiers dry up. |
| "Claude Fable 5 leaked system prompts" | Unverified / frequently fabricated content. Constitution §7 forbids building on unverified leaked prompts; prefer officially published guidance. |
| Playwright / Browser Use (as separate stack) | OpenClaw already provides browser/computer-use coverage; no need for a parallel browser-automation install. |
