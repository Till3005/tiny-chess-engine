# NOTES

Search: iterative-deepening alpha-beta, TT, null-move,
LMR, quiescence; qsearch expands evasions in check.

Repetition: O(1) path-hash dict, bumped on make, restored on
unmake; count 2+ scores a draw.

Nodes: fixed 355k budget, never a clock: trials pick identical
moves; 355k fits 10s/move.

Layout: main.py = `#tc1 v0.2.4` marker + one exec of an
lzma+base85 payload, within 4,096 bytes.

History: v0.2.0 packed; v0.2.1 O(1) repetition + 355k nodes;
v0.2.2 urllib alias fix; v0.2.3/4 docs only.
v0.3.0 delta-pruned quiescence (hopeless captures skipped);
r15 config kept: BUD 200k nodes + TS 4.0s backstop. 8-0
self-play vs v0.2.x at equal node budget.
