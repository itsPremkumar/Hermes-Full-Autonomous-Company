# ClawHub Batch Publishing Reference

## When to batch-publish
Creating 5+ ClawHub skills in one session. Writing each folder manually is slow and
error-prone. A Python generator script handles consistent frontmatter, tags, and tool
file placement.

## Generator template
Write a Python script that imports SKILL_DEFS (list of dicts) and creates all folders:

```python
import os, json

SKILLS_DIR = r"C:\one\paperclip-company\clawhub-skills"

def create_skill(slug, name, description, tags, body):
    sdir = os.path.join(SKILLS_DIR, slug)
    os.makedirs(sdir, exist_ok=True)
    tags_str = json.dumps(tags)
    skill_md = f"""---
name: {slug}
version: 1.0.0
description: {description}
tags: {tags_str}
---
# {name}
{body}
"""
    with open(os.path.join(sdir, "SKILL.md"), "w") as f:
        f.write(skill_md.lstrip())
```

## Content quality rules
Every SKILL.md MUST have these sections to avoid rejection:
1. `## Install` — copy/download instructions, language requirements
2. `## Usage` — 3+ command examples with flags shown
3. `## Features` — bullet list of capabilities
4. `## Commands` — table (| Command | Description |)
5. `## Why` — value proposition (1-2 paragraphs)
6. `## Support` — donation/sponsor links

The registry rejects with: `"Skill content is too thin or templated. Add meaningful,
specific documentation."` A skeleton with just frontmatter + one paragraph will fail.

## Per-skill structure
Each skill folder:
```
clawhub-skills/<slug>/
├── SKILL.md          # REQUIRED — YAML frontmatter + rich documentation
├── <tool>.py         # RECOMMENDED — standalone Python CLI (stdlib preferred)
└── README.md         # OPTIONAL — mirrors SKILL.md for GitHub repo root
```

## Python tool requirements
- **stdlib-only preferred** — zero pip install needed (urllib, json, re, os, sys, math)
- If an external dep is required (e.g. Pillow), make it optional with a clear fallback
- Shebang line: `#!/usr/bin/env python3`
- Docstring includes full usage block
- Compile-check: `python -c "import py_compile; py_compile.compile('file.py')"`
- Verify with `--help` or a dry-run smoke test before publishing

## Publish loop
After generation, publish each skill:

```bash
clawhub publish "C:\one\paperclip-company\clawhub-skills\<slug>" \
  --slug <slug> \
  --name "Display Name" \
  --version 1.0.0 \
  --tags "tag1,tag2,tag3"
```

Success returns: `✔ OK. Published <slug>@1.0.0 (<hash>)`.

## GitHub repo creation (one per skill)
Each ClawHub skill needs its own GitHub repo. Extract the cached GCM token:

```bash
TOKEN=$(echo -e "protocol=https\nhost=github.com" | git credential-manager get | grep "^password=" | cut -d= -f2)

curl -sS -X POST "https://api.github.com/user/repos" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "{\"name\":\"<slug>\",\"description\":\"ClawHub skill: <slug>\",\"private\":false,\"auto_init\":false}"
```

Never echo the token. Verify the repo was created by checking HTTP 200 from
`https://api.github.com/repos/itsPremkumar/<slug>`.

## Push skill code to GitHub repo
After publishing on ClawHub and creating the repo:

```bash
mkdir -p /c/one/clawhub-repos/<slug>
cp -r "/c/one/paperclip-company/clawhub-skills/<slug>/"* "/c/one/clawhub-repos/<slug>/"
cd /c/one/clawhub-repos/<slug>

git init
git checkout -b main
git add -A
git commit -m "Initial commit: <slug> ClawHub skill"
git remote add origin "https://github.com/itsPremkumar/<slug>.git"
git push origin main
```

### Add .gitignore right after first push
The initial commit likely included `__pycache__/*.pyc` bytecode files. Fix:

```bash
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
git rm -r --cached __pycache__/ 2>/dev/null || true
git add .gitignore
git commit -m "Add .gitignore, remove __pycache__"
git push origin main
```

### Clean up temp workspace
```bash
rm -rf /c/one/clawhub-repos
```

## Batch loop (combined workflow)
For N skills, combine all steps:

```python
BATCH = ["slug1", "slug2", "slug3"]
for slug in BATCH:
    create_skill(slug, ...)          # Step 1: generate folder
    publish_to_clawhub(slug, ...)    # Step 2: clawhub publish
    create_github_repo(slug, ...)    # Step 3: curl API
    git_init_and_push(slug)          # Step 4: git init + commit + push
    add_gitignore(slug)              # Step 5: .gitignore cleanup
```

## Delegation for large batches
For 8+ skills, split into subagent (delegate_task) groups of 3-4 skills each.
Each subagent gets:
- The slug, name, description, tags
- The content-quality rules (never thin SKILL.md)
- The generator script approach
- The publish command format
- The Python stdlib tool requirements

Subagents run in parallel, each handling its own publish. Follow up separately
for GitHub repo creation + git push (those require the GCM token, which should
stay in the parent context — do NOT pass the token to subagents).

## Verification
After batch publish, verify a sample:
```bash
clawhub search "<slug>" --limit 3
```

**Critical**: Vector search index may lag by minutes. The publish response
(`✔ OK. Published <slug>@1.0.0`) is authoritative confirmation. Do NOT
retry-publish just because search returns nothing — that creates duplicates.
