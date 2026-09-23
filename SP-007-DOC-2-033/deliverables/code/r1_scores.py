import numpy as np, json, time
t0=time.time()
idx = json.load(open('results/accum/index.json'))
primary, desc, batches = idx['primary'], idx['descriptive'], idx['batches']
NB, NG = len(batches), 8563
P = np.memmap('results/accum/P_targetXbatch.f32', dtype='float32', mode='r', shape=(len(primary)*NB, NG))
D = np.memmap('results/accum/D_target.f32', dtype='float32', mode='r', shape=(len(desc), NG))
C = np.load('results/accum/C_controlXbatch.npy'); NP = np.load('results/accum/NP_pseudo.npy')
Pn = np.load('results/accum/Pn.npy'); Dn = np.load('results/accum/Dn.npy')
Cn = np.load('results/accum/Cn.npy'); NPn = np.load('results/accum/NPn.npy')
import os as _os
G = np.memmap("results/accum/G_construct.f32", dtype="float32", mode="r", shape=(_os.path.getsize("results/accum/G_construct.f32")//(4*NG), NG))
Gn = np.load('results/accum/Gn.npy')
con = json.load(open('results/accum/construct_index.json'))['constructs']
def cpm_log2(x):  # x: (n, G) counts
    s = x.sum(1, keepdims=True); s[s==0]=1
    return np.log2(x/s*1e6 + 1.0)
def score_vs_control(Xc, cnt, control_log2_by_batch, cell_batch_counts):
    # Xc (nB, G) counts per batch; control_log2_by_batch (NB, G); cell_batch_counts (nB,)
    out = np.zeros(NG, np.float32); wsum = 0.0
    cl = cpm_log2(Xc)
    for b in range(NB):
        n = cell_batch_counts[b]
        if n <= 0 or Cn[b] == 0: continue
        out += n * (cl[b] - control_log2_by_batch[b])
        wsum += n
    return out / max(wsum, 1)
CtlL2 = cpm_log2(C)                       # (NB, G) per-batch control
CtlL2_pooled = cpm_log2(C.sum(0, keepdims=True))[0]
# primary scores
Spri = np.zeros((len(primary), NG), np.float32)
for i in range(len(primary)):
    Spri[i] = score_vs_control(P[i*NB:(i+1)*NB], None, CtlL2, Pn[i*NB:(i+1)*NB])
# construct-level scores vs pooled control (documented approximation)
Gcl = cpm_log2(np.asarray(G))
SE = np.zeros((len(primary), NG), np.float32); NCON = np.zeros(len(primary), np.int32)
from collections import defaultdict
by_target = defaultdict(list)
for j, c in enumerate(con): by_target[c['target']].append(j)
for i, t in enumerate(primary):
    js = by_target[t]; NCON[i] = len(js)
    if len(js) >= 2:
        sc = Gcl[js] - CtlL2_pooled
        SE[i] = sc.std(0, ddof=1) / np.sqrt(len(js))
# descriptive scores (pooled control; batch-mixing documented)
Sdesc = cpm_log2(np.asarray(D)) - CtlL2_pooled
# NTC pseudo scores -> tau
NPcl = cpm_log2(NP)
pseudo_scores = NPcl - CtlL2_pooled
abs_ps = np.abs(pseudo_scores)
med = np.median(abs_ps); mad = np.median(np.abs(abs_ps - med))
tau = med + 2*mad
np.save('results/atlas_primary_scores.npy', Spri)
np.save('results/atlas_primary_construct_se.npy', SE)
np.save('results/atlas_primary_nconstructs.npy', NCON)
np.save('results/atlas_descriptive_scores.npy', Sdesc.astype(np.float32))
np.save('results/atlas_ntc_pseudo_scores.npy', pseudo_scores.astype(np.float32))
json.dump({'tau': float(tau), 'ntc_median_abs': float(med), 'ntc_mad': float(mad),
           'note': 'tau = median(|NTC pseudo-intervention effects|) + 2*MAD, per locked protocol; computed before any evaluation'},
          open('results/tau.json','w'))
with open('results/gene_names.txt','w') as fh:
    import h5py
    with h5py.File('data/raw/ReplogleWeissman2022_K562_essential.h5ad','r') as f:
        for g in f['var/gene_name'][:]: fh.write((g.decode() if isinstance(g,bytes) else str(g))+'\n')
print('scores done', time.time()-t0, 's; tau =', round(float(tau),4))
print('primary score sanity: |score|>tau edges per target:', int((np.abs(Spri)>tau).sum()), 'of', Spri.size)
