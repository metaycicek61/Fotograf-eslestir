import sys,json,numpy as np
from PIL import Image
src,cj,out,y0,y1=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
im=np.array(Image.open(src).convert('RGB')).astype(int);r,g,b=im[...,0],im[...,1],im[...,2]
loose=((r-g>30)&(r-b>20))|((g-r>25)&(b-r>10)&(g>=b-15))
_hr=np.where(loose.mean(1)>0.25)[0]
for _y in _hr: loose[max(0,_y-1):_y+2]=False
C=json.load(open(cj));xs=[c['x'] for c in C];pitch=float(np.median(np.diff(xs)))
N=[]
def mk(x):
    xi=int(round(x));col=loose[y0:y1,xi-1:xi+2].any(1);ys=np.where(col)[0]
    if not len(ys): return None
    hi,lo=int(ys.min()+y0),int(ys.max()+y0);m=(hi+lo)//2
    return dict(x=float(x),bt=m,bb=m,hi=hi,lo=lo,red=bool((r[y0:y1,xi][loose[y0:y1,xi]]>g[y0:y1,xi][loose[y0:y1,xi]]).mean()>.5) if loose[y0:y1,xi].any() else False,ek=True)
for a,bb in zip(C,C[1:]+[None]):
    N.append(a)
    if bb is None: break
    n=int(round((bb['x']-a['x'])/pitch))-1
    for t in range(1,n+1):
        c=mk(a['x']+(bb['x']-a['x'])*t/(n+1))
        if c: N.append(c)
json.dump(N,open(out,'w'));print(len(C),'->',len(N),'pitch',round(pitch,2))
print([ (k+1,int(c['x'])) for k,c in enumerate(N) if c.get('ek')])
