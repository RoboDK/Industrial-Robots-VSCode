// Exercises extension.js (content detection) against a minimal stand-in for the vscode API.
const path = require('path');
const Module = require('module');
const { ROOT, readManifest } = require('./tokenize');

const calls = [];
let detectEnabled = true;
const listeners = { open: [], close: [] };
const fakeVscode = {
  workspace: {
    textDocuments: [],
    getConfiguration: () => ({ get: (key, def) => (key === 'detectLanguage' ? detectEnabled : def) }),
    onDidOpenTextDocument: (fn) => { listeners.open.push(fn); return { dispose() {} }; },
    onDidCloseTextDocument: (fn) => { listeners.close.push(fn); return { dispose() {} }; },
  },
  languages: {
    setTextDocumentLanguage: (doc, id) => { calls.push({ file: doc.fileName, id }); return Promise.resolve(doc); },
  },
};
const originalLoad = Module._load;
Module._load = function (request, ...rest) {
  return request === 'vscode' ? fakeVscode : originalLoad.call(this, request, ...rest);
};

const extension = require(path.join(ROOT, 'extension.js'));

function doc(fileName, languageId, text, scheme = 'file') {
  const lines = text.split('\n');
  return {
    fileName, languageId, lineCount: lines.length,
    uri: { scheme, toString: () => scheme + '://' + fileName },
    lineAt: (i) => ({ text: lines[i] }),
  };
}
const open = (d) => listeners.open.forEach((fn) => fn(d));
const close = (d) => listeners.close.forEach((fn) => fn(d));

const RAPID = '%%%\n  VERSION:1\n%%%\nMODULE Prog\n  PROC main()\n  ENDPROC\nENDMODULE';
const SPEL = 'Function main\n  Motor On\nFend';

const errors = [];
function expect(name, expected) {
  const got = calls.map((c) => c.id).join(',');
  if (got !== expected) errors.push(`${name}: expected language change "${expected}", got "${got}"`);
  calls.length = 0;
}

// A document that is already open when the extension starts
fakeVscode.workspace.textDocuments = [doc('/w/start.prg', 'Epson', RAPID)];
extension.activate({ subscriptions: [], extension: { packageJSON: readManifest() } });
expect('already open at activation', 'ABB');

open(doc('/w/a.prg', 'Epson', RAPID));
expect('default language replaced by detected one', 'ABB');

open(doc('/w/b.prg', 'ABB', RAPID));
expect('already the right language', '');

open(doc('/w/c.prg', 'Epson', SPEL));
expect('default is already correct', '');

open(doc('/w/d.prg', 'Epson', 'nothing recognisable here'));
expect('no signature: keep the default', '');

open(doc('/w/e.prg', 'python', RAPID));
expect('user association to another language is respected', '');

open(doc('/w/f.md', 'markdown', RAPID));
expect('extension without detection entry', '');

open(doc('/w/g.prg', 'Epson', RAPID, 'git'));
expect('non-file scheme ignored', '');

const manual = doc('/w/h.prg', 'Epson', RAPID);
close(manual);
open(manual);
expect('reopen right after close is a manual language change', '');

detectEnabled = false;
open(doc('/w/i.prg', 'Epson', RAPID));
expect('setting disabled', '');
detectEnabled = true;

if (errors.length) {
  console.error('extension: ' + errors.length + ' problem(s)');
  for (const e of errors) console.error('  - ' + e);
  process.exit(1);
}
console.log('extension: OK');
