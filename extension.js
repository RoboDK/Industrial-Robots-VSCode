// Picks the robot language from the content of a file when its extension is shared by several
// controllers (.prg, .script, .job...) or is too generic to be claimed (.txt, .cfg...).
// Syntax highlighting itself is purely declarative (see package.json, syntaxes/ and cnfg.*.json).
'use strict';

const vscode = require('vscode');
const { detect, extensionKey } = require('./detect');
const table = require('./detect.json');

const MAX_LINES = 200;
// setTextDocumentLanguage closes and reopens the document: an open event this soon after a close
// of the same file is a language change (by the user or by us), not a new file
const REOPEN_MS = 1000;
const SCHEMES = new Set(['file', 'vscode-remote', 'vscode-vfs', 'vscode-userdata']);

function activate(context) {
  // Languages that own each extension statically (package.json)
  const owners = {};
  for (const lang of context.extension.packageJSON.contributes.languages) {
    for (const ext of lang.extensions || []) {
      const key = ext.toLowerCase();
      (owners[key] = owners[key] || new Set()).add(lang.id);
    }
  }

  const closedAt = new Map();

  function check(doc) {
    if (!SCHEMES.has(doc.uri.scheme)) return;
    const key = extensionKey(doc.fileName);
    const candidates = table[key];
    if (!candidates) return;
    if (!vscode.workspace.getConfiguration('industrialRobots', doc.uri).get('detectLanguage', true)) return;

    const uri = doc.uri.toString();
    const closed = closedAt.get(uri);
    if (closed !== undefined && Date.now() - closed < REOPEN_MS) return;

    // Only replace the default choice for this extension. Any other language means the user
    // (or a files.associations setting) decided, and that decision is respected.
    const current = doc.languageId;
    const replaceable = current === 'plaintext' ||
      candidates.some((c) => c.id === current) ||
      (owners[key] && owners[key].has(current));
    if (!replaceable) return;

    const lines = [];
    const count = Math.min(doc.lineCount, MAX_LINES);
    for (let i = 0; i < count; i++) lines.push(doc.lineAt(i).text);
    const id = detect(doc.fileName, lines, table);
    if (id && id !== current) {
      vscode.languages.setTextDocumentLanguage(doc, id).then(undefined, () => { /* unknown language id: keep the default */ });
    }
  }

  context.subscriptions.push(
    vscode.workspace.onDidCloseTextDocument((doc) => {
      closedAt.set(doc.uri.toString(), Date.now());
      if (closedAt.size > 500) {
        const limit = Date.now() - REOPEN_MS;
        for (const [uri, time] of closedAt) if (time < limit) closedAt.delete(uri);
      }
    }),
    vscode.workspace.onDidOpenTextDocument(check)
  );
  vscode.workspace.textDocuments.forEach(check);
}

function deactivate() {}

module.exports = { activate, deactivate };
