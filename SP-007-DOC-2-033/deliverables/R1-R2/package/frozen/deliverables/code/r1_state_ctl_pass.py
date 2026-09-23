import h5py, numpy as np, pandas as pd, json, time, resource
t0=time.time()
df = pd.read_pickle('/tmp/sp7_obs_frozen.pkl')
NG=8563
qc = df['qc_pass'].values; pert = df['perturbation'].values; state = df['cell_state'].values
sidx = {'T1':0,'T2':1,'T3':2}
row_S = np.full(len(df), -1, np.int32)
for i in range(len(df)):
    if qc[i] and pert[i]=='control' and state[i] in sidx: row_S[i] = sidx[state[i]]
CS = np.zeros((3, NG), np.float32); CSn = np.zeros(3, np.int32)
with h5py.File('data/raw/ReplogleWeissman2022_K562_essential.h5ad','r') as f:
    X = f['X']; step = 1213
    for lo in range(0, len(df), step):
        hi = min(lo+step, len(df))
        ids = row_S[lo:hi]; m = ids>=0
        if not m.any(): continue
        slab = np.asarray(X[lo:hi,:], dtype=np.float32)
        u, inv = np.unique(ids[m], return_inverse=True)
        sums = np.zeros((len(u), NG), np.float32)
        np.add.at(sums, inv, slab[m])
        CS[u] += sums; CSn[u] += np.bincount(inv)[:len(u)]
np.save('results/accum/CS_controlXstate.npy', CS); np.save('results/accum/CSn.npy', CSn)
print('DONE ctl-state pass', time.time()-t0, 's', flush=True)
