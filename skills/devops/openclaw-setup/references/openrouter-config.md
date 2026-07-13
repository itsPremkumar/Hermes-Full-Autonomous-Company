# OpenRouter config for OpenClaw

## Provider discovery
OpenRouter is a **built-in** OpenClaw provider (OpenAI-compatible transport).
No plugin install needed. Two onboarding modes:
- OAuth: `openclaw onboard --auth-choice openrouter-oauth`
- API key: `openclaw onboard --auth-choice openrouter-api-key`

Both default the model to `openrouter/auto`. Pick a concrete model after:
`openclaw models set openrouter/<provider>/<model>`.

## Config schema (openclaw.json)
```json5
{
  "env": { "OPENROUTER_API_KEY": "sk-or-..." },
  "agents": {
    "defaults": {
      "model": { "primary": "openrouter/tencent/hy3:free" },
      "models": { "openrouter/tencent/hy3:free": {} }
    }
  }
}
```

- Model ref pattern: `openrouter/<provider>/<model>`.
- Bundled fallback refs: `openrouter/auto`, `openrouter/moonshotai/kimi-k2.6`,
  `openrouter/moonshotai/kimi-k2.5`. Any other `openrouter/<provider>/<model>`
  resolves dynamically against OpenRouter's live catalog.
- `agents.defaults.models` acts as an **allowlist** when set — include the model
  or OpenClaw may reject it.
- Optional image model: `agents.defaults.imageGenerationModel.primary =
  "openrouter/google/gemini-3.1-flash-image-preview"`.

## The user's OpenRouter key location
NOT in shell env. Lives in `C:\one\omniroute\start-omniroute.bat`:
```
set OPENROUTER_API_KEY=sk-or-...
```
(73 chars, prefix `sk-or-v`).

## Key extraction (NEVER print the secret)
```bash
KEY=$(grep -oP 'OPENROUTER_API_KEY=\K\S+' /c/one/omniroute/start-omniroute.bat | head -1)
printf '%s' "$KEY" > ~/.openrouter_key
chmod 600 ~/.openrouter_key
# verify only shape, never value
echo "len=${#KEY} prefix=${KEY:0:7}"
```

## Free model caveat — tencent/hy3:free
- Alias resolves to `tencent/hy3-20260706:free` (provider: Novita).
- It is a **reasoning model**: at low `max_tokens` it returns empty `content`
  (all budget spent on the `reasoning` field, `finish_reason: length`).
  Always request `max_tokens: ~200` for real output.
- The `/api/v1/models/tencent/hy3:free` catalog endpoint returns 404; the
  chat-completions endpoint works fine. Test via chat, not the model-alias GET.
