# tiny-chess-01 starter

A working entry to fork: `main.py` plays every game through the env and
picks the move that captures the most valuable piece. It is a template,
not a contender. Replace its one-line choice with a real search.

v0.3.0: budget back up to 70,000 nodes with exact Zobrist keys (castling +
en-passant mixed into the hash), transposition-table best-move ordering,
PVS at the root and quiescence delta pruning — 3/6 on practice trial-0 at
under 1 s/move locally. Incremental-eval fixes: material, king squares,
fifty/repetition counts and the Zobrist key are all updated in make/unmake,
so no position is rescanned during search.

## The size rule

- `main.py` is the whole engine: at most 4,096 bytes as committed,
  Python 3.13, standard library only. It reads, imports or execs no other
  file in the repository.
- Every byte counts: comments, whitespace, docstrings.
- Compression is allowed and counted. A `main.py` that unpacks and execs
  a compressed payload (`lzma`, `zlib`) is fine; the payload and the
  unpacker are both part of its 4,096 bytes.
- The rest of the tree (this README, LICENSE) is at most 8,192 bytes in
  all, and no file over 4,096. MIT, BSD, ISC and 0BSD licences fit.
- Search to a fixed depth or node count, never a clock: a final
  contender's trials are replayed and must play the same moves.

## Grade it locally

You need Docker and the `makefun` CLI. Download the competition's dev
kit, unpack it, and from inside it run:

    makefun grade-local --kit . --bot <your repository> --driver docker

It plays one practice trial against the house engines, replays it, and
prints the Elo the scorer gives it. Before you submit, `makefun check`
runs the site's own pre-submit checks, size caps included.

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/Till3005/tiny-chess-engine/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/Till3005/tiny-chess-engine/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
