# Reusable audit-trace recipe

Run from the project root. Prints every vulnerable package with severity,
advisory titles, whether it's a DIRECT dep, and whether a fix exists.

```bash
npm audit --omit=dev --json | python -c "
import json,sys
d=json.load(sys.stdin)
v=d.get('vulnerabilities',{})
for name,info in v.items():
    sev=info.get('severity')
    titles=[x.get('title') for x in info.get('via',[]) if isinstance(x,dict)]
    print(f'{sev.upper():>8}  {name}')
    for t in titles: print('        -', t)
    print('        direct:', info.get('isDirect'), '| fixAvailable:', bool(info.get('fixAvailable')))
"
```

## Full verification bundle (run after any dep change)

```bash
npm audit --omit=dev 2>&1 | tail -1        # found 0 vulnerabilities
npm run typecheck                          # clean
npm run test:unit 2>&1 | grep -E '^# (tests|pass|fail)'
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))" && echo "ci.yml OK"
```

## Find what a removed dep leaves behind

```bash
grep -rni "gtts" src --include=*.ts        # replace 'gtts' with the removed symbol
npm ls <vuln-pkg>                          # trace a transitive vuln to its direct parent
```
