"""Find a LOD2 atlas tile clear of all existing retained UV faces."""
from low_tri_plan import *
from PIL import Image,ImageDraw
import numpy as np
uv=item(g,b'LayerElementUV')
u=prop(uv,b'UV'); ui=prop(uv,b'UVIndex')
uu=[tuple(u[k:k+2]) for k in range(0,len(u),2)]
base=next((d/'low-textures').glob('*LOD2_BaseColor.png'))
size=Image.open(base).size
print('Texture formats:',[(p.name,Image.open(p).size,Image.open(p).mode) for p in sorted((d/'low-textures').glob('*.png'))])
W,H=size
assert min(u)>=0 and max(u)<=1
occ=Image.new('L',size)
p=ImageDraw.Draw(occ)
for i,f in enumerate(F):
 if i in disks:continue
 p.polygon([(int(W*uu[j][0]),int(H*(1-uu[j][1]))) for j in ui[i*3:i*3+3]],fill=1)
a=np.asarray(occ); q=np.pad(a,((1,0),(1,0))).cumsum(0,dtype=np.int64).cumsum(1,dtype=np.int64)
empty=[]
for w,h in [(144,152),(116,126),(96,104),(80,88)]:
 s=q[h:,w:]-q[h:,:-w]-q[:-h,w:]+q[:-h,:-w]
 ys,xs=np.where(s==0)
 R=[(int(i),int(j)) for i,j in zip(xs,ys) if 32<=i and i+w<=W-32 and 32<=j and j+h<=H-32 and i%4==j%4==0]
 print(w,h,len(R),R[:8])
 if R:
  x,y=max(R,key=lambda t:min(t[0],t[1],W-w-t[0],H-h-t[1]))
  empty.append(dict(x=x,y=y,w=w,h=h))
alt=Image.fromarray(a*255)
alt.save(d/'low-far-existing-UV.png')
(d/'low-atlas-probe.json').write_text(json.dumps(empty,indent=2)+'\n')
