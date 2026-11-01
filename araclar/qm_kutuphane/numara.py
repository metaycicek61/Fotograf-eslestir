import sys,json
from PIL import Image,ImageDraw,ImageFont
import numpy as np
src,out,cfg=sys.argv[1],sys.argv[2],json.loads(sys.argv[3])
img=Image.open(src).convert('RGB');im=np.array(img).astype(int)
H,W,_=im.shape
r,g,b=im[...,0],im[...,1],im[...,2]
body=((r>200)&(g<120)&(b<120))|((g>130)&(r<90)&(b>110)&(b<190))
wick=((r-g>50)&(r-b>50)&(r>180))|((g-r>50)&(b-r>30)&(g>120))
y0,y1,x0,x1=cfg['area']
for m in (body,wick):
    m[:y0]=False;m[y1:]=False;m[:,:x0]=False;m[:,x1:]=False
cols=body.sum(0);xs=[x for x in range(W) if cols[x]>0]
groups=[];cur=[xs[0]]
for x in xs[1:]:
    if x-cur[-1]<=1:cur.append(x)
    else:groups.append(cur);cur=[x]
groups.append(cur)
C=[]
for gp in groups:
    a,z=gp[0],gp[-1]
    ys=np.where(body[:,a:z+1].any(1))[0]
    cx=(a+z)/2
    wz=wick[:,max(0,int(cx)-1):int(cx)+2]
    wy=np.where(wz.any(1))[0]
    hi=min(ys.min(),wy.min() if len(wy) else 9999);lo=max(ys.max(),wy.max() if len(wy) else 0)
    C.append(dict(x=float(cx),bt=int(ys.min()),bb=int(ys.max()),hi=int(hi),lo=int(lo),red=bool((r[:,a:z+1][body[:,a:z+1]]>200).mean()>.5)))
json.dump(C,open(out+'.json','w'))
S=cfg.get('scale',3)
big=img.resize((W*S,H*S),Image.LANCZOS).convert('RGBA')
ov=Image.new('RGBA',big.size,(0,0,0,0));d=ImageDraw.Draw(ov)
if 'yellow_right' in cfg:
    k=cfg['yellow_right'];xa=(C[k-1]['x']+C[k]['x'])/2*S
    d.rectangle([xa,0,W*S,H*S],fill=(255,215,0,80))
if 'yellow' in cfg:
    i,j=cfg['yellow'];xa=(C[i-1]['x']-3)*S;xb=(C[j-1]['x']+3)*S
    d.rectangle([xa,0,xb,H*S],fill=(255,215,0,70))
big=Image.alpha_composite(big,ov);d=ImageDraw.Draw(big)
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',int(4.2*S))
for k,c in enumerate(C,1):
    y=(c['lo']+4+(k%3)*6)*S
    d.text((c['x']*S,y),str(k),fill=(20,20,160),font=f,anchor='mt',stroke_width=2,stroke_fill='white')
for seg in cfg.get('channels',[]):
    i,j,col=seg[0],seg[1],tuple(seg[2])
    P=C[i-1:j];x=np.array([p['x'] for p in P]);m=np.array([(p['bt']+p['bb'])/2 for p in P])
    k_,c_=np.polyfit(x,m,1);base=k_*x+c_
    q=cfg.get('q',0.1);up=np.quantile(np.array([p['bt'] for p in P])-base,q);dn=np.quantile(np.array([p['bb'] for p in P])-base,1-q)
    for off in (up,dn):
        d.line([(x[0]*S,(k_*x[0]+c_+off)*S),(x[-1]*S,(k_*x[-1]+c_+off)*S)],fill=col,width=S+1)
for lab in cfg.get('labels',[]):
    k,t=lab[0],lab[1];c=C[k-1];below=len(lab)>2
    if below: d.text((c['x']*S,(c['lo']+24)*S),t,fill=(200,0,0),font=f,anchor='mt',stroke_width=2,stroke_fill='white')
    else: d.text((c['x']*S,(c['hi']-4)*S),t,fill=(200,0,0),font=f,anchor='mb',stroke_width=2,stroke_fill='white')
for k in cfg.get('cutafter',[]):
    xc=(C[k-1]['x']+C[k]['x'])/2*S
    d.line([(xc,0),(xc,H*S)],fill=(230,0,0),width=S)
big.convert('RGB').save(out)
print(len(C))
