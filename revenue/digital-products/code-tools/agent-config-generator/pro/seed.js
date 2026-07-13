#!/usr/bin/env node

/**
 * agent-config-generator — PRO: Paperclip Company Seed Script
 * ------------------------------------------------------------
 * Materialises the multi-agent orchestration company template
 * (pro/company-template.json) into a ready-to-deploy Paperclip company
 * configuration, applies runtime overrides, validates it, and (optionally)
 * POSTs it to a Paperclip-compatible API.
 *
 * This is part of the PRO ($29) tier: it bootstraps your entire autonomous
 * org in one command instead of hand-wiring five agents and two workflows.
 *
 * Zero runtime dependencies — uses only Node built-ins.
 *
 * @license MIT
 * @author Prem Autonomous Co <https://premautonomous.co>
 * @tier pro
 */

import { readFile, writeFile, access } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import https from 'node:https';
import http from 'node:http';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TEMPLATE_PATH = path.join(__dirname, 'company-template.json');
const VERSION = '1.0.0';

/**
 * @typedef {Object} SeedOptions
 * @property {string} [apiBase]   Base URL of a Paperclip-compatible API.
 * @property {string} [apiKey]    Bearer token for the API.
 * @property {string} [outFile]   Where to write the resolved config.
 * @property {Object<string, unknown>} [overrides]  Dot-path overrides.
 * @property {boolean} [dryRun]   Validate + print, do not write or POST.
 * @property {boolean} [json]     Machine-readable output.
 */

/**
 * Small dot-path setter: set({a:{b:1}}, 'a.b', 2) → {a:{b:2}}.
 * @param {Record<string, unknown>} obj
 * @param {string} dotted
 * @param {unknown} value
 * @returns {void}
 */
function setDotPath(obj, dotted, value) {
  const parts = dotted.split('.');
  let cursor = obj;
  for (let i = 0; i < parts.length - 1; i += 1) {
    const key = parts[i];
    if (typeof cursor[key] !== 'object' || cursor[key] === null) {
      cursor[key] = {};
    }
    cursor = /** @type {Record<string, unknown>} */ (cursor[key]);
  }
  cursor[parts[parts.length - 1]] = value;
}

/**
 * Coerce a string override value into a JSON-native primitive when possible.
 * @param {string} raw
 * @returns {unknown}
 */
function coerceOverride(raw) {
  if (raw === 'true') return true;
  if (raw === 'false') return false;
  if (raw === 'null') return null;
  if (/^-?\d+(\.\d+)?$/.test(raw)) return Number(raw);
  if (
    (raw.startsWith('[') && raw.endsWith(']')) ||
    (raw.startsWith('{') && raw.endsWith('}'))
  ) {
    try {
      return JSON.parse(raw);
    } catch {
      /* fall through to string */
    }
  }
  return raw;
}

/**
 * Load the PRO company template.
 * @returns {Promise<Record<string, unknown>>}
 */
export async function loadTemplate() {
  const raw = await readFile(TEMPLATE_PATH, 'utf-8');
  return JSON.parse(raw);
}

/**
 * Apply dot-path overrides to a deep-cloned template.
 * @param {Record<string, unknown>} template
 * @param {Record<string, unknown>} overrides
 * @returns {Record<string, unknown>}
 */
export function applyOverrides(template, overrides) {
  const clone = JSON.parse(JSON.stringify(template));
  for (const [key, value] of Object.entries(overrides)) {
    setDotPath(clone, key, value);
  }
  return clone;
}

/**
 * Validate the resolved company config. Throws on the first hard failure.
 * @param {Record<string, unknown>} cfg
 * @returns {string[]} warnings (non-fatal)
 */
export function validateConfig(cfg) {
  const warnings = [];
  if (!cfg || typeof cfg !== 'object') {
    throw new Error('Config root must be an object.');
  }
  const company = /** @type {any} */ (cfg).company;
  if (!company || !company.name) {
    throw new Error('Missing company.name');
  }
  const agents = /** @type {any[]> */ (cfg).agents;
  if (!Array.isArray(agents) || agents.length === 0) {
    throw new Error('company must define at least one agent');
  }
  const roles = new Set();
  for (const agent of agents) {
    if (!agent.role) throw new Error('Every agent needs a role');
    if (!agent.adapterType) throw new Error(`Agent ${agent.role} needs adapterType`);
    if (roles.has(agent.role)) warnings.push(`Duplicate agent role: ${agent.role}`);
    roles.add(agent.role);
  }
  // Validate handoff rules reference known roles.
  for (const agent of agents) {
    const rules = agent.handoffRules;
    if (!rules) continue;
    for (const dir of ['acceptFrom', 'delegateTo', 'escalateTo']) {
      const list = rules[dir];
      const items = Array.isArray(list) ? list : list ? [list] : [];
      for (const r of items) {
        if (r === '__complete__' || r === agent.role) continue;
        if (!roles.has(r)) warnings.push(`Agent ${agent.role} references unknown role "${r}" in ${dir}`);
      }
    }
  }
  return warnings;
}

/**
 * POST the resolved config to a Paperclip-compatible company bootstrap endpoint.
 * @param {string} apiBase
 * @param {string} apiKey
 * @param {Record<string, unknown>} cfg
 * @returns {Promise<{status: number, body: string}>}
 */
export function postToApi(apiBase, apiKey, cfg) {
  return new Promise((resolve, reject) => {
    const url = new URL('/api/companies', apiBase.replace(/\/$/, '') + '/');
    const payload = JSON.stringify(cfg);
    const lib = url.protocol === 'http:' ? http : https;
    const req = lib.request(
      url,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${apiKey}`,
          'Content-Length': Buffer.byteLength(payload),
        },
      },
      (res) => {
        let data = '';
        res.on('data', (chunk) => {
          data += chunk;
        });
        res.on('end', () =>
          resolve({ status: res.statusCode ?? 0, body: data }),
        );
      },
    );
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

/**
 * Parse CLI args into options.
 * @param {string[]} argv
 * @returns {SeedOptions & { help: boolean; version: boolean }}
 */
export function parseArgs(argv) {
  const opts = { overrides: {}, help: false, version: false, dryRun: false };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--help' || a === '-h') opts.help = true;
    else if (a === '--version' || a === '-v') opts.version = true;
    else if (a === '--dry-run') opts.dryRun = true;
    else if (a === '--json') opts.json = true;
    else if (a === '--api') opts.apiBase = argv[++i];
    else if (a === '--api-key') opts.apiKey = argv[++i];
    else if (a === '--out') opts.outFile = argv[++i];
    else if (a.startsWith('--set=')) {
      const body = a.slice('--set='.length);
      const eq = body.indexOf('=');
      if (eq === -1) throw new Error(`Invalid --set (expected key=value): ${a}`);
      const key = body.slice(0, eq);
      const value = coerceOverride(body.slice(eq + 1));
      opts.overrides[key] = value;
    } else if (a === '--set') {
      const body = argv[++i];
      const eq = body.indexOf('=');
      if (eq === -1) throw new Error(`Invalid --set (expected key=value): ${a} ${body}`);
      const key = body.slice(0, eq);
      const value = coerceOverride(body.slice(eq + 1));
      opts.overrides[key] = value;
    } else {
      throw new Error(`Unknown argument: ${a}`);
    }
  }
  return opts;
}

/**
 * Main entry.
 * @param {string[]} argv
 * @returns {Promise<number>} process exit code
 */
export async function main(argv) {
  const opts = parseArgs(argv);

  if (opts.version) {
    console.log(VERSION);
    return 0;
  }
  if (opts.help) {
    console.log(`
  gen-company v${VERSION}  —  PRO Paperclip Company Seed Script

  Materialises the multi-agent orchestration company template and
  bootstraps your autonomous org.

  USAGE
    node pro/seed.js --help
    node pro/seed.js --out company.json
    node pro/seed.js --set company.name="Acme Autonomous" --dry-run
    node pro/seed.js --api https://api.paperclip.so --api-key \$KEY

  OPTIONS
    --out <file>        Write resolved config to <file>
    --set key=value     Override a dot-path (e.g. company.name="X")
    --api <url>         Paperclip-compatible API base URL
    --api-key <key>     Bearer token (or set PAPERCLIP_API_KEY)
    --dry-run           Validate + print, do not write or POST
    --json              Machine-readable output
    --version, -v       Print version
    --help, -h          Show this message

  This script is part of the agent-config-generator PRO tier ($29).
  https://premautonomous.co/products/agent-config-generator
`);
    return 0;
  }

  const template = await loadTemplate();
  const resolved = applyOverrides(template, opts.overrides);
  const warnings = validateConfig(resolved);

  if (opts.dryRun || (!opts.outFile && !opts.apiBase && !opts.apiKey)) {
    if (!opts.json) {
      console.log('Resolved PRO company config:\n');
    }
    console.log(JSON.stringify(resolved, null, 2));
    if (warnings.length && !opts.json) {
      console.log('\nWarnings:');
      for (const w of warnings) console.log(`  ⚠ ${w}`);
    }
    if (!opts.json) {
      console.log(
        '\nDry run complete. Re-run with --out <file> or --api <url> to deploy.',
      );
    }
    return 0;
  }

  if (opts.outFile) {
    await writeFile(opts.outFile, JSON.stringify(resolved, null, 2) + '\n', 'utf-8');
    if (!opts.json) console.log(`✓ Wrote company config → ${opts.outFile}`);
  }

  const apiBase = opts.apiBase;
  const apiKey = opts.apiKey || process.env.PAPERCLIP_API_KEY;
  if (apiBase) {
    if (!apiKey) {
      console.error('\n✖ --api requires --api-key or PAPERCLIP_API_KEY env var.');
      return 1;
    }
    if (!opts.json) console.log(`\n→ POSTing company to ${apiBase} ...`);
    const res = await postToApi(apiBase, apiKey, resolved);
    if (!opts.json) {
      console.log(`  HTTP ${res.status}`);
      console.log(res.body);
    } else {
      console.log(JSON.stringify({ status: res.status, body: res.body }));
    }
    if (res.status >= 400) return 1;
  }

  if (warnings.length && !opts.json) {
    console.log('\nWarnings:');
    for (const w of warnings) console.log(`  ⚠ ${w}`);
  }
  return 0;
}

const isMain =
  process.argv[1] &&
  fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);

if (isMain) {
  main(process.argv.slice(2))
    .then((code) => process.exit(code))
    .catch((err) => {
      console.error(`\n✖ ${err instanceof Error ? err.message : String(err)}`);
      process.exit(1);
    });
}

export { VERSION };
export { coerceOverride };
export default { loadTemplate, applyOverrides, validateConfig, postToApi, parseArgs, main, VERSION };
