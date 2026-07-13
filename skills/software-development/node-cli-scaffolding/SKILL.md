---
name: node-cli-scaffolding
description: Scaffold and ship a production-grade Node.js CLI tool — ESM package, interactive prompts, config generation, npm distribution, free/pro tier structure. Covers bin entry setup, inquirer-based interactive flows, JSDoc-typed config builders, save-to-file output, and premium upgrade navigation.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
---

# Node.js CLI Scaffolding

End-to-end recipe for building a **Node.js CLI tool** packaged for npm distribution with interactive prompts, generated output, and optional free/pro tier separation. Use for: config generators, scaffolding tools, interactive wizards, utility CLIs that produce structured output.

## When to use

- A user asks to build a "CLI tool", "interactive generator", "wizard", or "scaffolder"
- Starting a new Node.js executable package from scratch
- Adding interactive prompts (inquirer) to an existing script
- Packaging a dev tool for npm with a `bin` entry

## Scaffold structure

```
agent-config-generator/
├── src/
│   └── index.js          # CLI entry (shebang + ESM)
├── pro/                   # Premium / paid-tier assets
│   └── company-template.json
├── package.json           # name, bin, type: module, deps
├── README.md              # Professional docs
└── .gitignore
```

## Step-by-step

### 1. Package setup (`package.json`)

- `"type": "module"` — ESM across the board.
- `"bin": { "<command-name>": "./src/index.js" }` — single bin entry.
- `"files": ["src/", "README.md", "LICENSE"]` — whitelist what ships to npm.
- `"engines": { "node": ">=18.0.0" }` — inquirer 12+ requires node 18.
- `"scripts"`: `"start"`, `"dev": "node --watch src/index.js"`, `"test"`, `"prepublishOnly"`.

### 2. Entry point (`src/index.js`)

```
#!/usr/bin/env node
import inquirer from 'inquirer';
```

- **Shebang** `#!/usr/bin/env node` is critical for the `bin` to work on Unix.
- **ESM** — use `import`, not `require`. Inquirer 12+ is ESM-only.
- **Imports** node built-in modules: `import { writeFile } from 'node:fs/promises'`.
- **JSDoc** type the config schema with `@typedef` so the code is self-documenting.

### 3. Banner

Print a box banner at startup with the tool name, version, and tagline. Uses `console.log` and `String.padEnd` for alignment.

```js
function printBanner() {
  console.log('');
  console.log('╔═══════════════════════════════════════════════════════════╗');
  console.log('║          Agent Config Generator  v' + VERSION.padEnd(38) + '║');
  console.log('╚═══════════════════════════════════════════════════════════╝');
  console.log('');
}
```

### 4. Interactive prompts (inquirer)

**Pattern for each prompt:**

```js
{
  type: 'list',       // 'list', 'checkbox', 'confirm', 'input'
  name: 'fieldName',
  message: 'Prompt text?',
  description: 'Helpful subtitle',
  choices: [...],
  default: 'default_value',
  when: (answers) => answers.prevField === 'xyz',  // conditional
  validate: (input) => input.length > 0 || 'Error message',
}
```

- **List choices** — always set `loop: false` so arrow-up at the first item doesn't jump to the bottom.
- **Checkbox** — `validate: (input) => input.length > 0 || 'Select at least one'`.
- **Conditional prompts** — use `when` to show a custom input only when `custom` is selected.
- **Error handling** — catch `ExitPromptError` (inquirer 12+ throws this on Ctrl+C):

```js
try {
  const answers = await runPrompts();
  // ... handle answers
} catch (err) {
  if (err instanceof Error && err.name === 'ExitPromptError') {
    console.log('\n  Cancelled.\n');
    process.exit(0);
  }
  die(String(err));
}
```

### 5. Config builder

Separate the logic from presentation. After collecting answers:

```js
function buildConfig(answers) {
  const model = answers.model === '__custom__' ? answers.customModel : answers.model;
  return {
    name: 'Paperclip Engineer',
    adapterType: 'hermes_local',
    role: answers.agentRole,
    adapterConfig: { model, provider, ... },
  };
}
```

- Resolve custom/fallback values before building.
- **JSDoc** the return type with `@typedef` and `@returns`.

### 6. Output (print / save / both)

After generating, let the user choose:

```js
{ type: 'list', name: 'action', message: 'What to do?',
  choices: [
    { name: '📋  Print to console', value: 'print' },
    { name: '💾  Save to file', value: 'save' },
    { name: '📋 + 💾  Both', value: 'both' },
  ],
}
```

- **Save** — use `path.resolve(path)` then `writeFile(resolved, json + '\n', 'utf-8')`.
- **mkdirp** — `mkdirSync(dir, { recursive: true })` before writing.
- **Handle errors** — wrap in try/catch with `die()`.

### 7. Premium / PRO tier

The free version generates single outputs. The PRO tier lives in a separate `pro/` directory with multi-agent or orchestration configs. Reference it in an upsell banner after output.

```js
function showPremiumUpsell() {
  console.log('🚀 Need multi-agent orchestration?');
  console.log('PRO version ($29) generates a complete company config...');
}
```

### 8. CLI flags

```js
if (flag === '--help' || flag === '-h') { printHelp(); return; }
if (flag === '--version' || flag === '-v') { console.log(VERSION); return; }
```

### 9. Professional README

A README for an npm-published CLI tool should include:

- Badges (npm version, license, node version)
- Overview paragraph — what problem it solves
- Installation (`npm install -g` / `npx`)
- Interactive usage screenshots (block-art simulating terminal output)
- Table of the prompts/questions
- Output example (JSON block)
- Premium upsell section with link
- API reference table
- Development instructions (clone, install, dev)

## Error-handling patterns

| Situation | Pattern |
|-----------|---------|
| User hits Ctrl+C | Catch `ExitPromptError`, exit gracefully |
| File write fails | Wrap in try/catch, call `die(msg)` |
| Invalid input | `validate` function returns error string |
| Missing/invalid CLI args | `--help` shows usage |

## Windows path pitfall (MSYS / git-bash)

When running on Windows under MSYS (git-bash), the `terminal` tool translates `/c/...` to `C:\...`, but `write_file`/`patch` resolve paths relative to the Hermes workspace (`C:\Users\<user>`). Consequently, passing `/c/one/project/file` to `write_file` lands at `C:\c\one\project\file` — not the intended `C:\one\project\file`.

**Fix:** Use `terminal` for file operations on paths under `/c/...`, `C:\...`, etc. OR pass native Windows paths to `write_file`/`patch`. If files already landed in the wrong place, `cp` them from `C:\c\...` to `C:\...` via `terminal`.

## Verification (after "done")

Before claiming done:
1. `node src/index.js --version` — prints version.
2. `node src/index.js --help` — prints usage.
3. `node -e "require('./package.json')"` — valid package.json.
4. Config builder logic — unit-test the output shape matches expectations.
5. Premium template (if any) — `JSON.parse(fs.readFileSync('pro/...'))` — valid JSON.

## npm publish checklist

- [ ] `package.json`: `name`, `version`, `bin`, `files`, `repository`, `license` all set
- [ ] `npm pack --dry-run` — verify only intended files are shipped
- [ ] README badges point to real npm and GitHub URLs
- [ ] LICENSE file present (MIT recommended)
- [ ] Run `npm test` — green
- [ ] `npm publish` — or `npm publish --access public` for scoped packages
