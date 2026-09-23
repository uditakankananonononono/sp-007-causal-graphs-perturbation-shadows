# SP-007 (DOC-2-033) Causal Graphs From Perturbation Shadows - R1

**Outcome: BOUNDED PERTURBATION-RESPONSE ATLAS (locked stop arm).** No transport claims, no graph claims, no causal edge claims. Every emitted edge is review-queue evidence with uncertainty; unlisted edges are UNLABELED, not negative.
R1 protocol sha256 7836cb204b997335c2abfbdacf07b6ef865e6500256b52ad91b91766218a85dc (locked before scoring).

## Why the stop arm fired (two independent grounds)
1. LINCS Level-5 access failure (environmental nontransport result): GSE92742 Level-5 gctx.gz is 21,328,033,748 bytes vs 15GB free disk; macchiato.clue.io S3 AccessDenied for anonymous reads; gzip is not range-sliceable; iLINCS is a different aggregation, not Level-5 per the locked gate. LINCS deferred to an environment that can hold it.
2. Reference coverability below the locked floor: only 31/118 primary targets are CollecTRI/OmniPath sources; E* = 142 edges / 25 evaluable targets (< 500 edges / < 50 targets). Graph work would have stopped here regardless.

## Cohort (frozen before scoring)
- 310,385 QC-pass cells (10,691 NTC); QC thresholds from the lock applied verbatim (mostly vacuous on this pre-QC harmonized file - documented).
- Primary: 118 targets with >=30 cells AND >=2 distinct construct-level guide_ids. Orchestrator ruling: paired-guide halves are co-delivered, not independent replicates (paired-guide semantic collision documented as cohort limitation, gate text untouched).
- Descriptive tier: 1,971 targets (>=30 cells); 1,853 single-construct targets flagged GUIDE-REPLICATION-UNVERIFIED; uncertainty clustered at construct/target and cell/batch.
- 5-fold split by held-out target (seed 20260922), zero fold overlap asserted. Freeze manifest+folds sha256 2a221605ffe9fce16fa8913a6226d0d212a6d4b955ee6c5d123877fd7a4cadf7.

## Estimator and calibration (preserved failures inside)
- Response score: pooled-count rate vs batch-matched NTC control rate. Naive per-(target x batch) CPM ratios were noise-dominated (median 2-3 cells per stratum; 87% of edges cleared tau) - preserved failure; documented stabilization, gate text untouched.
- tau: locked formula (median + 2*MAD over NTC pseudo-interventions). First calibration on ~1,069-cell pools gave tau=0.0867; the shuffled-label control exposed it (51.6% of shuffled edges above tau) - preserved failure. Pools re-drawn at matched size (121 cells x 80 disjoint, seed 20260922+4): tau=0.269.

## Controls battery
| control | verdict | key number |
|---|---|---|
| shuffled labels | PASS (matched calibration) | 10.2% vs 15.4% vs 18.2% (shuffled/primary/NTC-null) above tau; note: fraction-above-tau alone does not discriminate, operative criterion adds construct-CI + per-gene null z |
| NTC pseudo-interventions | PASS | null median \|score\| 0.116 |
| self-edge positive control | PASS | median self score -0.937; 98% below -tau; expression-matched nulls ~0 |
| permuted strata | PASS | score correlation 0.994 |
| leave-one-batch-out | PASS | 0.99977 (118 targets) |
| cell state | REVIEW (documented) | pooled-vs-state correlation 0.61; ~40-cell state pools underpowered at this cell count; per-state claims abstain |
| MOI | DOCUMENTED | vacuous (all targeting cells nperts==1) |
| leakage assertions | PASS | zero fold overlap; pseudo rows verified controls |

## Atlas output
- 26,525 supported edges (median 142/target, p10 30) under: |score|>0.269 AND 95% construct-CI excludes 0 AND per-gene NTC-null |z|>=1.96.
- Evidence cards: 26,525 perturbation-supported, 2,011 association-only (|r|>=0.5), 2 reference-discordant (sign contradictions preserved, not resolved).
- Reproducibility: accumulation rerun reproduces identical sha256 (see gate_evaluation_r1 / delivery note).

## Commercial artifact
Review queue (3 card classes, TSV + JSON summary); licenses (CollecTRI CC-BY, Zenodo CC-BY-4.0, LINCS NIH public; OmniPath upstream-constituent caveat for commercial use documented); runtime/memory (full pipeline <10 min, 2 cores, 0.60GB peak); reviewer-time protocol frozen (top-50 cards/target by |null_z|, accept/reject/abstain, 10% double-review); monitoring (drift of per-target supported counts vs this freeze) and rollback (hashed artifacts, restorable from tarballs + Zenodo 10044268).

## Boundaries
Product is a review queue for follow-up experiment prioritization. It does not establish causality, does not rank graph edges against reference truth, makes no transport claims across studies or modalities. RPE1 cross-cell-line transport can motivate a new R2 protocol after R1 closes; it is same-lab/platform, never independent replication.
