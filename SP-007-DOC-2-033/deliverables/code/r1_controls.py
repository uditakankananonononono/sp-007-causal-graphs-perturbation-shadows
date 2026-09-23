import numpy as np, json, time
t0=time.time()
idx = json.load(open('results/accum/index.json'))
primary, batches = idx['primary'], idx['batches']; NB, NG = len(batches), 8563
P = np.memmap('results/accum/P_targetXbatch.f32', dtype='float32', mode='r', shape=(len(primary)*NB, NG))
S = np.memmap('results/accum/S_targetXstate.f32', dtype='float32', mode='r', shape=(len(primary)*3, NG))
Pn = np.load('results/accum/Pn.npy'); C = np.load('results/accum/C_controlXbatch.npy'); Cn = np.load('results/accum/Cn.npy')
Spri = np.load('results/atlas_primary_scores.npy'); SE = np.load('results/atlas_primary_construct_se.npy')
tau = json.load(open('results/tau.json'))['tau']
genes = [l.strip() for l in open('results/gene_names.txt')]
gidx = {g:i for i,g in enumerate(genes)}
Crate = C / C.sum(1, keepdims=True)
def matched_score(Xsum, bw):
    N = bw.sum()
    r_unit = Xsum / Xsum.sum()
    w = bw / N
    r_ctl = (w[:,None]*Crate).sum(0)
    return np.log2((r_unit*1e6+1.0)/(r_ctl*1e6+1.0))
res = {}
# 1. self-edge positive control: score(t, gene=t) should be negative
self_scores, self_null = [], []
rng = np.random.default_rng(20260922+3)
ctl_mean_cpm = (Crate.mean(0)*1e6)
for i, t in enumerate(primary):
    if t in gidx:
        s = Spri[i, gidx[t]]; self_scores.append(float(s))
        # expression-matched null genes: 10 genes nearest control-mean expression to gene t
        d = np.abs(ctl_mean_cpm - ctl_mean_cpm[gidx[t]])
        nulls = np.argsort(d)[1:11]
        self_null.append(Spri[i, nulls].tolist())
self_scores = np.array(self_scores); self_null = np.array(self_null)
res['self_edge_control'] = {
 'n_targets_with_self_gene': int(len(self_scores)),
 'median_self_score': float(np.median(self_scores)),
 'frac_self_negative': float((self_scores<0).mean()),
 'frac_self_below_-tau': float((self_scores < -tau).mean()),
 'null_median': float(np.median(self_null)), 'null_frac_below_-tau': float((self_null < -tau).mean()),
 'verdict': 'PASS' if (np.median(self_scores) < -tau and (self_scores<-tau).mean() > 0.8) else 'REVIEW'}
# 2. permuted strata: shuffle control batch rows -> recompute scores for primary targets
perm = rng.permutation(NB)
Crate_perm = Crate[perm]
def matched_score_perm(Xsum, bw):
    N = bw.sum(); r_unit = Xsum/Xsum.sum(); w = bw/N
    r_ctl = (w[:,None]*Crate_perm).sum(0)
    return np.log2((r_unit*1e6+1.0)/(r_ctl*1e6+1.0))
diffs = []
for i in range(len(primary)):
    s0 = Spri[i]; s1 = matched_score_perm(P[i*NB:(i+1)*NB].sum(0), Pn[i*NB:(i+1)*NB].astype(np.float64))
    diffs.append(float(np.corrcoef(s0, s1)[0,1]))
res['permuted_strata'] = {'median_score_correlation': float(np.median(diffs)),
 'verdict': 'PASS' if np.median(diffs) > 0.95 else 'REVIEW'}
# 3. leave-one-batch-out stability (targets with >=2 nonempty batches)
lobo = []
for i in range(len(primary)):
    nb = Pn[i*NB:(i+1)*NB].astype(np.float64); nz = np.where(nb>0)[0]
    if len(nz) < 3: continue
    s0 = Spri[i]; cors = []
    for b in nz[:6]:
        nb2 = nb.copy(); nb2[b]=0
        if nb2.sum()==0: continue
        s1 = matched_score(P[i*NB:(i+1)*NB].sum(0), nb2)
        cors.append(float(np.corrcoef(s0,s1)[0,1]))
    if cors: lobo.append(float(np.median(cors)))
res['leave_one_batch_out'] = {'n_targets_tested': len(lobo), 'median_correlation': float(np.median(lobo)),
 'verdict': 'PASS' if np.median(lobo) > 0.95 else 'REVIEW'}
# 4. cell-state sensitivity: per-state scores vs pooled
cors = []
for i in range(len(primary)):
    s0 = Spri[i]
    for st in range(3):
        xs = S[(i*3+st)]
        if xs.sum()==0: continue
        s1 = np.log2((xs/xs.sum()*1e6+1.0)/((Crate.mean(0))*1e6+1.0))
        cors.append(float(np.corrcoef(s0, s1)[0,1]))
res['cell_state_sensitivity'] = {'n_target_state_pairs': len(cors), 'median_correlation': float(np.median(cors)),
 'verdict': 'PASS' if np.median(cors) > 0.9 else 'REVIEW'}
# 5. leakage assertions
folds = json.load(open('/tmp/sp7_folds.json'))
fold_groups = {}
for t, f in folds.items(): fold_groups.setdefault(f, []).append(t)
overlap = sum(len(set(fold_groups[a]) & set(fold_groups[b])) for a in fold_groups for b in fold_groups if a<b)
pseudo = json.load(open('/tmp/sp7_ntc_pseudo.json'))
import pandas as pd
df = pd.read_pickle('/tmp/sp7_obs_frozen.pkl')
ctl_ok = all(df['perturbation'].iloc[r]=='control' for k,v in pseudo.items() for r in v[:50])
res['leakage_assertions'] = {'fold_target_overlap': overlap, 'pseudo_rows_are_controls_sampled': bool(ctl_ok),
 'verdict': 'PASS' if overlap==0 and ctl_ok else 'FAIL'}
# 6. MOI
res['moi_sensitivity'] = {'note': 'vacuous on this harmonized file: all targeting cells nperts==1 (verified in QC audit); multi-perturbation exclusion documented in freeze manifest', 'verdict': 'DOCUMENTED'}
json.dump(res, open('results/controls_battery.json','w'), indent=1)
print(json.dumps(res, indent=1))
print('controls done', time.time()-t0, 's')
