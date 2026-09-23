# DOC-2-033 frozen review CLI

This is a read-only query/export interface over the three frozen R1 card TSVs and the frozen R2 transport record. It has no scoring, ranking, threshold, model, network, or write path. It never changes or creates a scientific result.

Commands:

```
python3 cli/doc2033_review.py summary
python3 cli/doc2033_review.py schema
python3 cli/doc2033_review.py lookup perturbation-supported TARGET GENE
python3 cli/doc2033_review.py row perturbation-supported 1
python3 cli/doc2033_review.py export perturbation-supported --format tsv
python3 cli/doc2033_review.py verify
```

`lookup` is an exact target/gene key query. `row` addresses the 1-based row after a fixed lexical sort by target, gene, class, then the complete stored row. `export` emits the whole selected frozen class in that same stable order. There is no predicate, threshold, top-N, score order, or user-selectable sort. Output is UTF-8 with LF endings. JSON keys are sorted. TSV fields are passed through as stored.

The three classes are separate frozen artifacts and have different schemas. Use `schema` before programmatic use. Python 3.8+ standard library only. No network.
