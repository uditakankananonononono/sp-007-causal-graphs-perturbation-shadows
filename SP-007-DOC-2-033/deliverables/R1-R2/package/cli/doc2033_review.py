#!/usr/bin/env python3
"""Read-only query/export CLI for frozen DOC-2-033 R1/R2 outputs.
No scoring, ranking, threshold parameters, model calls, or writes.
"""
import argparse, csv, hashlib, json, os, sys
CLASSES={
 'perturbation-supported':'cards_perturbation_supported.tsv',
 'association-only':'cards_association_only.tsv',
 'reference-discordant':'cards_reference_discordant.tsv'}
def root_files(root): return os.path.join(root,'frozen','deliverables','results')
def load_rows(root, cls):
 p=os.path.join(root_files(root),CLASSES[cls])
 with open(p,newline='',encoding='utf-8') as f: return list(csv.DictReader(f,delimiter='\t'))
def stable(rows): return sorted(rows,key=lambda r: tuple(r.get(k,'') for k in ('target','gene','class'))+tuple(r.values()))
def manifest_check(root):
 p=os.path.join(root,'MANIFEST.sha256'); listed={}; bad=[]
 with open(p,encoding='utf-8') as f:
  for line in f:
   h,rel=line.rstrip('\n').split('  ',1); listed[rel]=h
 for rel,h in listed.items():
  q=os.path.join(root,rel)
  if not os.path.isfile(q): bad.append('missing '+rel); continue
  got=hashlib.sha256(open(q,'rb').read()).hexdigest()
  if got!=h: bad.append('hash '+rel)
 actual=[]
 for dp,_,fs in os.walk(root):
  for n in fs:
   rel=os.path.relpath(os.path.join(dp,n),root)
   if rel!='MANIFEST.sha256': actual.append(rel)
 extra=sorted(set(actual)-set(listed))
 if extra: bad.extend('unlisted '+x for x in extra)
 return bad

def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--root',default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 sp=ap.add_subparsers(dest='cmd',required=True)
 sp.add_parser('summary'); sp.add_parser('schema'); sp.add_parser('verify')
 p=sp.add_parser('lookup'); p.add_argument('card_class',choices=sorted(CLASSES)); p.add_argument('target'); p.add_argument('gene')
 p=sp.add_parser('row'); p.add_argument('card_class',choices=sorted(CLASSES)); p.add_argument('number',type=int,help='1-based row in stable target/gene/class order')
 p=sp.add_parser('export'); p.add_argument('card_class',choices=sorted(CLASSES)); p.add_argument('--format',choices=('tsv','json'),default='tsv')
 a=ap.parse_args(); root=os.path.abspath(a.root)
 if a.cmd=='verify':
  bad=manifest_check(root)
  checks=[]
  for cls,n in [('perturbation-supported',26525),('association-only',2011),('reference-discordant',2)]:
   got=len(load_rows(root,cls)); checks.append((cls,got==n,got,n))
  print('MANIFEST '+('PASS' if not bad else 'FAIL'))
  for cls,ok,got,want in checks: print('%s %s rows=%d expected=%d'%(cls,'PASS' if ok else 'FAIL',got,want))
  ok=not bad and all(x[1] for x in checks); print('AUDIT RESULT: '+('PASS' if ok else 'FAIL'))
  if bad:
   for x in bad: print('  '+x)
  return 0 if ok else 1
 if a.cmd=='summary':
  obj=json.load(open(os.path.join(root_files(root),'review_queue_summary.json')))
  tr=json.load(open(os.path.join(root_files(root),'r2_transport_evaluation.json')))
  out={'r1_review_queue':obj,'r2_transport':tr,'boundary':'K562 exploratory/bounded; RPE1 transport failed'}
  print(json.dumps(out,sort_keys=True,indent=2)); return 0
 if a.cmd=='schema':
  out={}
  for cls in sorted(CLASSES): out[cls]=list(load_rows(root,cls)[0].keys())
  print(json.dumps(out,sort_keys=True,indent=2)); return 0
 rows=stable(load_rows(root,a.card_class))
 if a.cmd=='lookup':
  hit=[r for r in rows if r.get('target')==a.target and r.get('gene')==a.gene]
  print(json.dumps(hit,sort_keys=True,indent=2)); return 0 if hit else 1
 if a.cmd=='row':
  if a.number<1 or a.number>len(rows): return 1
  print(json.dumps(rows[a.number-1],sort_keys=True,indent=2)); return 0
 if a.cmd=='export':
  if a.format=='json': print(json.dumps(rows,sort_keys=True,indent=2)); return 0
  w=csv.DictWriter(sys.stdout,fieldnames=rows[0].keys(),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rows); return 0
if __name__=='__main__': sys.exit(main())
