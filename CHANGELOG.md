# Change Log

All notable changes to the "industrial-robots" extension will be documented in this file.

## 0.2.1

- ABB RAPID `.mod` modules opened as XML, because VS Code's built-in XML language also claims `.mod`. They now open as ABB. The same fix applies to Denso `.pac` (was JavaScript), Stäubli `.ltx` (was LaTeX) and Chaifu `.cfg` (was Properties). Real XML, JavaScript, LaTeX and INI files keep their language.

## 0.2.0

- Syntax highlighting for the output of every RoboDK post processor. 37 new languages: Aerotech AeroBasic, Allen Bradley Logix5000, Annin Robotics, Brooks GPL (Precise, MARS), Chaifu, CLOOS, Comau .lsv, CPC, CRP, Denso PAC, Elite Robots EC, Estun RCS2 and RCS3, Flexiv, G-code, GSK, HIWIN, Huashu, Hyundai, Inexbot, Inovance, KEBA KAIRO, Mecademic, Mitsubishi MELFA BASIC and MOVEMASTER, Nachi / OTC, NEWKer, Panasonic G3, QJAR, Rainbow Robotics, Robostar, Siasun (SPF and JOB), Siemens Sinumerik, Techman TMscript, Toshiba, Turin and Yamaha.
- Automatic language detection from the file content when several controllers share an extension (.prg, .pg, .script, .jbi, .job, .cnc, .txt, three-digit Nachi/Hyundai extensions...). Can be turned off with `industrialRobots.detectLanguage`.
- Post processor outputs in Python, Lua, JSON or XML open with VS Code's built-in languages (.drl, .jks, .aubo, .kr2, .rcp, .zu...).
- More complete grammars for the existing languages: ABB arc welding and ROKAE, Comau Nodal, Fanuc, Kawasaki and Astorino, KUKA splines and data sets, Motoman, Stäubli VAL3, Universal Robots URCaps, Omron V+ (.vb1, .v2) and Epson.
- The grammars are now plain JSON files; the Python generator was removed. `npm test` checks every grammar against sample programs from the RoboDK post processors.

## 0.1.6

- New languages: Epson SPEL+ (`.prg`) and Omron/Adept V+ (`.pg`) with syntax highlighting and snippets (contributed in #12).
- Fanuc: `IF`/`THEN`/`ELSE`/`ENDIF`/`JMP`/`LBL`, registers (`R[n]`, `TIMER[n]`, ...), `CNTnn` and `nn%` speeds are highlighted; `UFRAME[n]` works; `DO[10]`, `UTOOL[10]`, `PR[12,3]` and other multi-digit indices are accepted.
- Motoman: `OT#(n)`, `IN#(n)` and `TL#(n)` accept multi-digit numbers.
- KUKA: `EXT` no longer matches inside identifiers such as `NEXT_IDX`; `$VEL.CP` style system variables are highlighted as a whole.
- Universal Robots: `elif`, `return`, `thread`, `movep`, `servoj`, `textmsg`, the I/O, socket, kinematics and math functions are highlighted.
- Operators (`:=`, `==`, `<>`, `<=`, `>=`, `+`, `-`, `*`, `/`, `<`, `>`) are highlighted for ABB, Comau, Fanuc, Kawasaki and KUKA.
- Digits inside identifiers (`XP1`, `var_1`) are no longer colored as numbers.
- Folding markers fixed for Comau, Fanuc, Kawasaki and Universal Robots.
- Snippets: fixed duplicate keys that hid the Fanuc `J` and Motoman `movj` snippets, the ABB `CONST/PERS/VAR` choice and `FUNC` definition.
- Generator: deterministic output (LF line endings, sorted language order), only references snippet files that exist.

## 0.1.5

- Universal Robots script file extension fix, Yaskawa Motoman target highlighting fix, Fanuc `!` operator inside `IF` statements.

## 0.1.2

- Initial public release, released on 2019-09-11 with RoboDK 4.0.0
