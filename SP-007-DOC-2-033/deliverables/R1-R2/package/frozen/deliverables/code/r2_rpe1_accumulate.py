import h5py, numpy as np, pandas as pd, json, time, resource
t0=time.time()
df = pd.read_pickle('/tmp/sp7_rpe1_obs.pkl')
coh = json.load(open('/tmp/sp7_rpe1_cohorts.json'))
strict, desc = coh['strict'], coh['descriptive']
sidx = {t:i for i,t in enumerate(strict)}; didx = {t:i for i,t in enumerate(desc)}
batches = sorted(df['batch'].unique()); bidx = {b:i for i,b in enumerate(batches)}
NB, NG = len(batches), 8749
pert = df['perturbation'].values; batch = df['batch'].values; qc = df['qc_pass'].values; guide = df['guide_id'].values
row_S = np.full(len(df), -1, np.int32); row_D = np.full(len(df), -1, np.int32); row_C = np.full(len(df), -1, np.int32)
for i in range(len(df)):
    if not qc[i]: continue
    p = pert[i]
    if p == 'control': row_C[i] = bidx[batch[i]]
    else:
        if p in sidx: row_S[i] = sidx[p]*NB + bidx[batch[i]]
        if p in didx: row_D[i] = didx[p]
# constructs for strict
q = df[qc & df['perturbation'].isin(strict)]
constructs = sorted(q.groupby(['perturbation','guide_id']).groups.keys())
cidx = {c:i for i,c in enumerate(constructs)}
row_G = np.full(len(df), -1, np.int32)
for i in range(len(df)):
    if qc[i] and pert[i] in sidx: row_G[i] = cidx[(pert[i], guide[i])]
# matched pseudo pools: n_pools = min(80, floor(n_ctl/177))
ctl_rows = np.where((pert=='control') & qc)[0]
POOL = 177; NP_ = min(80, len(ctl_rows)//POOL)
rng = np.random.default_rng(20260922+4)
perm = rng.permutation(ctl_rows)[:NP_*POOL]
row_P = np.full(len(df), -1, np.int32)
for j, r in enumerate(perm): row_P[r] = j//POOL
import os
os.makedirs('results/accum_rpe1', exist_ok=True)
S = np.memmap('results/accum_rpe1/S_targetXbatch.f32', dtype='float32', mode='w+', shape=(len(strict)*NB, NG))
D = np.memmap('results/accum_rpe1/D_target.f32', dtype='float32', mode='w+', shape=(len(desc), NG))
G = np.memmap('results/accum_rpe1/G_construct.f32', dtype='float32', mode='w+', shape=(len(constructs), NG))
MP = np.memmap('results/accum_rpe1/MP_pseudo.f32', dtype='float32', mode='w+', shape=(NP_, NG))
C = np.zeros((NB, NG), np.float32)
Sn = np.zeros(len(strict)*NB, np.int32); Dn = np.zeros(len(desc), np.int32)
Gn = np.zeros(len(constructs), np.int32); Cn = np.zeros(NB, np.int32)
Gb = np.zeros((len(constructs), NB), np.int32); MPb = np.zeros((NP_, NB), np.int32)
for i in range(len(df)):
    if row_G[i]>=0: Gb[row_G[i], bidx[batch[i]]] += 1
    if row_P[i]>=0: MPb[row_P[i], bidx[batch[i]]] += 1
with h5py.File('data/raw/ReplogleWeissman2022_rpe1.h5ad','r') as f:
    X = f['X']; step = 1213
    for lo in range(0, len(df), step):
        hi = min(lo+step, len(df))
        slab = np.asarray(X[lo:hi,:], dtype=np.float32)
        for acc, arr, cnt in ((row_S,S,Sn),(row_D,D,Dn),(row_C,C,Cn),(row_G,G,Gn),(row_P,MP,None)):
            ids = acc[lo:hi]; m = ids>=0
            if not m.any(): continue
            u, inv = np.unique(ids[m], return_inverse=True)
            sums = np.zeros((len(u), NG), np.float32)
            np.add.at(sums, inv, slab[m])
            arr[u] += sums
            if cnt is not None: cnt[u] += np.bincount(inv)[:len(u)]
        if (lo//step)%40==0: print(f'{hi}/{len(df)} {time.time()-t0:.0f}s RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6:.2f}GB', flush=True)
S.flush(); D.flush(); G.flush(); MP.flush()
np.save('results/accum_rpe1/Sn.npy', Sn); np.save('results/accum_rpe1/Dn.npy', Dn)
np.save('results/accum_rpe1/Gn.npy', Gn); np.save('results/accum_rpe1/C.npy', C)
np.save('results/accum_rpe1/Cn.npy', Cn); np.save('results/accum_rpe1/Gb.npy', Gb)
np.save('results/accum_rpe1/MPb.npy', MPb)
json.dump({'strict': strict, 'descriptive': desc, 'batches': [int(b) for b in batches],
 'constructs': [{'target': t, 'guide_id': g, 'n_cells': int(Gn[i])} for i,(t,g) in enumerate(constructs)],
 'n_pools': int(NP_), 'pool_size': POOL,
 'pool_note': 'frozen rule n_pools=80 infeasible (80x177=14,160 > 11,485 controls); executed n_pools=min(80, floor(n_ctl/pool_size))=64 - documented adaptation, gate text untouched'},
 open('results/accum_rpe1/index.json','w'))
print('DONE', time.time()-t0, 's; pools:', NP_, 'peak RSS GB', resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6, flush=True)
