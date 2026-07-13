#!/usr/bin/env node
'use strict';

/**
 * prompt-executor
 *
 * Tiny, dependency-free CLI that takes a prompt category and prints the
 * matching expert prompt. No install step, no network calls.
 *
 * Usage:
 *   prompt-executor <category>        Print the prompt for a category
 *   prompt-executor list              List all available categories
 *   prompt-executor search <term>     Fuzzy-search categories by keyword
 *   prompt-executor --help            Show help
 *   prompt-executor --version         Print version
 *
 * Exit codes:
 *   0  success
 *   1  bad arguments / unknown category
 *   2  runtime error
 */

const { PROMPTS } = require('../src/prompts');
const VERSION = require('../package.json').version;

const HELP = `prompt-executor v${VERSION}
A tiny, dependency-free CLI that prints an expert prompt for a category.

USAGE
  prompt-executor <category>          Print the prompt for a category
  prompt-executor list                List all available categories
  prompt-executor search <term>       Search categories by keyword
  prompt-executor --help              Show this help
  prompt-executor --version           Print version

EXAMPLES
  prompt-executor coding
  prompt-executor search email
  prompt-executor list

Pass a category name (e.g. "coding", "marketing", "email"). Use
"prompt-executor list" to see every available category.`;

function listCategories() {
  const lines = PROMPTS.map(
    (p) => `  ${p.key.padEnd(16)} ${p.description}`
  );
  return `Available categories:\n${lines.join('\n')}\n\nRun "prompt-executor <category>" to print its prompt.`;
}

function searchCategories(term) {
  const q = term.toLowerCase();
  const matches = PROMPTS.filter(
    (p) =>
      p.key.toLowerCase().includes(q) ||
      p.title.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.prompt.toLowerCase().includes(q)
  );
  if (matches.length === 0) {
    return `No categories matched "${term}". Run "prompt-executor list" to see all.`;
  }
  const lines = matches.map(
    (p) => `  ${p.key.padEnd(16)} ${p.description}`
  );
  return `Matches for "${term}":\n${lines.join('\n')}`;
}

function normalizeKey(arg) {
  return arg.trim().toLowerCase().replace(/\s+/g, '-');
}

function main(argv) {
  const args = argv.slice(2);

  if (args.length === 0) {
    process.stdout.write(HELP + '\n');
    return 0;
  }

  const first = args[0];

  if (first === '--help' || first === '-h' || first === 'help') {
    process.stdout.write(HELP + '\n');
    return 0;
  }
  if (first === '--version' || first === '-v' || first === 'version') {
    process.stdout.write(VERSION + '\n');
    return 0;
  }
  if (first === 'list' || first === 'ls') {
    process.stdout.write(listCategories() + '\n');
    return 0;
  }
  if (first === 'search') {
    if (args.length < 2 || !args[1]) {
      process.stderr.write('Error: "search" requires a term.\n');
      return 1;
    }
    process.stdout.write(searchCategories(args[1]) + '\n');
    return 0;
  }

  const key = normalizeKey(first);
  const match = PROMPTS.find((p) => p.key === key);

  if (!match) {
    process.stderr.write(
      `Error: unknown category "${first}".\n\n` +
        listCategories() +
        '\n'
    );
    return 1;
  }

  process.stdout.write(`# ${match.title}\n\n${match.prompt}\n`);
  return 0;
}

if (require.main === module) {
  try {
    process.exit(main(process.argv));
  } catch (err) {
    process.stderr.write(`prompt-executor: unexpected error: ${err.stack || err}\n`);
    process.exit(2);
  }
}

module.exports = { main, normalizeKey, listCategories, searchCategories };
