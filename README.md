# SP-007 / DOC-2-033 - Causal Graphs From Perturbation Shadows

## Summary (from `SP-007-DOC-2-033/README.md`)


## Status
Closed scoring route after cross-cell-line transport failure. R1 remains a bounded K562 perturbation-response atlas, not a causal graph.

## Useful results
1. A strict 118-target K562 cohort with multi-construct support produced a calibrated exploratory response atlas. A broad 1,971-target descriptive tier is retained with 1,853 guide-replication-unverified flags.
2. Matched-size null recalibration produced 26,525 review-card edges, but LINCS/reference coverage and cell-state sensitivity stopped graph claims.
3. The unchanged card rule failed K562-to-RPE1 transport: sign agreement 0.535, median rank correlation 0.053, and supported-edge precision 0.0295 below null p95 0.0325.

## What is new
Rather than optimizing a perturbation network until it looked plausible, the project created explicit construct-support tiers, matched-null review cards, and then tested the same scoring rule across cell lines. It exposes the difference between a useful within-context response atlas and a portable causal graph.

## Why it matters
Many perturbation-network pipelines turn dense associations into causal-looking edges without independent transport. This project supplies an audit pattern that preserves a useful atlas while refusing the graph claim.

## Working application angle
A perturbation evidence-card generator can label construct support, matched-null calibration, state sensitivity, external-reference coverage and transport status for every proposed edge. It is a review/triage tool, not a causal discovery product.

## Top-lab next question
Can predeclared biological context descriptors identify in advance which response modules transport between cell lines, using independent perturbation datasets and without refitting the edge rule?

## Artifact structure
The overlay contains the compact R0/R1/R2 core packages. Large score matrices are preserved as separate Drive tarballs linked below.

## Drive artifacts
- R0: https://drive.google.com/file/d/1FO9fr9t-C9KyD7W5uG-jk8G_g1X-bXT1/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R1 core: https://drive.google.com/file/d/17AkEBw6HiFZ783RSmVI-PRtSCzR3q_OS/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R1 primary scores: https://drive.google.com/file/d/1yAlH4iGsnLSEFz6T-wH6FezHpR-c-m6k/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R1 descriptive part 0: https://drive.google.com/file/d/1ot_alUqt7xyWPbNlM4hodlSkttoe3hJy/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R1 descriptive part 1: https://drive.google.com/file/d/1cI6TrPZsj3u5aMFP-VjOza-ZNodeQj2K/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R1 descriptive part 2: https://drive.google.com/file/d/1Ah3YduorvqTMZpCphb1UbK0ZaKQ_Dlcj/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R2 core: https://drive.google.com/file/d/1VAvppeL0Qr4f9qyPXAPSEJB2jQCxiLeK/view?usp=drivesdk&authuser=uditakankana%40gmail.com
- R2 RPE1 scores: https://drive.google.com/file/d/1YczlHeLikom4O3KuIupxt4q4Xk4nL53v/view?usp=drivesdk&authuser=uditakankana%40gmail.com

## Contents

- `SP-007-DOC-2-033/` - migrated unchanged from `science-program/projects/SP-007-DOC-2-033` (124 files)

## Provenance

Split out of the `science-program` repository (source commit `028a7141ed5f951a7b6e6517d4e72768d414a560`) on 2026-09-23. Every file is byte-identical to the source; `MIGRATION_MANIFEST.tsv` lists sha256, original path and new path for each of the 124 files.

Part of Udita Phookan's computational science program: every experiment locks its question, validation design, success gate and failure policy before outcome analysis, and negative results are preserved. Program-wide ledgers and standards live in the `science-program-ledger` repository.
