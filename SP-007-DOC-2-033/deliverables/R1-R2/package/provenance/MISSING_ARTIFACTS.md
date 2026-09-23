# Missing or intentionally external artifacts

No existing repository artifact needed for the bounded package was missing.

Large source matrices are intentionally external and were not duplicated:
- `ReplogleWeissman2022_K562_essential.h5ad`, MD5 `d8cba17576d1a8afc0f7d71b79cad0f7`, 1,546,729,675 bytes.
- `ReplogleWeissman2022_rpe1.h5ad`, MD5 `cc7f1ec50aeb3a3e1b4a6cfa713d80fa`.
- Canonical raw K562 file provider MD5 `4f1122ce1c7f13299a68df6459a266d3`.

Reference tables and LINCS files remain external under hashes in the frozen manifests. This compact package does not claim full scientific-pipeline rerunnability without those external bytes.
