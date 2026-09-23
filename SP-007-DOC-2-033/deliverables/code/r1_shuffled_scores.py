import numpy as np, json
idx = json.load(open('results/accum/index.json'))
primary, batches = idx['primary'], idx['batches']; NB, NG = len(batches), 8563
SH = np.memmap('results/accum/SH_targetXbatch.f32', dtype='float32', mode='r', shape=(len(primary)*NB, NG))
SHn = np.load('results/accum/SHn.npy'); C = np.load('results/accum/C_controlXbatch.npy')
tau = json.load(open('results/tau.json'))['tau']
Crate = C / C.sum(1, keepdims=True)
frac = []
for i in range(len(primary)):
    bw = SHn[i*NB:(i+1)*NB].astype(np.float64)
    if bw.sum()==0: continue
    xs = SH[i*NB:(i+1)*NB].sum(0)
    r_unit = xs/xs.sum(); w = bw/bw.sum()
    r_ctl = (w[:,None]*Crate).sum(0)
    s = np.log2((r_unit*1e6+1.0)/(r_ctl*1e6+1.0))
    frac.append(float((np.abs(s)>tau).mean()))
Spri = np.load('results/atlas_primary_scores.npy')
res = {'shuffled_frac_edges_above_tau_median': float(np.median(frac)),
       'primary_frac_edges_above_tau': float((np.abs(Spri)>tau).mean()),
       'verdict': 'PASS' if np.median(frac) < 0.15 else 'REVIEW'}
json.dump(res, open('results/shuffled_label_control.json','w'), indent=1)
print(json.dumps(res, indent=1))
