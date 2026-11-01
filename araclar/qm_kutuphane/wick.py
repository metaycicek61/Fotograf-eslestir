import sys,json,numpy as np
from PIL import Image
src,cj,out,y0,y1=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5])
im=np.array(Image.open(src).convert('RGB')).astype(int);r,g,b=im[...,0],im[...,1],im[...,2]
col=((r-g>25)&(r-b>25))|((g-r>25)&(b-r>10)&(g>=b-15))
_hr=np.where(col.mean(1)>0.25)[0]
for _y in _hr: col[max(0,_y-1):_y+2]=False
C=json.load(open(cj))
for c in C:
    x=int(round(c['x']));ok=lambda y:col[y,x-1:x+2].any()
    y=c['bt']
    while y>y0 and (ok(y-1) or ok(y-2)): y-=1
    hi=y;y=c['bb']
    while y<y1 and (ok(y+1) or ok(y+2)): y+=1
    c['hi'],c['lo']=min(hi,c.get('hi',hi)) if c.get('ek') else hi,max(y,c.get('lo',y)) if c.get('ek') else y
json.dump(C,open(out,'w'))
for k,c in enumerate(C,1):
    if int(sys.argv[6])<=k<=int(sys.argv[7]): print(k,int(c['x']),c['hi'],c['bt'],c['bb'],c['lo'],'R' if c['red'] else 'G')
