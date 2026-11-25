// Content-based language detection for file extensions shared by several robot controllers.
// Pure module (no dependency on the vscode API) so it can be unit tested with Node.
//
// detect.json maps a lowercase file extension to an ordered list of candidates:
//   { ".prg": [ { "id": "ABB", "patterns": ["^\\s*MODULE\\b", ...] }, ... ] }
// The first candidate with a matching pattern wins, so list the most specific signatures first.
// Patterns are JavaScript regular expressions tested against the first lines of the file with
// the multiline flag; start a pattern with (?i) to make it case-insensitive.
// The special key ".NNN" stands for any three-digit extension (.001, .042, ...).
'use strict';

const compiled = new Map();

function compile(pattern) {
  let re = compiled.get(pattern);
  if (!re) {
    const insensitive = pattern.startsWith('(?i)');
    re = new RegExp(insensitive ? pattern.slice(4) : pattern, insensitive ? 'mi' : 'm');
    compiled.set(pattern, re);
  }
  return re;
}

function extensionKey(fileName) {
  const base = fileName.replace(/^.*[\\/]/, '');
  const dot = base.lastIndexOf('.');
  if (dot <= 0) return '';
  const ext = base.slice(dot).toLowerCase();
  return /^\.\d{3}$/.test(ext) ? '.NNN' : ext;
}

// Returns the language id for the file, or null when the content gives no clear answer.
function detect(fileName, lines, table) {
  const candidates = table[extensionKey(fileName)];
  if (!candidates) return null;
  const text = (Array.isArray(lines) ? lines.join('\n') : String(lines)).replace(/^﻿/, '');
  for (const candidate of candidates) {
    if (candidate.patterns.some((p) => compile(p).test(text))) return candidate.id;
  }
  return null;
}

module.exports = { detect, extensionKey, compile };
