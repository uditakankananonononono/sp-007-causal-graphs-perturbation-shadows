# DOC-2-033 combined R1/R2 submission package

Packaging-only backfill of the frozen bounded K562 perturbation-response atlas and K562-to-RPE1 transport test.

**Conclusion:** K562 atlas exploratory/bounded; RPE1 transport failed. No general perturbation atlas, validated causal map, or successful cross-cell-line transfer is claimed.

Contents:
- `paper/` - 21-page A4 PDF and LaTeX source
- `frozen/` - complete repository project deliverables and README, unchanged
- `figures/` - deterministic views of frozen JSON, with source-hash sidecars
- `cli/` - read-only exact query/export tool
- `tests/` - golden and custody tests
- `provenance/` - source chain, environment, external/missing registry, source-hash map
- `closeout/` - clean-restore evidence and closeout ledger
- `MANIFEST.sha256` and `PACKAGE_MANIFEST.json` - package custody

Restore and verify:
```
tar xzf DOC-2-033-R1-R2-package.tar.gz
cd DOC-2-033-R1-R2-package
sha256sum -c MANIFEST.sha256
python3 cli/doc2033_review.py verify
python3 tests/run_tests.py
```

Large source matrices remain external references with frozen hashes. No repository push or Drive upload was performed.
