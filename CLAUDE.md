# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A VS Code / VSCodium extension (publisher `RoboDK`) that provides TextMate syntax highlighting, language configuration, and snippets for industrial robot programming languages: ABB RAPID, Comau PDL, Fanuc LS, Kawasaki, KUKA KRL (SRC/DAT), Yaskawa Motoman INFORM (JBI), Stäubli VAL3, and Universal Robots Script. There is no extension host code (no `main`/`activate`); it is a pure declarative language-contribution extension.

## Generated files: edit the Python, not the JSON

The `syntaxes/*.json`, `cnfg.*.json`, and `package.json` files are **generated** by the scripts in `python/`. Edit the `python/theme_*.py` source and regenerate rather than hand-editing the JSON. Recent fixes (e.g. the Fanuc `IF`/`NOT` regex hotfix, the Motoman target highlighting fix) changed both the `theme_*.py` file and the generated JSON in the same commit; keep them in sync.

Regenerate everything (must be run from inside `python/`, since the scripts write to `../`):

```
cd python
python3 update_themes.py
```

This executes every `theme_*.py` via `exec()`, writes `../syntaxes/syntax.<id>.json` and `../cnfg.<id>.json` for each language, and rewrites `../package.json` from `package_model.json` by substituting the `###contributes###` placeholder with the generated `languages`/`grammars`/`snippets` arrays. Consequently:

- Extension metadata (version, description, keywords) lives in `package_model.json`, not `package.json`. Bump the version there.
- Importing `theme_Fanuc.py` directly (not via `update_themes.py`) also regenerates just that language, since each theme file calls `update_syntax()`/`update_config()` at module level.
- Snippet files are hand-written, not generated. The generator only emits a `snippets` entry for languages whose `snippets/snippet.<id>.json` exists (currently ABB, Fanuc, KUKA, Motoman).
- Output is written with LF line endings and themes are processed in sorted order, so a regeneration with no source change produces no diff.

## How a theme file works (`python/update_themes.py`)

Each `theme_<Robot>.py` does `from update_themes import *`, builds a `repository` dict of TextMate patterns, then sets `language_i` (id, aliases, extensions) and `config_i` (comments, brackets, folding) before calling the writers.

- `repo_match(repo, match, scope_name, key)`: adds a single-line `match` pattern. If `match` starts with `\`, it is passed through as a raw regex (so a raw regex that would naturally start with `(` or `[` must be written to begin with an escape, e.g. `\-?(?<!...)`). Otherwise it is a **space-separated keyword list** that `matchRegex()` turns into `(?i)\b(KW1|KW2|...)\b` with dots escaped. Trailing/extra spaces in a keyword string produce an empty alternative and break the grammar.
- `repo_begin_end(repo, begin, end, scope_name, key)`: adds a begin/end pattern (comments, strings, blocks).
- Duplicate `key` names are auto-suffixed (`control`, `control1`, `control2`, ...), so the same category can be called repeatedly. Pattern order in the generated grammar follows insertion order. When two rules match at the same position TextMate keeps the earlier one, so put comment/string patterns first and specific regexes (e.g. `DO[10]`) before the plain keyword list that contains `DO`.
- Oniguruma quirk: an isolated `(?i)` inside an alternation applies to everything after it, including later `|` branches. Use `(?i:...)` to scope it.
- Scope names are the module-level constants `name_comment`, `name_string`, `name_numeric`, `name_control`, `name_movements`, `name_builtInTypes`, `name_builtInFcn`, `name_builtInVar`, `name_operator`. These map onto standard VS Code theme scopes (e.g. `keyword.control`, `storage.type.c`); use them rather than inventing new scope strings so highlighting works with any color theme.
- Language ids are used verbatim as file names via `getFileSyntax`/`getFileConfig`/`getScopeName` (lowercased, spaces to `-`), giving `syntaxes/syntax.<id>.json`, `cnfg.<id>.json`, and scope `robodk.<id>`.

Adding a language: copy an existing `theme_*.py`, set a unique `language_i["id"]`, run the generator, and optionally add `snippets/snippet.<id>.json`.

## Testing

There is no automated test suite in the repo. Grammars can be checked headlessly with `vscode-textmate` + `vscode-oniguruma` (tokenize the files in `examples/` and inspect the scopes); otherwise verification is visual:

- Launch the Extension Development Host from VS Code with the `.vscode/launch.json` "Extension" config, or from the repo root:
  ```
  code --disable-extensions --extensionDevelopmentPath=.
  ```
  (`python/run_test.bat` and `run_test_codium.bat` are the Windows equivalents.)
- Open the sample programs in `examples/` (`Program.LS`, `Program.mod`, `Program.src`, `PROGRAM.JBI`, `Prog1.pdl`, `Prog1.pg`, `Prog1.script`, ...) to check highlighting. The `.rdk` files there are RoboDK stations used to produce those programs.

## Packaging

```
npm install -g vsce
vsce package
```

(`create_package_vsix.ps1` wraps this.) The resulting `Industrial-Robots-<version>.vsix` is committed to the repo root and is bundled with RoboDK for Windows. `.vscodeignore` excludes `python/`, `examples/`, `screenshots/`, `*.rdk`, `*.ps1`, and `package_model.json` from the package.
