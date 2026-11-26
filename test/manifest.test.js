// Consistency checks over package.json and the files it references.
// These replace the checks the old Python generator used to guarantee.
const fs = require('fs');
const path = require('path');
const { ROOT, readManifest } = require('./tokenize');

// Languages that ship with VS Code: this extension may add file extensions to them
const BUILTIN = new Set(['python', 'lua', 'json', 'jsonc', 'jsonl', 'xml', 'ini', 'properties', 'javascript', 'java', 'latex', 'plaintext']);

// Extensions that were already shared before this rule existed. Do not extend this list:
// a new language must not statically claim an extension another language already claims.
const SHARED_ALLOWED = { '.prg': ['ABB', 'Epson'], '.pg': ['Kawasaki', 'Omron'] };

// Too generic to be claimed by a robot language (content detection handles them)
const GENERIC = new Set(['.txt', '.cfg', '.csv', '.xml', '.json', '.py', '.lua', '.js', '.java', '.pro', '.task', '.path', '.prog', '.flow', '.ini', '.log', '.md']);

const errors = [];
const check = (cond, msg) => { if (!cond) errors.push(msg); };

// JSON.parse with duplicate key detection (JSON.parse silently keeps the last one)
function parseStrict(file) {
  const text = fs.readFileSync(file, 'utf8');
  let data;
  try { data = JSON.parse(text); } catch (e) { errors.push(`${file}: invalid JSON (${e.message})`); return null; }
  const stack = [];
  const re = /"(?:[^"\\]|\\.)*"\s*:|[{}\[\]]|"(?:[^"\\]|\\.)*"/g;
  let m;
  while ((m = re.exec(text))) {
    const t = m[0];
    if (t === '{') stack.push(new Set());
    else if (t === '[') stack.push(null);
    else if (t === '}' || t === ']') stack.pop();
    else if (t.endsWith(':')) {
      const key = t.slice(0, t.lastIndexOf('"') + 1);
      const top = stack[stack.length - 1];
      if (top) { check(!top.has(key), `${file}: duplicate key ${key}`); top.add(key); }
    }
  }
  return data;
}

const rel = (p) => path.join(ROOT, p);
const manifest = parseStrict(rel('package.json')) || readManifest();
const { languages, grammars, snippets = [] } = manifest.contributes;

const ids = new Set();
const claims = {};
for (const lang of languages) {
  const isAssociation = BUILTIN.has(lang.id);
  check(isAssociation || !ids.has(lang.id), `language ${lang.id} is declared twice`);
  ids.add(lang.id);
  for (const ext of lang.extensions || []) {
    check(ext.startsWith('.'), `${lang.id}: extension "${ext}" must start with a dot`);
    const key = ext.toLowerCase();
    check(!GENERIC.has(key), `${lang.id}: generic extension ${ext} must not be claimed, use detect.json instead`);
    (claims[key] = claims[key] || new Set()).add(lang.id);
  }
  if (isAssociation) {
    check(!lang.configuration, `${lang.id}: built-in language must not get a configuration`);
    continue;
  }
  check(lang.configuration, `${lang.id}: missing "configuration"`);
  if (lang.configuration) {
    check(lang.configuration === `./cnfg.${lang.id.toLowerCase()}.json`, `${lang.id}: configuration should be ./cnfg.${lang.id.toLowerCase()}.json`);
    check(fs.existsSync(rel(lang.configuration)), `${lang.id}: ${lang.configuration} does not exist`);
    if (fs.existsSync(rel(lang.configuration))) parseStrict(rel(lang.configuration));
  }
  const g = grammars.filter((x) => x.language === lang.id);
  check(g.length === 1, `${lang.id}: expected exactly one grammar entry, found ${g.length}`);
}

for (const [ext, owners] of Object.entries(claims)) {
  if (owners.size < 2) continue;
  const allowed = SHARED_ALLOWED[ext] || [];
  const extra = [...owners].filter((o) => !allowed.includes(o));
  check(extra.length === 0, `extension ${ext} is claimed by ${[...owners].join(', ')}: ` +
    `${extra.join(', ')} must use detect.json instead of claiming it`);
}

for (const g of grammars) {
  check(ids.has(g.language) && !BUILTIN.has(g.language), `grammar for unknown language ${g.language}`);
  const expectedScope = `robodk.${g.language.toLowerCase()}`;
  check(g.scopeName === expectedScope, `${g.language}: scopeName should be ${expectedScope}`);
  check(g.path === `./syntaxes/syntax.${g.language.toLowerCase()}.json`, `${g.language}: grammar path should be ./syntaxes/syntax.${g.language.toLowerCase()}.json`);
  if (!fs.existsSync(rel(g.path))) { errors.push(`${g.language}: ${g.path} does not exist`); continue; }
  const grammar = parseStrict(rel(g.path));
  if (!grammar) continue;
  check(grammar.scopeName === g.scopeName, `${g.path}: scopeName ${grammar.scopeName} does not match package.json (${g.scopeName})`);
  for (const p of grammar.patterns || []) {
    if (p.include && p.include.startsWith('#')) {
      check(grammar.repository && grammar.repository[p.include.slice(1)], `${g.path}: include ${p.include} has no rule in the repository`);
    }
  }
}

for (const s of snippets) {
  check(ids.has(s.language), `snippets for unknown language ${s.language}`);
  check(fs.existsSync(rel(s.path)), `${s.language}: ${s.path} does not exist`);
  if (fs.existsSync(rel(s.path))) parseStrict(rel(s.path));
}

// Every grammar and config file on disk must be registered
for (const f of fs.readdirSync(rel('syntaxes'))) {
  check(grammars.some((g) => g.path === `./syntaxes/${f}`), `syntaxes/${f} is not registered in package.json`);
}
for (const f of fs.readdirSync(ROOT).filter((x) => /^cnfg\..*\.json$/.test(x))) {
  check(languages.some((l) => l.configuration === `./${f}`), `${f} is not registered in package.json`);
}

// detect.json (content detection table), once it exists
const detectFile = rel('detect.json');
if (fs.existsSync(detectFile)) {
  const table = parseStrict(detectFile) || {};
  for (const [ext, candidates] of Object.entries(table)) {
    check(ext.startsWith('.'), `detect.json: key "${ext}" must be a file extension`);
    for (const c of candidates) {
      check(ids.has(c.id) || BUILTIN.has(c.id), `detect.json ${ext}: unknown language ${c.id}`);
      check(Array.isArray(c.patterns) && c.patterns.length > 0, `detect.json ${ext} ${c.id}: needs at least one pattern`);
      for (const p of c.patterns || []) {
        try { require(rel('detect.js')).compile(p); } catch (e) { errors.push(`detect.json ${ext} ${c.id}: bad pattern ${p} (${e.message})`); }
      }
    }
  }
}

// A built-in VS Code language that claims one of our extensions wins over our claim, and extension.js only
// replaces a language that is a candidate in detect.json. So every such extension needs a detect.json entry
// that lists our language(s) and the built-in language.
const builtinFile = path.join(__dirname, 'vscode-builtin-languages.json');
if (fs.existsSync(builtinFile)) {
  const builtinExt = JSON.parse(fs.readFileSync(builtinFile, 'utf8')).extensions;
  const table = fs.existsSync(detectFile) ? JSON.parse(fs.readFileSync(detectFile, 'utf8')) : {};
  const ours = {};
  for (const [ext, owners] of Object.entries(claims)) {
    const robot = [...owners].filter((o) => !BUILTIN.has(o));
    if (robot.length) ours[ext] = robot;
  }
  for (const [ext, candidates] of Object.entries(table)) {
    if (ext === '.NNN') continue;
    const robot = candidates.map((c) => c.id).filter((id) => !BUILTIN.has(id));
    if (robot.length) ours[ext] = [...new Set([...(ours[ext] || []), ...robot])];
  }
  for (const [ext, robot] of Object.entries(ours)) {
    const builtin = builtinExt[ext];
    if (!builtin || robot.includes(builtin)) continue;
    const ids = (table[ext] || []).map((c) => c.id);
    for (const id of robot) {
      check(ids.includes(id), `${ext}: VS Code's built-in ${builtin} language claims it, so ${id} needs a detect.json entry for ${ext}`);
    }
    check(ids.includes(builtin), `${ext}: VS Code's built-in ${builtin} language claims it, so detect.json ${ext} must list "${builtin}" as a candidate (otherwise detection never replaces it)`);
  }
}

if (errors.length) {
  console.error('manifest: ' + errors.length + ' problem(s)');
  for (const e of errors) console.error('  - ' + e);
  process.exit(1);
}
console.log(`manifest: OK (${[...ids].filter((i) => !BUILTIN.has(i)).length} languages, ${grammars.length} grammars, ${snippets.length} snippet files)`);
