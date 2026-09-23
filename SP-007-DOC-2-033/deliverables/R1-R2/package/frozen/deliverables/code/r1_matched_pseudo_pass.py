import h5py, numpy as np, pandas as pd, json, time, resource
t0=time.time()
df = pd.read_pickle('/tmp/sp7_obs_frozen.pkl')
NG=8563
rng = np.random.default_rng(20260922+4)
ctl_rows = np.where((df['perturbation'].values=='control') & df['qc_pass'].values)[0]
# 100 matched-size pseudo-targets: 121 cells each (median primary target size), disjoint
perm = rng.permutation(ctl_rows)[:80*121]
row_P = np.full(len(df), -1, np.int32)
for j, r in enumerate(perm): row_P[r] = j//121
MP = np.memmap('results/accum/MP_pseudo121.f32', dtype='float32', mode='w+', shape=(80, NG))
batch = df['batch'].values
import json as j2
idx = j2.load(open('results/accum/index.json')); bidx={b:i for i,b in enumerate(idx['batches'])}
MPb = np.zeros((80, len(bidx)), np.int32)
for j, r in enumerate(perm): MPb[j//121, bidx[batch[r]]] += 1
with h5py.File('data/raw/ReplogleWeissman2022_K562_essential.h5ad','r') as f:
    X = f['X']; step=1213
    for lo in range(0, len(df), step):
        hi = min(lo+step, len(df))
        ids = row_P[lo:hi]; m = ids>=0
        if not m.any(): continue
        slab = np.asarray(X[lo:hi,:], dtype=np.float32)
        u, inv = np.unique(ids[m], return_inverse=True)
        sums = np.zeros((len(u), NG), np.float32)
        np.add.at(sums, inv, slab[m])
        MP[u] += sums
MP.flush(); np.save('results/accum/MPb.npy', MPb)
print('DONE matched pseudo pass', time.time()-t0, 's', flush=True)
