# tiny-chess-engine

A tiny but complete chess engine for the make.fun **tiny-chess-01**
bounty: one Python file, iterative-deepening alpha-beta search,
packed under 4 KB.

## The engine

- 128-square 0x88 board; make/unmake with incremental Zobrist hashing
  (castling, en-passant and repetition folded into the key)
- alpha-beta with a transposition table, null-move pruning, PVS with
  late-move reductions, killer moves and history ordering
- quiescence search with delta pruning; full evasion search in check
- deterministic search: fixed 200k-node budget with a 4.0 s backstop

## Size rules

- `main.py` is the whole engine: at most 4,096 bytes as committed,
  Python 3.13, standard library only; it reads or execs no other file.
- The rest of the tree stays under 8,192 bytes in all.
- `main.py` is generated, never edited by hand: it is a `#coding:l1`
  marker plus one exec of an lzma payload. Edit `engine_src.py`, then
  repack with:

      makefun compress engine_src.py --out main.py

## Grade it locally

You need Docker and the `makefun` CLI from the competition dev kit.
From inside the kit, run:

    makefun grade-local --kit . --bot <repo> --driver docker

It plays one practice trial against the house engines, replays it to
confirm determinism, and prints the Elo the scorer gives it.
`makefun check` runs the site's pre-submit checks, size caps included.

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Till3005/tiny-chess-engine/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Till3005/tiny-chess-engine/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
