# Require-changes correction list

Only the four audited custody defects were changed:
1. Populated `provenance/SOURCE_HASH_MAP.tsv` with all 48 frozen copied items and their repository paths, SHA-256 values, and MATCH status.
2. Added `closeout/CLEAN_RESTORE_EVIDENCE.txt` inside the archive; final archive hash remains in the transferred outer evidence.
3. Added `figures/render_figures.py`, the exact deterministic renderer/specification for both PNGs, and documented matplotlib 3.10.9. Packaging-time rerender was byte-identical.
4. Regenerated internal and outer custody metadata from the revised bytes. The outer manifest explicitly inventories the standalone PDF. Report content, frozen bytes, CLI behavior, claims, and scientific values did not change.
