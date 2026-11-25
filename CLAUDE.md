# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A VS Code / VSCodium extension (publisher `RoboDK`) that provides TextMate syntax highlighting, language configuration, and snippets for industrial robot programming languages. It is bundled with RoboDK and is meant to cover the output of every RoboDK post processor.

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

## Sample programs

- `examples/`: hand-picked programs for the original languages (the `.rdk` files are the RoboDK stations that produced them).
- `examples/posts/<PostName>/`: one output per RoboDK post processor, copied from the `tests/outputs/MAIN_1` folder of the RoboDK-Post-Processors repository. Use these when writing or checking a grammar.

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

The resulting `Industrial-Robots-<version>.vsix` is committed to the repo root (replace the previous one) and is bundled with RoboDK. Bump `version` in `package.json` and add a `CHANGELOG.md` entry first. `.vscodeignore` keeps `examples/`, `test/`, `scripts/` and `node_modules/` out of the package.
