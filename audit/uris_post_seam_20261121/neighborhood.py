"""Measure full reimported patch neighborhood with both GEOS and independent convex clipping."""
from itertools import combinations
from pathlib import Path
from osgeo import ogr
import numpy as np,json,sys,collections,math
D=Path(__file__).resolve().parent
E=1e-5; M=1e-6
def signed(a,b,c):
 return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def clipping(a,b):
 def area(p):return abs(sum(signed(p[0],u,v) for u,v in zip(p[1:],p[2:])))/2 if p else 0.
 p=list(a);q=list(b)
 if signed(*q)<0:q.reverse()
 for c,d in zip(q,q[1:]+q[:1]):
  out=[]
  for u,v in zip(p[-1:]+p[:-1],p):
   t,w=signed(c,d,u),signed(c,d,v)
   if (t>=0)!=(w>=0):
    j=t/(t-w);out.append(tuple(a+j*(b-a) for a,b in zip(u,v)))
   if w>=0:out.append(v)
  p=out
 return area(p)
def poly(q):
 r=ogr.Geometry(ogr.wkbLinearRing)
 for a,b in q:r.AddPoint_2D(float(a),float(b))
 r.CloseRings();p=ogr.Geometry(ogr.wkbPolygon);p.AddGeometry(r);return p
def calc(P,Q):
 n=[]
 for V in P,Q:
  a,b,c=V;x=np.cross(b-a,c-a);s=np.linalg.norm(x)
  if s<=0:return
  n.append(x/s)
 dn=n[0]@n[1]
 if abs(dn)<1-1e-6:return
 if max(np.abs((Q-P[0])@n[0]).max(),np.abs((P-Q[0])@n[1]).max())>E:return
 ds=[]
 for ix,R in enumerate([P,Q]):
  k=int(np.argmax(np.abs(n[ix]))); A,B=[np.delete(V-R[0],k,axis=1) for V in [P,Q]]
  two=clipping(A,B)/abs(n[ix][k]);C=poly(A).Intersection(poly(B));geos=C.GetArea()/abs(n[ix][k]) if C.GetDimension()==2 else 0.
  assert abs(two-geos)<1e-8,(two,geos)
  ds.append(geos)
 if min(ds)<=M:return
 return dict(mode='same' if dn>0 else 'opposed',area_2ways_m2=ds,normal_dot=float(dn))
def screen(r):
 a={int(k):np.asarray(x) for k,x in r.items()};h={}
 for i,j in combinations(a,2):
  p,q=a[i],a[j]
  if not np.all((p.min(0)-E<=q.max(0)) & (q.min(0)-E<=p.max(0))):continue
  s=calc(p,q)
  if s:h[min(i,j),max(i,j)]=s
 return h
d=json.loads((D/'verified.json').read_text());out={}
for lod,r in d.items():
 before,after=(screen(r[k]) for k in ('local_before','local_after'))
 vanished=before.keys()-after.keys()
 assert all(after[q]==s for q,s in before.items() if q not in vanished) and not after.keys()-before.keys()
 L={int(i) for i in r['removed']};assert all(set(q)&L for q in vanished)
 ties=[(min(t['before_face'],t['after_face_old_id']),max(t['before_face'],t['after_face_old_id'])) for t in r['first_hit_tests']['full_building']['coincident_first_hit_choices']]
 # Tied hits are demonstrably on a pre-existing same/opposed overlap that remains unchanged.
 assert all(q in before and q in after and before[q]==after[q] for q in ties)
 c=lambda x:dict(collections.Counter(p['mode'] for p in x.values()))
 orig,cand=c(before),c(after)
 out[lod]=dict(source_counts=orig,repair_counts=cand,vanished=[dict(faces=q,**before[q]) for q in sorted(vanished)],existing_tied_choice_count=len(ties),existing_tied_pairs=sorted(set(ties)))
 print(lod,orig,cand,collections.Counter(before[q]['mode'] for q in vanished),sorted(set(ties)))
(D/'neighborhood.json').write_text(json.dumps(out,indent=2)+'\n')
