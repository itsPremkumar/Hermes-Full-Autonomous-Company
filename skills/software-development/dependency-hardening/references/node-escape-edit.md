# Fixing regex/backslash edits when `patch` silently no-ops

## Symptom
`patch` reports success but the file is unchanged after re-read. Almost always
happens when the old/new string contains backslash escapes (`\\s`, `\\[`,
`\\d`, regex literals with `\\`).

## Why
The fuzzy matcher in the `patch` tool mishandles escaped backslashes and the
edit silently fails. Repeating the same `patch` call loops forever with "success".

## Reliable fix — node script via terminal
Write a `.cjs` file and run it with `node`. Node string handling is exact.

### Replace literal `\\s` (two chars) -> `\s` (one char) in source
In a TS *regex literal* source, a single backslash is one char. To turn a broken
double-backslash `\\s` (literal `\s` text) into correct `\s` (whitespace):
```js
const fs = require('fs');
const p = 'C:/path/to/file.ts';
let s = fs.readFileSync(p, 'utf8');
s = s.split('\\\\s').join('\\s');   // each '\\' in JS source == one backslash
fs.writeFileSync(p, s);
```
Verify byte-content first with a char-dump if unsure:
```js
const line = fs.readFileSync(p,'utf8').split('\n')[70];
for (let i=0;i<line.length;i++) if (line[i]==='\\') console.log(i,'BACKSLASH');
```

### Character-class escape fix (`[^\[]` -> `[^[]`)
```js
const fs = require('fs');
const p = 'C:/path/to/file.ts';
let s = fs.readFileSync(p, 'utf8');
s = s.replace(/\[\^\\\[/g, '[^[');   // [^\[  ->  [^[
fs.writeFileSync(p, s);
```

## Notes
- `execute_code` is BLOCKED under cron mode — do NOT use it for file edits.
- Use **native Windows paths** (`C:\one\...`) in the script, not MSYS `/c/one/...`
  (the `terminal` tool runs git-bash but node resolves `C:\` fine).
- Always clean up the temp `.cjs` after (`rm -f C:/one/fix-*.cjs`).
- After the edit, verify with the actual linter/typecheck, not just re-read.
