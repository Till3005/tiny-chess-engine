# NOTES

Search: iterative-deepening alpha-beta, TT, null-move pruning,
LMR, quiescence; in check, qsearch expands full evasions.

Repetition: O(1) path-hash dict (hash counts), bumped on make,
restored on unmake; count 2+ scores a draw.

Nodes: fixed 355k budget (env ENG_NODES), never a clock: replayed
trials must pick identical moves and 355k fits 10s/move.

Layout: main.py = `#tc1 v0.2.3` marker + one exec of an
lzma+base85 packed engine, within 4,096 bytes.

History: v0.2.0 packed layout; v0.2.1 O(1) repetition +
355k nodes; v0.2.2 urllib alias (UR) live-play fix;
v0.2.3 docs only, payload unchanged.
