# Change Log

All notable changes to the "industrial-robots" extension will be documented in this file.

## 0.1.6

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
