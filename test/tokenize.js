// Tokenizes text with the grammars of this extension, using the same engine as VS Code
// (vscode-textmate + vscode-oniguruma).
//
// CLI: node test/tokenize.js <languageId> <file> [maxLines]
const fs = require('fs');
const path = require('path');
const vsctm = require('vscode-textmate');
const oniguruma = require('vscode-oniguruma');

const ROOT = path.join(__dirname, '..');

function readManifest() {
  return JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8'));
}

let registry = null;
let grammarsByLanguage = null;

function getRegistry() {
  if (registry) return registry;
  const manifest = readManifest();
  const grammarPaths = {};
  grammarsByLanguage = {};
  for (const g of manifest.contributes.grammars) {
    grammarPaths[g.scopeName] = path.join(ROOT, g.path);
    grammarsByLanguage[g.language] = g.scopeName;
  }
  const wasm = fs.readFileSync(path.join(path.dirname(require.resolve('vscode-oniguruma')), 'onig.wasm')).buffer;
  const onigLib = oniguruma.loadWASM(wasm).then(() => ({
    createOnigScanner: (patterns) => new oniguruma.OnigScanner(patterns),
    createOnigString: (s) => new oniguruma.OnigString(s),
  }));
  registry = new vsctm.Registry({
    onigLib,
    loadGrammar: async (scopeName) => {
      const file = grammarPaths[scopeName];
      if (!file) return null;
      return vsctm.parseRawGrammar(fs.readFileSync(file, 'utf8'), file);
    },
  });
  return registry;
}

// Returns [{ text, tokens: [{ text, scopes }] }], one entry per line.
// `scopes` excludes the root scope of the grammar.
async function tokenize(languageId, text, maxLines) {
  const reg = getRegistry();
  const scopeName = grammarsByLanguage[languageId];
  if (!scopeName) throw new Error('No grammar registered for language ' + languageId);
  const grammar = await reg.loadGrammar(scopeName);
  if (!grammar) throw new Error('Could not load grammar ' + scopeName);
  let lines = text.replace(/^﻿/, '').split(/\r?\n/);
  if (maxLines) lines = lines.slice(0, maxLines);
  let ruleStack = vsctm.INITIAL;
  const result = [];
  for (const line of lines) {
    const r = grammar.tokenizeLine(line, ruleStack);
    ruleStack = r.ruleStack;
    result.push({
      text: line,
      tokens: r.tokens.map((t) => ({ text: line.substring(t.startIndex, t.endIndex), scopes: t.scopes.slice(1) })),
    });
  }
  return result;
}

function readText(file) {
  // Robot programs are often written in a legacy 8-bit encoding: never fail on invalid UTF-8
  return fs.readFileSync(file, 'latin1');
}

module.exports = { ROOT, readManifest, tokenize, readText };

if (require.main === module) {
  const [languageId, file, maxLines] = process.argv.slice(2);
  if (!languageId || !file) {
    console.error('Usage: node test/tokenize.js <languageId> <file> [maxLines]');
    process.exit(2);
  }
  tokenize(languageId, readText(file), maxLines ? parseInt(maxLines, 10) : 0).then((lines) => {
    lines.forEach((l, i) => {
      console.log(String(i + 1).padStart(4) + ' | ' + l.text);
      const scoped = l.tokens.filter((t) => t.scopes.length);
      if (scoped.length) {
        console.log('       -> ' + scoped.map((t) => JSON.stringify(t.text) + ':' + t.scopes.join(',')).join('  '));
      }
    });
  }).catch((e) => { console.error(e); process.exit(1); });
}
