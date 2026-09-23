import h5py, numpy as np, pandas as pd, json, time, resource
t0 = time.time()
df = pd.read_pickle('/tmp/sp7_obs_frozen.pkl')
folds = json.load(open('/tmp/sp7_folds.json'))
primary = sorted(folds.keys()); pidx = {t:i for i,t in enumerate(primary)}
NG = 8563
q = df[(df.qc_pass) & (df.perturbation.isin(primary))]
constructs = sorted(q.groupby(['perturbation','guide_id']).ngroups and q.groupby(['perturbation','guide_id']).groups.keys())
cidx = {c:i for i,c in enumerate(constructs)}
NC = len(constructs)
pert = df['perturbation'].values; guide = df['guide_id'].values; qc = df['qc_pass'].values
row_G = np.full(len(df), -1, np.int32)
for i in range(len(df)):
    if qc[i] and pert[i] in pidx:
        row_G[i] = cidx[(pert[i], guide[i])]
G = np.memmap('results/accum/G_construct.f32', dtype='float32', mode='w+', shape=(NC, NG))
Gn = np.zeros(NC, np.int32)
with h5py.File('data/raw/ReplogleWeissman2022_K562_essential.h5ad','r') as f:
    X = f['X']; step = 1213
    for lo in range(0, len(df), step):
        hi = min(lo+step, len(df))
        ids = row_G[lo:hi]; m = ids >= 0
        if not m.any(): continue
        slab = np.asarray(X[lo:hi, :], dtype=np.float32)
        u, inv = np.unique(ids[m], return_inverse=True)
        sums = np.zeros((len(u), NG), np.float32)
        np.add.at(sums, inv, slab[m])
        G[u] += sums
        Gn[u] += np.bincount(inv)[:len(u)]
G.flush()
np.save('results/accum/Gn.npy', Gn)
json.dump({'constructs': [{'target': t, 'guide_id': g, 'n_cells': int(Gn[i])} for i,(t,g) in enumerate(constructs)]},
          open('results/accum/construct_index.json','w'))
print('DONE', NC, 'constructs,', time.time()-t0, 's; peak RSS GB', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6, flush=True)
