/**
 * Deterministic exact-string replacer.
 * Usage:  node exact-replace.cjs replace.json
 *
 * replace.json shape:
 *   { "path": "src/lib/x.ts", "from": "<exact old>", "to": "<exact new>" }
 *
 * Backslash content: write `from`/`to` with JSON escaping (JSON "\\" == one backslash).
 * Example file to turn `\\s` (two chars) into `\s` (one char) in source:
 *   { "path": "src/lib/x.ts", "from": "\\\\s", "to": "\\s" }
 * (In JSON, "\\\\s" is two backslashes + s; "\\s" is one backslash + s.)
 */
const fs = require('fs');

const cfgPath = process.argv[2];
if (!cfgPath) {
    console.error('Usage: node exact-replace.cjs <replace.json>');
    process.exit(1);
}

const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
if (!cfg.path || cfg.from === undefined || cfg.to === undefined) {
    console.error('replace.json must have: path, from, to');
    process.exit(1);
}

let s = fs.readFileSync(cfg.path, 'utf8');

if (!s.includes(cfg.from)) {
    const probe = cfg.from.substring(0, 24);
    const i = s.indexOf(probe);
    console.error('FROM not found in', cfg.path);
    if (i >= 0) {
        console.error('found partial at', i, '->', JSON.stringify(s.substring(Math.max(0, i - 10), i + 60)));
    } else {
        console.error('no partial match for probe', JSON.stringify(probe));
    }
    process.exit(2);
}

const count = s.split(cfg.from).length - 1;
s = s.split(cfg.from).join(cfg.to);
fs.writeFileSync(cfg.path, s);
console.log('Replaced', count, 'occurrence(s) in', cfg.path);
