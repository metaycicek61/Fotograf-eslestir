import sys,json,numpy as np
from PIL import Image,ImageDraw
cj,first,last,name,chans=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],json.loads(sys.argv[5])
RED=(224,43,59);GREEN=(8,156,88);W,H=502,277;MX,MY=30,22
C=json.load(open(cj))[first-1:last];n=len(C)
pitch=(W-2*MX)/n;bw=max(2,min(15,round(pitch*.76)))
lo_y=min(c['hi'] for c in C);hi_y=max(c['lo'] for c in C)
sy=(H-2*MY)/(hi_y-lo_y)
Y=lambda v:MY+(v-lo_y)*sy
Xc=lambda i:MX+pitch*(i+.5)
D=[]
for i,c in enumerate(C):
    x=Xc(i);col=RED if c['red'] else GREEN
    bt,bb=Y(c['bt']),Y(c['bb'])
    if bb-bt<1:bb=bt+1
    D.append((x,Y(c['hi']),bt,bb,Y(c['lo']),col))
def draw(img,ox=0,oy=0):
    d=ImageDraw.Draw(img)
    for x,h,t,b,l,col in D:
        d.line([(x+ox,h+oy),(x+ox,l+oy)],fill=col,width=1)
        d.rectangle([x-bw/2+ox,t+oy,x+bw/2+ox-1,b+oy],fill=col)
img=Image.new('RGB',(W,H),'white');draw(img);img.save(name+'_temiz.png')
# kanallar (temiz koordinatlarda), govde esasli + %20
segs=[];meta=[]
for i,j,col in chans:
    idx=list(range(i-first,j-first+1))
    x=np.array([D[k][0] for k in idx]);bt=np.array([D[k][2] for k in idx]);bb=np.array([D[k][3] for k in idx])
    k_,c_=np.polyfit(x,(bt+bb)/2,1);base=k_*x+c_;up=(bt-base).min();dn=(bb-base).max();w=dn-up
    tu,td=up-.2*w,dn+.2*w;X0,X1=x[0]-pitch/2,x[-1]+pitch/2
    segs+=[((X0,k_*X0+c_+tu),(X1,k_*X1+c_+tu),tuple(col)),((X0,k_*X0+c_+td),(X1,k_*X1+c_+td),tuple(col))]
    meta.append(dict(mumlar=[i-first+1,j-first+1],egim=round(float(k_),4),kesisim=round(float(c_),2),ust=round(float(tu),2),alt=round(float(td),2),tur='yukselis' if k_<-0.05 else ('dusus' if k_>0.05 else 'yatay')))
ys=[p[1] for s in segs for p in s[:2]];top=int(min(0,min(ys)-6));bot=int(max(H,max(ys)+6))
S=3;big=Image.new('RGB',(W,bot-top),'white');draw(big,0,-top)
big=big.resize((W*S,(bot-top)*S),Image.LANCZOS);d=ImageDraw.Draw(big)
def dash(p,q,col,w,on=14,off=8):
    x0,y0=p;x1,y1=q;L=((x1-x0)**2+(y1-y0)**2)**.5;m=int(L//(on+off))+1
    for t in range(m):
        a=t*(on+off)/L;b=min(1,(t*(on+off)+on)/L)
        d.line([(x0+(x1-x0)*a,y0+(y1-y0)*a),(x0+(x1-x0)*b,y0+(y1-y0)*b)],fill=col,width=w)
for p,q,col in segs: dash((p[0]*S,(p[1]-top)*S),(q[0]*S,(q[1]-top)*S),col,S+1)
big.save(name+'_temiz_kanal20.png')
json.dump(dict(mum_sayisi=n,boyut=[W,H],kanal_payi=0.2,kanallar=meta),open(name+'_kanallar.json','w'),ensure_ascii=False,indent=1)
print(n,bw,round(pitch,2));print(json.dumps(meta,ensure_ascii=False))
