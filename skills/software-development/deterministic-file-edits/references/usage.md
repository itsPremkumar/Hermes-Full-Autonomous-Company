# Usage — deterministic exact replace

## Step-by-step
1. Identify the exact old string. If it contains backslashes, dump char codes first
   (see byte-inspect snippet) so you know how many backslashes are actually in the file.
2. Write `replace.json`:
   ```json
   { "path": "src/lib/script-parser.ts",
     "from": "[^\\\\[]*\\\\]",
     "to":   "[^[]*\\\\]" }
   ```
   JSON escaping reminder: in JSON, `\\` is ONE backslash. So `"\\\\["` = two
   backslashes + `[`; `"\\["` = one backslash + `[`.
3. Run: `node scripts/exact-replace.cjs replace.json`
4. `read_file` the lines to confirm, then run typecheck/test/lint.

## Byte-inspect when escaping is confusing
```js
const fs = require('fs');
const line = fs.readFileSync('src/lib/script-parser.ts', 'utf8').split('\n')[70];
for (let i = 0; i < line.length; i++) {
    if (line[i] === '\\') console.log(i, 'BACKSLASH');
}
console.log(JSON.stringify(line));
```
Rule: `JSON.stringify` doubles backslashes. Output `\\\\s` = two backslashes in file;
output `\\s` = one backslash in file.

## Why not `sed` / `patch` here
- `sed` in MSYS mangles backslashes.
- `patch` fuzzy matcher silently no-ops on regex/escaped content (reports success,
  applies nothing). Node `split/join` is exact and verifiable.
