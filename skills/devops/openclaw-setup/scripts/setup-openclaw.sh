#!/usr/bin/env bash
# setup-openclaw.sh — extract the OpenRouter key (no echo), patch openclaw.json
# with env.OPENROUTER_API_KEY + primary model tencent/hy3:free, verify without
# printing the secret. Run from git-bash on the Windows host.
set -euo pipefail

CFG="$HOME/.openclaw/openclaw.json"
SRC_BAT="/c/one/omniroute/start-omniroute.bat"
KEYFILE="$HOME/.openrouter_key"
MODEL="openrouter/tencent/hy3:free"

# 1) extract key without echoing it
if [ ! -s "$KEYFILE" ]; then
  KEY="$(grep -oP 'OPENROUTER_API_KEY=\K\S+' "$SRC_BAT" | head -1)"
  [ -z "${KEY:-}" ] && { echo "KEY_EXTRACT_FAILED"; exit 1; }
  printf '%s' "$KEY" > "$KEYFILE"
  chmod 600 "$KEYFILE"
else
  KEY="$(cat "$KEYFILE")"
fi
assert_prefix() { [ "${KEY:0:6}" = "sk-or-" ] || { echo "KEY_LOOKS_WRONG"; exit 1; }; }
assert_prefix

# 2) patch config via python (keeps JSON valid, never prints value)
python - "$CFG" "$KEYFILE" "$MODEL" <<'PY'
import json, os, sys
cfg_path, keyfile, model = sys.argv[1], sys.argv[2], sys.argv[3]
key = open(keyfile).read().strip()
assert key.startswith("sk-or-")
cfg = json.load(open(cfg_path)) if os.path.exists(cfg_path) else {}
cfg.setdefault("env", {})["OPENROUTER_API_KEY"] = key
ad = cfg.setdefault("agents", {}).setdefault("defaults", {})
ad["model"] = {"primary": model}
ad.setdefault("models", {})[model] = {}
json.dump(cfg, open(cfg_path, "w"), indent=2)
open(cfg_path, "a").write("\n")
PY

# 3) verify shape only
echo "WROTE $CFG"
echo "env.OPENROUTER_API_KEY -> ***${KEY:0:4}*** (${#KEY} chars)"
echo "agents.defaults.model.primary -> $MODEL"
echo "model in allowlist -> $(python -c "import json;print('openrouter/tencent/hy3:free' in json.load(open('$CFG'))['agents']['defaults'].get('models',{}))")"
echo "DONE"
