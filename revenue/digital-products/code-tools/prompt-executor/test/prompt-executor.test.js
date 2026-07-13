'use strict';

/**
 * Minimal test harness (no test framework dependency).
 * Run with: node test/prompt-executor.test.js
 */

const assert = require('assert');
const path = require('path');

const cli = require(path.join(__dirname, '..', 'bin', 'prompt-executor.js'));
const { PROMPTS } = require(path.join(__dirname, '..', 'src', 'prompts.js'));

let passed = 0;
function check(name, fn) {
  fn();
  passed += 1;
  console.log(`  ok  ${name}`);
}

function captureStreams(fn) {
  const chunks = [];
  const origOut = process.stdout.write.bind(process.stdout);
  const origErr = process.stderr.write.bind(process.stderr);
  process.stdout.write = (s) => { chunks.push(s); return true; };
  process.stderr.write = (s) => { chunks.push(s); return true; };
  let code;
  try {
    code = fn();
  } finally {
    process.stdout.write = origOut;
    process.stderr.write = origErr;
  }
  return { code, out: chunks.join('') };
}

const captureStdout = captureStreams;

console.log('prompt-executor tests');

check('lists all categories', () => {
  const { code, out } = captureStdout(() => cli.main(['node', 'prompt-executor', 'list']));
  assert.strictEqual(code, 0);
  for (const p of PROMPTS) {
    assert.ok(out.includes(p.key), `list should include ${p.key}`);
  }
});

check('prints a known category prompt', () => {
  const { code, out } = captureStdout(() => cli.main(['node', 'prompt-executor', 'coding']));
  assert.strictEqual(code, 0);
  const coding = PROMPTS.find((p) => p.key === 'coding');
  assert.ok(out.includes(coding.prompt), 'should print the coding prompt');
  assert.ok(out.includes('# Code Helper'), 'should print the title header');
});

check('unknown category exits 1 and lists options', () => {
  const { code, out } = captureStdout(() => cli.main(['node', 'prompt-executor', 'nope']));
  assert.strictEqual(code, 1);
  assert.ok(out.includes('unknown category'), 'should report unknown category');
  assert.ok(out.includes('Available categories'), 'should show available list');
});

check('search finds matches', () => {
  const { code, out } = captureStdout(() => cli.main(['node', 'prompt-executor', 'search', 'email']));
  assert.strictEqual(code, 0);
  assert.ok(out.includes('email'), 'search should mention email');
});

check('search with no term exits 1', () => {
  const { code } = captureStdout(() => cli.main(['node', 'prompt-executor', 'search']));
  assert.strictEqual(code, 1);
});

check('no args prints help (exit 0)', () => {
  const { code, out } = captureStdout(() => cli.main(['node', 'prompt-executor']));
  assert.strictEqual(code, 0);
  assert.ok(out.includes('USAGE'), 'help should include USAGE');
});

check('normalizeKey handles spaces and case', () => {
  assert.strictEqual(cli.normalizeKey('Social Media'), 'social-media');
  assert.strictEqual(cli.normalizeKey('  SEO  '), 'seo');
});

check('every prompt has required fields', () => {
  for (const p of PROMPTS) {
    assert.ok(p.key && p.title && p.description && p.prompt, `incomplete entry: ${p.key}`);
  }
});

console.log(`\n${passed} tests passed.`);
