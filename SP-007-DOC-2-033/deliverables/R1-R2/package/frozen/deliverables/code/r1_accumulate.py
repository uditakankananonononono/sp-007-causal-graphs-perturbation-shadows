import h5py, numpy as np, pandas as pd, json, time, resource, os
t0 = time.time()
df = pd.read_pickle('/tmp/sp7_obs_frozen.pkl')
folds = json.load(open('/tmp/sp7_folds.json'))
pseudo = json.load(open('/tmp/sp7_ntc_pseudo.json'))
primary = sorted(folds.keys())
desc_targets = sorted(df[(df.qc_pass)&(df.perturbation!='control')].groupby('perturbation').size().pipe(lambda s: s[s>=30]).index)
pidx = {t:i for i,t in enumerate(primary)}
didx = {t:i for i,t in enumerate(desc_targets)}
batches = sorted(df['batch'].unique()); bidx = {b:i for i,b in enumerate(batches)}
NB = len(batches); NG = 8563
# row -> accumulator mapping arrays (int32, -1 = skip)
pert = df['perturbation'].values; batch = df['batch'].values; qc = df['qc_pass'].values
row_P = np.full(len(df), -1, np.int32)   # primary target x batch -> flat
row_D = np.full(len(df), -1, np.int32)   # descriptive target
row_C = np.full(len(df), -1, np.int32)   # control batch
row_NP = np.full(len(df), -1, np.int32)  # NTC pseudo
for i in range(len(df)):
    if not qc[i]: continue
    p = pert[i]
    if p == 'control':
        row_C[i] = bidx[batch[i]]
    else:
        if p in pidx: row_P[i] = pidx[p]*NB + bidx[batch[i]]
        if p in didx: row_D[i] = didx[p]
pseudo_lookup = {}
for k, rows in pseudo.items():
    j = int(k.split('_')[-1])
    for r in rows: pseudo_lookup[r] = j
for r, j in pseudo_lookup.items(): row_NP[r] = j
os.makedirs('results/accum', exist_ok=True)
P = np.memmap('results/accum/P_targetXbatch.f32', dtype='float32', mode='w+', shape=(len(primary)*NB, NG))
D = np.memmap('results/accum/D_target.f32', dtype='float32', mode='w+', shape=(len(desc_targets), NG))
C = np.zeros((NB, NG), np.float32); NP = np.zeros((10, NG), np.float32)
Pn = np.zeros(len(primary)*NB, np.int32); Dn = np.zeros(len(desc_targets), np.int32)
Cn = np.zeros(NB, np.int32); NPn = np.zeros(10, np.int32)
Db = np.zeros((len(desc_targets), NB), np.int16)
# per (primary target x cell-state) counts-free sums? state sums need per-state -> do sums for 3 states
S = np.memmap('results/accum/S_targetXstate.f32', dtype='float32', mode='w+', shape=(len(primary)*3, NG))
state = df['cell_state'].values; sidx = {'T1':0,'T2':1,'T3':2}
row_S = np.full(len(df), -1, np.int32)
for i in range(len(df)):
    if row_P[i] >= 0:
        st = state[i]
        if st in sidx: row_S[i] = pidx[pert[i]]*3 + sidx[st]
with h5py.File('data/raw/ReplogleWeissman2022_K562_essential.h5ad','r') as f:
    X = f['X']; step = 1213
    for lo in range(0, len(df), step):
        hi = min(lo+step, len(df))
        slab = np.asarray(X[lo:hi, :], dtype=np.float32)
        for acc, arr, cnt in ((row_P, P, Pn), (row_D, D, Dn), (row_C, C, Cn), (row_NP, NP, NPn), (row_S, S, None)):
            ids = acc[lo:hi]
            m = ids >= 0
            if not m.any(): continue
            u, inv = np.unique(ids[m], return_inverse=True)
            sums = np.zeros((len(u), NG), np.float32)
            np.add.at(sums, inv, slab[m])
            arr[u] += sums
            if cnt is not None: cnt[u] += np.bincount(inv)[ :len(u)] if len(u) else 0
        if (lo//step) % 40 == 0:
            print(f'{hi}/{len(df)} rows, {time.time()-t0:.0f}s, RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.2f}GB', flush=True)
# batch counts for descriptive
for i in range(len(df)):
    if row_D[i] >= 0: Db[row_D[i], bidx[batch[i]]] += 1
P.flush(); D.flush(); S.flush()
np.save('results/accum/C_controlXbatch.npy', C); np.save('results/accum/NP_pseudo.npy', NP)
np.save('results/accum/Pn.npy', Pn); np.save('results/accum/Dn.npy', Dn)
np.save('results/accum/Cn.npy', Cn); np.save('results/accum/NPn.npy', NPn); np.save('results/accum/Db.npy', Db)
json.dump({'primary': primary, 'descriptive': desc_targets, 'batches': [int(b) for b in batches]},
          open('results/accum/index.json','w'))
print('DONE', time.time()-t0, 's; peak RSS GB', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6, flush=True)
