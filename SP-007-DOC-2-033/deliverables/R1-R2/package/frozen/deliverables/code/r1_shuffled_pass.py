import h5py, numpy as np, pandas as pd, json, time, resource
t0=time.time()
df = pd.read_pickle('/tmp/sp7_obs_frozen.pkl')
idx = json.load(open('results/accum/index.json'))
primary = idx['primary']; batches = idx['batches']; NB=len(batches); NG=8563
bidx = {b:i for i,b in enumerate(batches)}
rng = np.random.default_rng(20260922+2)
pert = df['perturbation'].values; qc = df['qc_pass'].values; batch = df['batch'].values
mask = np.array([p in set(primary) for p in pert]) & qc
rows = np.where(mask)[0]
shuffled_labels = rng.permutation(pert[rows])   # permuted target labels among targeting cells
lab_idx = {t:i for i,t in enumerate(primary)}
row_T = np.full(len(df), -1, np.int32); row_B = np.full(len(df), -1, np.int32)
for r, lab in zip(rows, shuffled_labels):
    row_T[r] = lab_idx[lab]; row_B[r] = bidx[batch[r]]
SH = np.memmap('results/accum/SH_targetXbatch.f32', dtype='float32', mode='w+', shape=(len(primary)*NB, NG))
SHn = np.zeros(len(primary)*NB, np.int32)
with h5py.File('data/raw/ReplogleWeissman2022_K562_essential.h5ad','r') as f:
    X = f['X']; step = 1213
    for lo in range(0, len(df), step):
        hi = min(lo+step, len(df))
        ids = row_T[lo:hi]; m = ids>=0
        if not m.any(): continue
        slab = np.asarray(X[lo:hi,:], dtype=np.float32)
        flat = ids[m]*NB + row_B[lo:hi][m]
        u, inv = np.unique(flat, return_inverse=True)
        sums = np.zeros((len(u), NG), np.float32)
        np.add.at(sums, inv, slab[m])
        SH[u] += sums
        SHn[u] += np.bincount(inv)[:len(u)]
SH.flush(); np.save('results/accum/SHn.npy', SHn)
print('DONE shuffled pass', time.time()-t0, 's; peak RSS GB', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6, flush=True)
