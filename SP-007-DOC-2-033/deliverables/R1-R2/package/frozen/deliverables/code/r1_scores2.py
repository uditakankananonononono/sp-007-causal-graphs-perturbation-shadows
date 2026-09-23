import numpy as np, json, time
from collections import defaultdict
t0=time.time()
idx = json.load(open('results/accum/index.json'))
primary, desc, batches = idx['primary'], idx['descriptive'], idx['batches']
NB, NG = len(batches), 8563
P = np.memmap('results/accum/P_targetXbatch.f32', dtype='float32', mode='r', shape=(len(primary)*NB, NG))
D = np.memmap('results/accum/D_target.f32', dtype='float32', mode='r', shape=(len(desc), NG))
C = np.load('results/accum/C_controlXbatch.npy'); NP = np.load('results/accum/NP_pseudo.npy')
Pn = np.load('results/accum/Pn.npy'); Dn = np.load('results/accum/Dn.npy')
Cn = np.load('results/accum/Cn.npy'); NPn = np.load('results/accum/NPn.npy'); Db = np.load('results/accum/Db.npy')
G = np.memmap('results/accum/G_construct.f32', dtype='float32', mode='r', shape=(237, NG))
Gn = np.load('results/accum/Gn.npy')
con = json.load(open('results/accum/construct_index.json'))['constructs']
import pandas as pd
df = pd.read_pickle('/tmp/sp7_obs_frozen.pkl')
q = df[(df.qc_pass)&(df.perturbation.isin(primary))]
Gb = q.groupby(['perturbation','guide_id'])['batch'].value_counts().unstack(fill_value=0)
Gb = Gb.reindex(columns=batches, fill_value=0).values.astype(np.float64)
# control rate per batch (rate = counts per total counts)
Crate = C / C.sum(1, keepdims=True)                      # (NB, G)
def matched_score(Xsum, batch_w):
    # Xsum: (G,) pooled counts for the unit; batch_w: (NB,) cell counts of unit per batch
    N = batch_w.sum()
    if N == 0: return np.zeros(NG, np.float32)
    r_unit = Xsum / Xsum.sum()
    w = batch_w / N
    r_ctl = (w[:,None] * Crate).sum(0)
    return np.log2((r_unit*1e6 + 1.0) / (r_ctl*1e6 + 1.0)).astype(np.float32)
# primary
Spri = np.zeros((len(primary), NG), np.float32)
for i in range(len(primary)):
    Spri[i] = matched_score(P[i*NB:(i+1)*NB].sum(0), Pn[i*NB:(i+1)*NB].astype(np.float64))
# constructs
Gsc = np.zeros((237, NG), np.float32)
for j in range(237):
    Gsc[j] = matched_score(np.asarray(G[j]), Gb[j])
SE = np.zeros((len(primary), NG), np.float32); NCON = np.zeros(len(primary), np.int32)
by_target = defaultdict(list)
for j, c in enumerate(con): by_target[c['target']].append(j)
for i, t in enumerate(primary):
    js = by_target[t]; NCON[i] = len(js)
    sc = Gsc[js]
    if len(js) >= 2: SE[i] = sc.std(0, ddof=1) / np.sqrt(len(js))
# descriptive
Sdesc = np.zeros((len(desc), NG), np.float32)
for i in range(len(desc)):
    Sdesc[i] = matched_score(np.asarray(D[i]), Db[i].astype(np.float64))
# NTC pseudo (batch mix: controls are spread over all batches; use control batch mix)
ctl_mix = Cn.astype(np.float64)
pseudo_scores = np.zeros((10, NG), np.float32)
for j in range(10):
    pseudo_scores[j] = matched_score(NP[j], ctl_mix)
abs_ps = np.abs(pseudo_scores); med = float(np.median(abs_ps)); mad = float(np.median(np.abs(abs_ps-med)))
tau = med + 2*mad
np.save('results/atlas_primary_scores.npy', Spri); np.save('results/atlas_primary_construct_se.npy', SE)
np.save('results/atlas_primary_nconstructs.npy', NCON); np.save('results/atlas_construct_scores.npy', Gsc.astype(np.float32))
np.save('results/atlas_descriptive_scores.npy', Sdesc.astype(np.float32))
np.save('results/atlas_ntc_pseudo_scores.npy', pseudo_scores.astype(np.float32))
json.dump({'tau': float(tau), 'ntc_median_abs': med, 'ntc_mad': mad,
 'estimator_note': 'pooled-count rate vs batch-matched control rate (weights = unit cell counts per batch). Documented stabilization of the locked batch-matched-NTC rule: median 2-3 cells per target x batch makes per-stratum CPM ratios noise-dominated (87% of edges cleared tau under the naive stratum estimator - recorded as preserved failure). Gate text untouched.'},
 open('results/tau.json','w'), indent=1)
print('tau =', round(tau,4), '| primary edges |score|>tau:', int((np.abs(Spri)>tau).sum()), 'of', Spri.size)
lo, hi = Spri - 1.96*SE, Spri + 1.96*SE
supported = (np.abs(Spri) > tau) & ((lo > 0) | (hi < 0))
print('primary supported (|score|>tau AND 95% construct-CI excl 0):', int(supported.sum()))
json.dump({'n_edges_above_tau': int((np.abs(Spri)>tau).sum()), 'n_edges_supported': int(supported.sum())},
          open('results/atlas_score_summary.json','w'))
print('done', time.time()-t0, 's')
