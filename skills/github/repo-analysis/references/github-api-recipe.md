# GitHub API recipe (Phase 1 — no clone needed)

Run in `bash`. Note: use `python` not `python3` if `python3` is missing.

```bash
REPO="itsPremkumar/Automated-Video-Generator"   # owner/name

# 1. Repo metadata
curl -sL "https://api.github.com/repos/$REPO" > repo.json
python -c "
import json
d=json.load(open('repo.json'))
print('Name      :', d.get('full_name'))
print('Desc      :', d.get('description'))
print('Lang      :', d.get('language'))
print('Stars     :', d.get('stargazers_count'))
print('Forks     :', d.get('forks_count'))
print('Created   :', d.get('created_at'))
print('Updated   :', d.get('updated_at'))
print('Size KB   :', d.get('size'))
print('OpenIssues:', d.get('open_issues_count'))
print('License   :', (d.get('license') or {}).get('spdx_id'))
print('Topics    :', d.get('topics'))
print('Archived  :', d.get('archived'))
print('Homepage  :', d.get('homepage'))
"

# 2. Full recursive file tree (sizes + paths) — great for spotting big binaries
curl -sL "https://api.github.com/repos/$REPO/git/trees/HEAD?recursive=1" > tree.json
python -c "
import json
d=json.load(open('tree.json'))
for t in d.get('tree', []):
    if t['type']=='blob':
        print(f\"{t['size']:>8}  {t['path']}\")
"

# 3. Language byte breakdown
curl -sL "https://api.github.com/repos/$REPO/languages" > langs.json
python -c "
import json
d=json.load(open('langs.json'))
tot=sum(d.values())
for k,v in sorted(d.items(), key=lambda x:-x[1]):
    print(f'{k:<16} {v:>10}  {100*v/tot:.1f}%')
"

# 4. Commit history + contributor counts (single page of 100)
curl -sL "https://api.github.com/repos/$REPO/commits?per_page=100" > commits.json
python -c "
import json
d=json.load(open('commits.json'))
print('Commits on page:', len(d))
print('Latest:', d[0]['commit']['message'].split(chr(10))[0], '|', d[0]['commit']['author']['date'])
a={}
for c in d:
    n=c['commit']['author']['name']; a[n]=a.get(n,0)+1
print('Contributors:', a)
"

# 5. Read key human-readable files by raw URL (no clone)
for f in README.md package.json AGENTS.md CHANGELOG.md; do
  curl -sL "https://raw.githubusercontent.com/$REPO/main/$f" -o "$f"
done
"
