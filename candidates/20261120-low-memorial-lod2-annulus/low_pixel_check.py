"""Cross-check the unlit changed pixels against the projected repaired ring."""
from low_tri_plan import *
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
d=Path(__file__).resolve().parent
C=np.array([0.,9.,34.]); extent=42.; span=1.10*extent
projection=lambda w,h,right,up,j:(w/2+w/span*np.dot(right,[(V[j][0]-C[0]),(-V[j][2]-C[1]),(V[j][1]-C[2])]),
                                     h/2-w/span*np.dot(up,[(V[j][0]-C[0]),(-V[j][2]-C[1]),(V[j][1]-C[2])]))
report={}
for k,pos in {'front':(1.6,-2.1,.7),'rear':(-1.4,1.9,.66),'aerial':(.25,-.84,2.5)}.items():
 f=-np.asarray(pos);f=f/np.linalg.norm(f)
 right=np.cross(f,[0,0,1]);right=right/np.linalg.norm(right);up=np.cross(right,f)
 for mode in ('base','lit'):
  b,a=[np.asarray(Image.open(d/'low-candidate-renders'/f'{s}-{mode}-{k}.png').convert('RGBA')).astype(np.int16) for s in ('before','after')]
  h,w=b.shape[:2]
  m=Image.new('L',(w,h))
  pen=ImageDraw.Draw(m);pen.polygon([projection(w,h,right,up,i) for i in oa],fill=255)
  pen.polygon([projection(w,h,right,up,i) for i in ia],fill=0)
  mask=np.asarray(m.filter(ImageFilter.MaxFilter(9)))>0
  diff=np.max(abs(a-b),axis=2)
  q=diff[~mask]
  change_out=int(np.sum(q>2));change_in=int(np.sum(diff[mask]>2))
  if mode=='base':assert change_out==0 and change_in>50,(k,change_out,change_in)
  report[k+'-'+mode]=dict(projected_annulus_change_gt2=change_in,outside_change_gt2=change_out,
   outside_max=int(q.max()),outside_p99=float(np.quantile(q,.99)),
   foreground_silhouette_different_px=int(np.sum((b[:,:,3]>=128)!=(a[:,:,3]>=128))))
(d/'low-pixels.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
