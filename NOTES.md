# NOTES

A self-contained Python chess engine in one file (engine_src.py);
the committed main.py is its lzma-packed image, rebuilt with
`makefun compress engine_src.py --out main.py`.

Board: 128-square 0x88 mailbox; pieces are type 1..6 (P N B R Q K)
with bit 3 set for black; a move is a (from, to, flag, promo) tuple.

Search: iterative-deepening alpha-beta with a Zobrist-keyed
transposition table, null-move pruning, PVS with late-move
reductions, killer moves and history heuristic ordering.

Quiescence: captures/promotions with stand-pat and delta pruning
(DELTA = 200); when in check it expands full evasions instead.

Repetition: O(1) detection via a Zobrist-key counter dict, bumped
on make and restored on unmake; fifty-move clock tracked as well.

Budget: hard 200k-node cap with a 4.0 s wall-clock backstop, so
trials replay identical moves within the server's per-move clock.

Layout: main.py = `#coding:l1` marker + one exec of an lzma
payload, always under 4096 bytes as committed.
