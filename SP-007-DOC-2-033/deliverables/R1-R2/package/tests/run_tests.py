#!/usr/bin/env python3
import hashlib, os, shutil, subprocess, sys, tempfile
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE); CLI=os.path.join(ROOT,'cli','doc2033_review.py'); GOLD=os.path.join(HERE,'golden')
def run(root,*args): return subprocess.run([sys.executable,CLI,'--root',root,*args],capture_output=True)
def main():
 fail=[]
 for name,args in [('summary',('summary',)),('schema',('schema',)),('lookup',('lookup','reference-discordant','PKM','STAT3')),('row',('row','perturbation-supported','1'))]:
  p=run(ROOT,*args); want=open(os.path.join(GOLD,name+'.txt'),'rb').read(); ok=p.returncode==0 and p.stdout==want
  print('[%s] golden %s'%('PASS' if ok else 'FAIL',name)); fail += [] if ok else [name]
 p=run(ROOT,'verify'); ok=p.returncode==0 and b'AUDIT RESULT: PASS' in p.stdout; print('[%s] verify'%('PASS' if ok else 'FAIL')); fail += [] if ok else ['verify']
 a=run(ROOT,'export','association-only','--format','tsv').stdout; b=run(ROOT,'export','association-only','--format','tsv').stdout
 ok=a==b and hashlib.sha256(a).hexdigest()=='a1be0d3c4ab6ca5f78cd1393025b024f6d5a28620e9b7784f3b3d066b7bad373'; print('[%s] deterministic full export'%('PASS' if ok else 'FAIL')); fail += [] if ok else ['export']
 tmp=tempfile.mkdtemp(prefix='doc2033-corrupt-')
 try:
  shutil.copytree(ROOT,os.path.join(tmp,'p')); q=os.path.join(tmp,'p','frozen','deliverables','results','review_queue_summary.json'); d=open(q,'rb').read(); open(q,'wb').write(d.replace(b'26525',b'26524',1)); p=run(os.path.join(tmp,'p'),'verify'); ok=p.returncode==1 and b'AUDIT RESULT: FAIL' in p.stdout
  print('[%s] corruption detected'%('PASS' if ok else 'FAIL')); fail += [] if ok else ['corruption']
 finally: shutil.rmtree(tmp)
 print('ALL TESTS PASS' if not fail else 'TESTS FAILED: '+', '.join(fail)); return bool(fail)
if __name__=='__main__': sys.exit(main())
