// Tokenizes one sample program per post processor and checks that the grammar works on it.
//
//   node test/samples.test.js                  check the samples in examples/posts
//   node test/samples.test.js --root <dir>     check <dir>/<Post>/<file> instead (for example the
//                                              tests/outputs/MAIN_1/Posts folder of RoboDK-Post-Processors)
//   node test/samples.test.js --only <Lang>    only check one language
//   node test/samples.test.js --verbose        list the unscoped lines
//
// test/samples.json lists the samples: { "post", "file", "language", "minCoverage"? }
const fs = require('fs');
const path = require('path');
const { ROOT, readManifest, tokenize, readText } = require('./tokenize');

const args = process.argv.slice(2);
const arg = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : null; };
const samplesRoot = arg('--root') || path.join(ROOT, 'examples', 'posts');
const only = arg('--only');
const verbose = args.includes('--verbose');

const DEFAULT_MIN_COVERAGE = 0.8;
const BUILTIN = new Set(['python', 'lua', 'json', 'jsonl', 'xml', 'ini', 'properties', 'javascript', 'java', 'plaintext']);

let detect = null;
let detectTable = null;
if (fs.existsSync(path.join(ROOT, 'detect.js')) && fs.existsSync(path.join(ROOT, 'detect.json'))) {
  detect = require(path.join(ROOT, 'detect.js')).detect;
  detectTable = JSON.parse(fs.readFileSync(path.join(ROOT, 'detect.json'), 'utf8'));
}

async function main() {
  const manifest = readManifest();
  const samples = JSON.parse(fs.readFileSync(path.join(__dirname, 'samples.json'), 'utf8'));
  const languages = {};
  for (const l of manifest.contributes.languages) languages[l.id] = Object.assign(languages[l.id] || {}, l);

  const failures = [];
  const covered = new Set();
  let checked = 0;
  for (const s of samples) {
    if (only && s.language !== only) continue;
    const label = `${s.post}/${s.file} [${s.language}]`;
    const file = path.join(samplesRoot, s.post, s.file);
    if (!fs.existsSync(file)) { failures.push(`${label}: sample file not found (${file})`); continue; }
    const text = readText(file);
    checked++;

    // 1. content detection picks the expected language
    if (detect) {
      const detected = detect(file, text.split(/\r?\n/).slice(0, 200), detectTable);
      const staticOwners = manifest.contributes.languages
        .filter((l) => (l.extensions || []).some((e) => e.toLowerCase() === path.extname(file).toLowerCase()))
        .map((l) => l.id);
      // VS Code uses the last registered language for an extension
      const staticDefault = staticOwners.length ? staticOwners[staticOwners.length - 1] : 'plaintext';
      const effective = detected || staticDefault;
      if (effective !== s.language) {
        failures.push(`${label}: opens as ${effective} (detected: ${detected}, default for extension: ${staticDefault})`);
      }
    }
    if (BUILTIN.has(s.language)) continue;
    covered.add(s.language);

    // 2. the grammar compiles and tokenizes
    let lines;
    try { lines = await tokenize(s.language, text); }
    catch (e) { failures.push(`${label}: ${e.message}`); continue; }

    // 3. most lines with words or numbers get some highlighting, and comment lines are comments
    const config = JSON.parse(fs.readFileSync(path.join(ROOT, languages[s.language].configuration), 'utf8'));
    const lineComment = config.comments && config.comments.lineComment;
    let nonBlank = 0, scoped = 0;
    const unscoped = [];
    for (const l of lines) {
      // blank lines and lines with only punctuation (a closing brace...) have nothing to highlight
      if (!/[A-Za-z0-9]/.test(l.text)) continue;
      nonBlank++;
      if (l.tokens.some((t) => t.scopes.length)) scoped++; else unscoped.push(l.text);
      if (lineComment && l.text.trim().startsWith(lineComment)) {
        const first = l.tokens.find((t) => t.text.trim());
        if (!first || !first.scopes.some((sc) => sc.startsWith('comment'))) {
          failures.push(`${label}: comment line not highlighted as a comment: ${l.text.trim().slice(0, 60)}`);
          break;
        }
      }
    }
    const coverage = nonBlank ? scoped / nonBlank : 1;
    const min = s.minCoverage === undefined ? DEFAULT_MIN_COVERAGE : s.minCoverage;
    if (coverage < min) {
      failures.push(`${label}: only ${(coverage * 100).toFixed(0)}% of lines are highlighted (minimum ${(min * 100).toFixed(0)}%), e.g. ` +
        unscoped.slice(0, 3).map((u) => JSON.stringify(u.trim().slice(0, 50))).join(', '));
    }
    if (verbose) {
      console.log(`${label}: ${(coverage * 100).toFixed(0)}% of ${nonBlank} lines`);
      for (const u of [...new Set(unscoped)].slice(0, 8)) console.log('      unscoped: ' + u.trim().slice(0, 100));
    }
  }

  // every language with a grammar needs at least one sample
  if (!only && !arg('--root')) {
    for (const g of manifest.contributes.grammars) {
      if (!covered.has(g.language)) failures.push(`${g.language}: no sample in test/samples.json`);
    }
  }

  if (failures.length) {
    console.error(`samples: ${failures.length} problem(s) in ${checked} samples`);
    for (const f of failures) console.error('  - ' + f);
    process.exit(1);
  }
  console.log(`samples: OK (${checked} samples, ${covered.size} languages${detect ? ', detection checked' : ''})`);
}

main().catch((e) => { console.error(e); process.exit(1); });
