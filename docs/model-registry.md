# Model Capability Registry

The orchestrator routes each task to the best-fit model/agent. This is the explicit map
(CONSTITUTION §5). "Local" = default; escalate only when the task needs it.

| Actor | Best at | Default for | Escalate when |
|---|---|---|---|
| Hermes (local) | Executive reasoning, planning, documentation, coordination | Routine ops, drafts, scheduling | Needs stronger reasoning |
| OpenRouter free tier (hy3/others) | General + reasoning via OmniRoute | Coding/reasoning spikes | Free quota exhausted |
| OpenClaw | Computer-use, browser/GUI automation, messaging | Any GUI/desktop task | — |
| Claude Code / Codex / Gemini CLI | Engineering, GitHub workflows | Code generation, refactors | — |
| (future) Qwen / DeepSeek | Local coding | Cheap code tasks | If local model insufficient |

## Routing rule
1. Start local. 2. If confidence < 75% or task is code-heavy/vision → escalate per table.
3. Log the chosen actor + token cost in knowledge-base/benchmarks.md so routing improves over time.
4. Never hardcode a single model as the only path — the OS is model-agnostic (CONSTITUTION §2).

## Zero-cost free providers (no paid key)

The full, detailed catalog of **completely free AI providers/models** that cost $0 (no paid API key,
no credit card) lives in **[docs/free-ai-providers.md](./free-ai-providers.md)**. It documents:
- **Tier A** — truly anonymous / no sign-up (Pollinations, Puter, GLM-CN, OpenCode Zen, Kilo-gateway free, SiliconFlow, Tencent, Baidu).
- **Tier B** — keyless but requires a host login/cookie (Antigravity, Qwen-web, Muse, DuckDuckGo, Blackbox, OpenCode).
- Both **with OmniRoute** (single endpoint) and **without OmniRoute** (direct per-provider) usage paths.
- The golden rule: **always re-check the latest OmniRoute catalog + each provider's latest official docs** before shipping, since free tiers change constantly.

Route high-volume / non-critical traffic through Tier-A providers to keep the company's inference cost at $0.
