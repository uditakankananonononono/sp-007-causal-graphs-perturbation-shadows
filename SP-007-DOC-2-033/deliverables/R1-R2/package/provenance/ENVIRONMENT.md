# Environment notes

Frozen analysis environment is preserved verbatim in `frozen/deliverables/protocol/environment_ledger.json`: Python 3.10.12; anndata 0.11.4; h5py 3.16.0; scikit-learn 1.7.2; numpy 2.2.6; pandas 2.3.3; scipy 1.15.3; Linux x86_64. Wheel hashes are recorded there.

Packaging environment: Linux x86_64; Python standard library for CLI and tests; pdfTeX for the PDF; matplotlib 3.10.9 for two deterministic figures. Packaging does not invoke the scientific pipeline.

Figure rerender contract: `python3 figures/render_figures.py` under matplotlib 3.10.9. The renderer consumes only two frozen JSON files, embeds each source SHA-256 in the PNG metadata and image footer, and rewrites matching source-hash sidecars. A packaging-time rerender produced byte-identical PNGs.
