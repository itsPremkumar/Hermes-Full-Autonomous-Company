#!/usr/bin/env node

/**
 * Unit tests for the PRO Company Seed Script (pro/seed.js).
 * Run with: node --test
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  loadTemplate,
  applyOverrides,
  validateConfig,
  parseArgs,
  coerceOverride,
  VERSION,
} from './seed.js';

test('loadTemplate returns a well-formed company config', async () => {
  const tpl = await loadTemplate();
  assert.equal(typeof tpl.company, 'object');
  assert.ok(Array.isArray(tpl.agents) && tpl.agents.length >= 5);
  assert.ok(Array.isArray(tpl.workflows) && tpl.workflows.length >= 1);
});

test('applyOverrides mutates a dot-path without touching the template', async () => {
  const tpl = await loadTemplate();
  const resolved = applyOverrides(tpl, { 'company.name': 'Acme Autonomous' });
  assert.equal(resolved.company.name, 'Acme Autonomous');
  // original template untouched
  assert.notEqual(tpl.company.name, 'Acme Autonomous');
});

test('applyOverrides coerces primitive types', async () => {
  const tpl = await loadTemplate();
  const resolved = applyOverrides(tpl, {
    'company.sharedMemory.enabled': false,
    'company.defaultMaxIterations': 99,
  });
  assert.equal(resolved.company.sharedMemory.enabled, false);
  assert.equal(resolved.company.defaultMaxIterations, 99);
});

test('validateConfig accepts the shipped template', async () => {
  const tpl = await loadTemplate();
  const warnings = validateConfig(tpl);
  assert.ok(Array.isArray(warnings));
});

test('validateConfig rejects a config with no agents', () => {
  assert.throws(() => validateConfig({ company: { name: 'X' }, agents: [] }));
});

test('validateConfig rejects a config missing company name', () => {
  assert.throws(() => validateConfig({ company: {}, agents: [{ role: 'a', adapterType: 'x' }] }));
});

test('parseArgs handles --set, --out, --api, --api-key', () => {
  const opts = parseArgs([
    '--set',
    'company.name=Acme',
    '--out',
    'c.json',
    '--api',
    'https://api.example.com',
    '--api-key',
    'secret',
    '--dry-run',
  ]);
  assert.equal(opts.overrides['company.name'], 'Acme');
  assert.equal(opts.outFile, 'c.json');
  assert.equal(opts.apiBase, 'https://api.example.com');
  assert.equal(opts.apiKey, 'secret');
  assert.equal(opts.dryRun, true);
});

test('coerceOverride parses booleans, numbers, and JSON arrays', () => {
  assert.equal(coerceOverride('true'), true);
  assert.equal(coerceOverride('false'), false);
  assert.equal(coerceOverride('null'), null);
  assert.equal(coerceOverride('42'), 42);
  assert.deepEqual(coerceOverride('[1,2,3]'), [1, 2, 3]);
  assert.equal(coerceOverride('plain-string'), 'plain-string');
});

test('parseArgs flags --help and --version', () => {
  assert.equal(parseArgs(['--help']).help, true);
  assert.equal(parseArgs(['-v']).version, true);
  assert.equal(parseArgs(['--json']).json, true);
});

test('VERSION is a semver string', () => {
  assert.match(VERSION, /^\d+\.\d+\.\d+$/);
});
