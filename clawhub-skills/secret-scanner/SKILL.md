---
name: secret-scanner
version: 1.0.0
description: >-
  Scan files and directories for 27 types of leaked secrets, API keys, tokens,
  credentials, and private keys using regex and Shannon entropy analysis.
  Fully offline, Python stdlib only — zero dependencies.
tags: [security, secrets, scan, devtools, python, credential-detection]
---

# Secret Scanner 🔍

**Detect leaked secrets before attackers do.** Secret Scanner is a lightweight,
offline CLI tool that recursively scans files and directories for 27 different
types of credentials, tokens, API keys, private keys, and connection strings —
plus high-entropy strings that look like unknown tokens.

Built with **zero external dependencies** (Python stdlib only: `re` + `math`).
Runs anywhere Python 3.8+ runs. No telemetry, no network calls, no data leaves
your machine.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **27 regex patterns** | Covers AWS, GitHub, OpenAI, Stripe, JWT, SSH keys, Slack, Google, Discord, Telegram, GitLab, MongoDB, Twilio, Facebook, Azure, Heroku, Twitter, and more |
| **Entropy-based detection** | Shannon entropy analysis catches unknown or custom token formats that regex misses |
| **Recursive directory scan** | Walks entire directory trees, skipping `.git/`, `node_modules/`, binaries, and other noise |
| **Test-fixture filtering** | Smart heuristic skips `example`, `placeholder`, `test-`, and similar false-positive tokens |
| **Severity rating** | Every finding graded: `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW` |
| **Redacted output** | Secrets are shown as `abcd****wxyz` in reports — safe for CI logs |
| **JSON output** | Machine-readable output (`--json`) for pipeline integration |
| **Exit codes** | Non-zero exit when critical secrets found — CI/commit-hook ready |
| **Offline & air-gapped** | Zero network calls. Works in disconnected environments |
| **Python stdlib only** | No pip install, no dependencies, no npm, no containers |

---

## 📦 Install

```bash
# Copy the script anywhere — zero dependencies!
cp secret_scanner.py /usr/local/bin/secret-scanner
chmod +x /usr/local/bin/secret-scanner

# Or run directly from the cloned repo
cd clawhub-skills/secret-scanner/
python secret_scanner.py --help
```

**Requires:** Python 3.8+

---

## 🚀 Usage

```bash
python secret_scanner.py <command> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `scan <file-or-dir>` | Recursively scan a file or entire directory tree |
| `check <file>` | Deep-scan a single file with detailed context |
| `list-patterns` | Display all 27 detection patterns with severity levels |

### Options

| Flag | Applies to | Description |
|------|-----------|-------------|
| `--json` | `scan` | Output results as JSON array (pipe-friendly) |
| `--version` | all | Print version and exit |

---

## 📋 Examples

### Scan an entire project directory

```bash
python secret_scanner.py scan ~/projects/my-app/
```

### Check a single config file

```bash
python secret_scanner.py check config/settings.env
```

### Machine-readable output for CI pipelines

```bash
python secret_scanner.py scan ./src --json > report.json
```

### Scan and fail CI on any critical finding

```bash
python secret_scanner.py scan ./src/ || echo "!! Secrets detected !!"
```

### List all detectable patterns

```bash
python secret_scanner.py list-patterns
```

---

## 🎯 Detected Patterns (27 regex rules)

| # | Pattern ID | What It Detects | Severity |
|---|-----------|-----------------|----------|
| 1 | `aws-access-key` | AWS Access Key ID (`AKIA...`) | HIGH |
| 2 | `aws-secret-key` | AWS Secret Access Key (40-char base64) | CRITICAL |
| 3 | `github-pat` | GitHub PAT (`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghf_`) | CRITICAL |
| 4 | `openai-key` | OpenAI API Key (`sk-...`) | CRITICAL |
| 5 | `slack-bot-token` | Slack Bot/App/User token (`xoxb-`, `xoxp-`, etc.) | HIGH |
| 6 | `google-api-key` | Google API Key (`AIza...`) | HIGH |
| 7 | `google-oauth` | Google OAuth token (`ya29.`) | HIGH |
| 8 | `jwt` | JSON Web Token (`eyJ...`) | CRITICAL |
| 9 | `ssh-private-key` | SSH Private Key block (`-----BEGIN ... PRIVATE KEY-----`) | CRITICAL |
| 10 | `pgp-private-key` | PGP Private Key block | CRITICAL |
| 11 | `password-in-url` | Password/credentials in URL | HIGH |
| 12 | `twitter-bearer` | Twitter/X Bearer Token | HIGH |
| 13 | `heroku-api-key` | Heroku API Key | HIGH |
| 14 | `discord-bot-token` | Discord Bot Token | HIGH |
| 15 | `telegram-bot-token` | Telegram Bot Token | HIGH |
| 16 | `gitlab-pat` | GitLab Personal Access Token (`glpat-`) | HIGH |
| 17 | `mongodb-connection-string` | MongoDB connection string with credentials | CRITICAL |
| 18 | `stripe-key` | Stripe API Key (`sk_live_`, `pk_live_`) | CRITICAL |
| 19 | `twilio-key` | Twilio API Key / SID | HIGH |
| 20 | `facebook-access-token` | Facebook Access Token | HIGH |
| 21 | `slack-webhook` | Slack Webhook URL | HIGH |
| 22 | `azure-connection-string` | Azure / SQL connection string with credentials | HIGH |
| 23 | `generic-private-key` | Generic private key block | CRITICAL |
| 24 | `generic-api-key-env` | Generic env-var-style API keys (`API_KEY=...`) | MEDIUM |
| 25 | `private-key-file-ref` | Embedded public/private key material | MEDIUM |
| 26 | `auth-header-basic` | Basic Auth / Bearer / Token headers | MEDIUM |
| 27 | `generic-password` | Generic password assignment (`password="..."`) | MEDIUM |

**Plus:** High-entropy string detection catches anything that looks like a
token but doesn't match known formats — ideal for proprietary or lesser-known
SaaS platforms.

---

## 🧠 Entropy Detection

Secret Scanner calculates **Shannon entropy** on extracted strings to spot
high-entropy tokens that don't match a known pattern. This catches:

- Custom/internal API keys
- Tokens for lesser-known services
- Randomly-generated secrets in proprietary formats

Threshold: **entropy ≥ 4.5** (tuned to flag random-looking strings while
ignoring UUIDs, hex hashes, and numeric IDs).

---

## 🔬 How It Works

1. **Recursive walk** — traverses the directory tree, skipping `.git/`,
   `node_modules/`, binary files, and other noise.
2. **Regex matching** — runs each of the 27 compiled patterns against every
   line of every text file.
3. **False-positive filtering** — discards matches in lines containing
   `example`, `placeholder`, `test_`, `changeme`, etc.
4. **Entropy check** — extracts potential token strings and computes Shannon
   entropy, flagging anything above 4.5 that wasn't already caught.
5. **Reporting** — groups findings by file, shows redacted matches, severity
   coloring, and optional JSON output.

---

## ⚙️ Configuration & Customization

You can easily extend the pattern list by editing the `PATTERNS` list in
`secret_scanner.py`. Each pattern is a dict:

```python
{
    "id": "my-custom-key",
    "name": "My SaaS API Key",
    "severity": "high",
    "regex": re.compile(r"myapp-[A-Za-z0-9]{32}"),
}
```

The entropy threshold can be adjusted by changing `HIGH_ENTROPY_THRESHOLD`
at the top of the script (default: `4.5`).

---

## 🧪 Exit Codes

| Code | Meaning |
|------|---------|
| `0` | No secrets found — clean! |
| `1` | Usage error or path not found |
| `2` | Secrets found (one or more `CRITICAL` findings) |

CI systems can simply check `$?` — any non-zero after `scan` means
something needs attention.

---

## ❓ Why Secret Scanner?

There are many secret scanners out there (truffleHog, Gitleaks, detect-secrets),
but they all require **npm install**, **pip install**, or **Docker pull**.
Secret Scanner is:

- **Zero dependencies** — copy one file and run
- **Zero network** — works in air-gapped environments
- **Zero telemetry** — no phone-home, no analytics
- **Instant setup** — no config files, no databases, no plugins
- **5KB** — smaller than this README

Use it as a **pre-commit hook**, a **CI gate**, or a **one-off audit tool**.

---

## 🔗 Related

- [ClawHub Registry](https://github.com/itsPremkumar/clawhub) — find more skills
- [Paperclip](https://github.com/paperclipai/paperclip) — agent collaboration platform

---

## 📄 License

MIT — free to use, modify, and distribute.
