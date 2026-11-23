# NOTES

Search: iterative-deepening alpha-beta, TT, null-move,
LMR, quiescence; qsearch expands evasions in check and
delta-prunes hopeless captures (stand-pat + gain + DELTA < a).

Repetition: O(1) path-hash dict, bumped on make, restored on
unmake; count 2+ scores a draw.

Nodes: fixed 200k budget with a 4.0s backstop; trials pick
identical moves; budget fits the server's per-move clock.

Layout: main.py = `#coding:l1` marker + one exec of an
lzma payload, within 4,096 bytes.

History: v0.2.0 packed; v0.2.1 O(1) repetition;
v0.3.0 delta pruning at r15 budget; 8-0 self-play vs v0.2.x.
