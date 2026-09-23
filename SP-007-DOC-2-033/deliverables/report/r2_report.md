# SP-007 (DOC-2-033) R2 - Cross-cell-line transport (K562 -> RPE1)

**Verdict: TRANSPORT FAIL (locked pass rule). Scoring procedure closed; R1 retained as a K562-only atlas.**
R2 protocol sha256 f2231e39380484637366f06c392ba7a71189c859df6eb768bbf534b4ff869256 (locked before any RPE1 scoring; R1 algorithm preregistered unchanged).

## Setup
- RPE1 cohorts built independently with the same rules: 135 strict targets (>=30 cells AND >=2 construct-level guide_ids), 2,016 descriptive, 11,485 NTC, 56 batches. Freeze manifest sha256 b5311740a4823a8db4e1c398534e82f61c757d94a2de283b0267966f48180420.
- Documented pool-count adaptation: frozen n_pools=80 infeasible (80 x 177 = 14,160 > 11,485 controls); executed n_pools = min(80, floor(n_ctl/pool_size)) = 64 pools of 177 cells (median strict-target size), same seed, same tau formula. Gate text untouched.
- RPE1 tau = 0.2361 (frozen formula); 87,880 supported edges (median 493/target).
- Shared-unit overlap frozen before outcome comparison: 115 shared strict targets x 7,226 shared genes (exact gene_name match); overlap sha256 77eb86ad1779a7a2...; all shared genes pass the frozen stratum-A constitutive-expression rule (strata B empty; recorded).

## Transport metrics (target-level bootstrap CIs, 1,000 resamples, seed 20260922; 200 target permutations)
| metric | value | target-permuted null (mean / p95) | expression-matched null | verdict |
|---|---|---|---|---|
| sign agreement | 0.535 [0.528, 0.543] | 0.510 / 0.512 | 0.526 | beats permuted null, but expression-matched null nearly equal - directional structure of expressed genes, not target-specific biology |
| rank correlation (median Spearman) | 0.053 [0.051, 0.054] | 0.011 / 0.019 | - | technically beats null; effect size very weak |
| supported-set precision | 0.0295 [0.0239, 0.0357] | 0.0273 / 0.0325 | - | **FAIL** - supported edge overlap indistinguishable from chance |
| supported-set recall / Jaccard | 0.0875 / 0.0182 | - | - | descriptive |
| calibration: K562-supported also RPE1-supported | 10.96% | 2.73% | - | enrichment present but far below support |

## Interpretation (no causal graph claims; RPE1 = cross-context support only)
- The unchanged preregistered card-support rule does NOT transport across cell lines: per-target supported-edge sets overlap at chance. Whole-transcriptome directional and rank structure carries weak but nonzero cross-line signal (sign agreement, rank correlation above permuted nulls) concentrated in constitutively expressed genes; the discrete supported-edge decisions - the object the review queue ships - do not reproduce.
- This closes the scoring procedure per the locked outcome rule. R1 stands as a K562-only exploratory review-queue atlas (26,525 cards, exploratory not confirmatory, per the R1 calibration history). Cell-state claims remain abstained; no reference-graph claims were attempted in R2.

## Preserved artifacts
RPE1 accumulators, strict scores/SE/null-z/supported mask, NTC pseudo pools, overlap freeze, transport evaluation, all hashes; reproducibility note: identical deterministic pipeline as R1 (R1 rerun reproduced byte-identical sha256).
