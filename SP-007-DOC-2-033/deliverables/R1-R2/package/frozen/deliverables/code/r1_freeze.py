import numpy as np, pandas as pd, json, hashlib
df = pd.read_pickle('/tmp/sp7_obs_raw.pkl')
SEED = 20260922
ngenes = pd.to_numeric(df['ngenes'], errors='coerce')
ncounts = pd.to_numeric(df['ncounts'], errors='coerce')
mito = pd.to_numeric(df['percent_mito'], errors='coerce')
nperts = pd.to_numeric(df['nperts'], errors='coerce')
qc = (ngenes >= 500) & (ncounts >= 1000) & (mito <= 20) & (nperts == 1) & (~df['perturbation'].str.contains(r'\+', regex=True))
df['qc_pass'] = qc
manifest = {'seed': SEED, 'n_cells_total': int(len(df)), 'n_qc_pass': int(qc.sum()),
 'qc_fail_breakdown': {'ngenes<500': int((ngenes<500).sum()), 'ncounts<1000': int((ncounts<1000).sum()),
   'mito>20': int((mito>20).sum()), 'nperts!=1': int((nperts!=1).sum()),
   'plus_named': int(df['perturbation'].str.contains(r'\+', regex=True).sum())},
 'qc_note': 'thresholds from locked protocol applied verbatim; most are vacuous on this pre-QC harmonized file (documented, not weakened)'}
q = df[df.qc_pass]
ctl = q[q.perturbation=='control']
# cell-state terciles from controls
umi = pd.to_numeric(ctl['core_adjusted_UMI_count'], errors='coerce')
t1, t2 = np.nanpercentile(umi, [100/3, 200/3])
df['cell_state'] = pd.cut(pd.to_numeric(df['core_adjusted_UMI_count'], errors='coerce'),
                          [-np.inf, t1, t2, np.inf], labels=['T1','T2','T3']).astype(str)
manifest['cell_state_tercile_edges'] = [float(t1), float(t2)]
# target inclusion
tg = q[q.perturbation!='control'].groupby('perturbation').agg(n=('qc_pass','size'), guides=('guide_id','nunique'))
inc = tg[(tg.n >= 30) & (tg.guides >= 2)].index.tolist()
manifest['n_targets_screen'] = int(len(tg)); manifest['n_targets_included'] = int(len(inc))
manifest['excluded_targets_lowcell_or_lowguide'] = sorted(set(tg.index)-set(inc))[:50]
# folds by target
rng = np.random.default_rng(SEED)
perm = rng.permutation(len(inc))
folds = {}
for i, t in enumerate(sorted(inc)):
    folds[t] = int(np.argsort(np.argsort(perm))[sorted(inc).index(t)] % 5)
manifest['fold_sizes'] = {str(k): sum(1 for v in folds.values() if v==k) for k in range(5)}
# NTC pseudo-interventions: 10 pseudo-targets
ctl_idx = np.where(df['perturbation'].values=='control')[0]
rng2 = np.random.default_rng(SEED+1)
assign = rng2.integers(0, 10, size=len(ctl_idx))
pseudo = {f'NTC_pseudo_{i}': ctl_idx[assign==i].tolist() for i in range(10)}
manifest['ntc_pseudo_sizes'] = {k: len(v) for k, v in pseudo.items()}
json.dump(manifest, open('results/r1_freeze_manifest.json','w'), indent=1)
np.save('/tmp/sp7_qc_pass.npy', df['qc_pass'].values)
json.dump(folds, open('/tmp/sp7_folds.json','w'))
json.dump(pseudo, open('/tmp/sp7_ntc_pseudo.json','w'))
df[['perturbation','batch','guide_id','cell_state','qc_pass']].to_pickle('/tmp/sp7_obs_frozen.pkl')
blob = json.dumps(manifest, sort_keys=True).encode() + json.dumps(folds, sort_keys=True).encode()
print('freeze_manifest+folds sha256:', hashlib.sha256(blob).hexdigest())
print(json.dumps(manifest, indent=1)[:800])
