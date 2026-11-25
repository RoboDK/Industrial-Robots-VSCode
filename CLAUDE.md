# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A VS Code / VSCodium extension (publisher `RoboDK`) that provides TextMate syntax highlighting, language configuration, and snippets for industrial robot programming languages. It is bundled with RoboDK and is meant to cover the output of every RoboDK post processor.

Highlighting is purely declarative (JSON). The only code is a small activation script (`extension.js`, plain JavaScript, no build step) that picks the language from the file content when an extension is ambiguous.

## Everything is hand-edited JSON

There is no generator. (A Python generator existed until 0.1.6 and was retired; do not reintroduce `package_model.json` or `python/`.) A language consists of:

- `syntaxes/syntax.<id>.json`: TextMate grammar, `scopeName` is `robodk.<id>` (lowercase id).
- `cnfg.<id>.json`: language configuration (line comment, brackets, folding markers).
- `package.json`: `contributes.languages` entry (id, aliases, extensions, configuration) and `contributes.grammars` entry. Optional `contributes.snippets` entry pointing at `snippets/snippet.<id>.json`.

Language ids are brand names (`ABB`, `KUKA`, `Mitsubishi`, ...); file names use the lowercase id.

## Grammar conventions

- Top-level `patterns` is a list of `{ "include": "#rule" }`; rule order matters. When two rules match at the same position TextMate keeps the earlier one, so put comment and string rules first, then specific regexes (e.g. `DO[10]`), then plain keyword lists that contain the shorter word (`DO`).
- Use the shared scope names so every color theme works:

  | Meaning | Scope |
  |---|---|
  | comment | `comment` |
  | string | `string` |
  | number | `constant.numeric.c` |
  | program structure / control flow | `keyword.control` |
  | motion instructions | `entity.name.function.preprocessor.c` |
  | built-in functions / instructions | `entity.name.function.c` |
  | built-in variables / constants | `constant.language` |
  | data types | `storage.type.c` |
  | operators | `keyword.operator` |

- Regexes are Oniguruma. An isolated `(?i)` inside an alternation applies to everything after it, including later `|` branches; scope it with `(?i:...)` or put it at the very start.
- Numbers need a boundary so digits inside identifiers (`XP1`, `var_1`) are not colored: `-?(?<![\w.])\d+(\.\d+)?\b`.
- Many RoboDK posts emit placeholder lines that are not real controller syntax (`OUT[5]=TRUE`, `WAIT FOR IN[5]==TRUE TIMEOUT=...`, `CODE_INSERT_172`). Grammars should tolerate them but not treat them as keywords.

## File extensions

- The same extension can legitimately belong to several controllers (`.prg`: ABB, Epson, Mitsubishi, Yamaha...). Never remove or reassign an extension that a language already claims.
- A new language only claims an extension statically in `package.json` if no other language claims it; shared extensions are handled by content detection instead.
- Never claim generic extensions (`.txt`, `.cfg`, `.csv`, `.xml`, `.json`, `.py`, `.lua`, ...).
- Unusual extensions of generic formats are mapped to VS Code's built-in languages by adding a `contributes.languages` entry with the built-in id and no configuration, e.g. `{ "id": "lua", "extensions": [".aubo"] }`.

## Content detection

- `detect.json` maps a lowercase extension to an ordered candidate list: `{ ".prg": [ { "id": "ABB", "patterns": [...] }, ... ] }`. The first candidate with a matching pattern wins, so order them from most to least specific. Patterns are JavaScript regexes run with the multiline flag over the first 200 lines; a leading `(?i)` makes one case-insensitive. The key `.NNN` matches any three-digit extension. Candidate ids may be built-in languages (`python`, `lua`, `xml`, `json`, `ini`).
- `detect.js` is the pure matching function (no `vscode` import, unit-testable). `extension.js` calls it when a document opens and switches the language with `setTextDocumentLanguage`.
- It only replaces `plaintext` or a language that is a candidate/static owner of that extension, so a user's `files.associations` or manual choice is respected. An open event within a second of a close of the same file is treated as a manual language change and left alone. The setting `industrialRobots.detectLanguage` turns it off.
- When no pattern matches, the file keeps the static default: the last language in `package.json` that claims the extension.

## Sample programs

- `examples/`: hand-picked programs for the original languages (the `.rdk` files are the RoboDK stations that produced them).
- `examples/posts/<PostName>/`: one output per RoboDK post processor, copied from the `tests/outputs/MAIN_1` folder of the RoboDK-Post-Processors repository. Use these when writing or checking a grammar.

## Tests

```
npm install     # once: installs vscode-textmate and vscode-oniguruma (dev only)
npm test
```

- `test/manifest.test.js` checks `package.json` against the files on disk: every language has its config and grammar, scope names and file names follow the convention, snippet files exist, JSON has no duplicate keys, no extension is claimed by two languages (apart from the grandfathered `.prg` and `.pg` pairs), and no generic extension is claimed.
- `test/samples.test.js` tokenizes every sample listed in `test/samples.json` with the real VS Code engine and fails if a grammar does not compile, if fewer than 80% of the lines containing letters or digits get any highlighting, or if a comment line is not scoped as a comment. Every language with a grammar needs at least one sample. Useful flags: `--only <LanguageId>`, `--verbose` (lists unscoped lines), `--root <dir>` (check `<dir>/<Post>/<file>`, e.g. the `tests/outputs/MAIN_1/Posts` folder of RoboDK-Post-Processors).
- When `detect.json` exists, the sample test also asserts that each sample opens as its expected language (detected, or the static default of its extension).
- `test/extension.test.js` runs `extension.js` against a stub of the `vscode` API (activation, guards, setting).
- Inspect how a single file is tokenized: `node test/tokenize.js <LanguageId> <file> [maxLines]`.

## Trying changes

Launch the Extension Development Host with the `.vscode/launch.json` "Extension" config, or from the repo root:

```
code --disable-extensions --extensionDevelopmentPath=.
```

(`scripts/run_test.bat` and `scripts/run_test_codium.bat` do the same on Windows.)

## Packaging

```
npx @vscode/vsce package
```

The resulting `Industrial-Robots-<version>.vsix` is committed to the repo root (replace the previous one) and is bundled with RoboDK. Bump `version` in `package.json` and add a `CHANGELOG.md` entry first. `.vscodeignore` keeps `examples/`, `test/`, `scripts/` and `node_modules/` out of the package; `extension.js`, `detect.js` and `detect.json` must be in it.
