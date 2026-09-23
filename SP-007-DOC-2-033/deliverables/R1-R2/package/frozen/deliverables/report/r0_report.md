# SP-007 (DOC-2-033) Causal Graphs From Perturbation Shadows - R0 Feasibility

**Verdict: GO to R1 locked benchmark (4/4 gates PASS).**
R0 protocol sha256 f4950b94c2056be69f09016e273b1e7327ed08a9a1d9a9b06ccc42f44b29caba (locked before source inspection).

## G1 primary source - PASS
Replogle et al. 2022 genome-scale Perturb-seq, K562 essential screen. Canonical: figshare.plus article 20029387 v1 (doi:10.25452/figshare.plus.20029387.v1, CC BY 4.0, provider md5s). Working copy: scPerturb harmonized collection, Zenodo record 10044268 (CC-BY-4.0) - md5 d8cba17576d1a8afc0f7d71b79cad0f7 verified exactly (parallel byte-range download, Zenodo throttles single connections ~0.5MB/s).
Content probe: 310,385 cells x 8,563 genes; 2,057 perturbation targets; 10,691 non-targeting control cells; per-cell assignments, guide_id, batch, nperts (multiplet policy), QC fields. Floors (>=20 targets, >=10k cells) exceeded by ~100x/30x.

## G2 replication - PASS
- LINCS L1000 phase I (GSE92742, bulk, shRNA/oe): 8,912 unique genetic-perturbation genes; 706/2,057 primary targets covered = 34.3% (>=30% gate). Metadata + SHA512SUMS grounded; Level-5 matrix download is R1 scope.
- Cross-cell-line: RPE1 screen (same lab) shares 2,055/2,057 targets - supporting, not independence-qualifying.
- Cross-study honest negative: Datlinger et al. 2017 CROP-seq verified (md5 exact) but shares zero target genes with the essential screen - recorded, not hidden.

## G3 reference graphs - PASS
CollecTRI regulons (primary directed reference): 64,515 signed TF->target edges, sha256 c9b622365dd09c6b76e44d6ca7a96f1982918ce6f2811f8fdeafa61fbd87cb50.
OmniPath signed interactions: 86,188 directed edges, sha256 bb516713f584eda4936e9f1fb07f8431dc63bae22f9395423d1e10874671f44f. License caveat: OmniPath integration CC-BY; some upstream constituents carry their own terms - commercial deployment must filter or clear constituents.
Reactome interactors: 124,865 physical pairs (undirected, secondary), sha256 a5ed8376d7da82b0dbfc6f0d243b422b2635482025b74e434d3b9be48cb55e5d.
Incompleteness: references cover TF/signaling subsets; coverage of the 2,057 primary targets will be quantified in R1. Semi-synthetic calibration arm spec frozen regardless.

## G4 environment - PASS
python 3.10.12; anndata 0.11.4 / h5py 3.16.0 / scikit-learn 1.7.2 / numpy 2.2.6 / pandas 2.3.3 / scipy 1.15.3 with wheel sha256 pinned (protocol/environment_ledger.json).

## R1 handoff notes
Lock before any outcome inspection: causal unit = perturbation target (cells as replicates), response = expression change vs NTCs within strata; split by held-out target (random-cell split forbidden); baselines = correlation + perturbation-response mean shift; >=1 mature causal/graph method; directionality vs CollecTRI/OmniPath; top-k precision/calibration; held-out intervention prediction; uncertainty + abstention; failure controls per orchestrator list (shuffled labels, permuted condition, NTCs, expression-matched nulls, guide-efficiency/MOI, cell-state confounding, leakage assertions); contradictions between association and perturbation evidence preserved. An inferred edge is never called causal because a graph method emitted it.
