# tiny-chess-01 starter

A working entry to fork: `main.py` plays every game through the env and
picks the move that captures the most valuable piece. It is a template,
not a contender. Replace its one-line choice with a real search.

v0.2.3: node budget cut to 60,000 (env `ENG_NODES`), tuned for the grader's
slow 1-CPU sandbox where 355k nodes/move timed out the 10-second move limit.

v0.2.2: live-play fix — the packed payload's `urllib.request` import is now
aliased as `UR` (module) so `RP`'s `UR.Request`/`UR.urlopen` calls resolve;
the old `q` alias was shadowed by the `q(m)` make-move function and crashed
on the first env call.

v0.2.1: repetition detection is O(1) (a per-position hash-count dict checked
in constant time instead of rescanning move history), and the search's default
node budget is 355,000 (env `ENG_NODES`).

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
