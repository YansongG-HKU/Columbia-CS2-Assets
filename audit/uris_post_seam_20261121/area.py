"""GEOS proof of the complete tall/short coverage using actual encoded FBX rows."""
import numpy as np,sys,json,math
from pathlib import Path
from osgeo import ogr
D=Path(__file__).resolve().parent
raw=json.loads((D/'raw.json').read_text())
eps=1e-5; fields=('uv','normal','tangent','binormal')
def poly(x):
 r=ogr.Geometry(ogr.wkbLinearRing)
 for a,b in x:r.AddPoint_2D(float(a),float(b))
 r.CloseRings();p=ogr.Geometry(ogr.wkbPolygon);p.AddGeometry(r);assert p.IsValid() and p.GetArea()>0
 return p
def ar(g):return g.GetArea() if g.GetDimension()==2 else 0.
def union(items):
 m=ogr.Geometry(ogr.wkbMultiPolygon)
 for p in items:m.AddGeometry(p)
 return m.UnionCascaded()
def project(r,k,rounding=None):
 a=np.delete(r['x'],k,axis=1)
 return poly(a if rounding is None else np.round(a,rounding))
def direction(r):
 a,b,c=np.asarray(r['x']);q=np.cross(b-a,c-a);k=int(np.argmax(abs(q)));return k,int(np.sign(q[k]))
def aff(projected,value):
 # Local plane coordinates plus 1; direct solving preserves all values, including tangent vectors.
 q=np.asarray(projected);return np.linalg.solve(np.column_stack((q,np.ones(len(q)))),np.asarray(value))
fix={}
for lod,r in raw.items():
 ll=r['local']['long'];sh=r['local']['short'];
 res={}
 for k in (0,2):
  for s in (-1,1):
   A=[(z,x) for z,x in ll.items() if direction(x)==(k,s)]
   B=[(z,x) for z,x in sh.items() if direction(x)==(k,s)]
   assert len(A)==len(B)==2
   assert max(q[k] for _,x in A+B for q in x['x'])-min(q[k] for _,x in A+B for q in x['x'])<eps
   a,b=[union([project(z,k) for _,z in qq]) for qq in (A,B)]
   dist=ar(b.Difference(a))
   coverage=ar(a.Intersection(b)); expected=b.GetArea()
   aa,bb=[union([project(z,k,5) for _,z in qq]) for qq in (A,B)]
   assert ar(bb.Difference(aa))==0 and dist<.00001,(lod,k,s,ar(bb.Difference(aa)),dist)
   # Compare per-corner affine fields across EVERY pair of old triangles whose intersection has area.
   maxerr={u:0. for u in fields};n=0
   for (_,x),(_,y) in [(x,y) for x in A for y in B]:
    p=project(x,k).Intersection(project(y,k))
    if ar(p)<=1e-10:continue
    n+=1
    assert p.GetGeometryName()=='POLYGON'
    pp=np.asarray([[a,b,1.] for a,b,*_ in p.GetGeometryRef(0).GetPoints()])
    for u in fields:
     dx=aff(np.delete(x['x'],k,axis=1),x[u]);dy=aff(np.delete(y['x'],k,axis=1),y[u])
     maxerr[u]=max(maxerr[u],float(np.linalg.norm(pp@(dx-dy),axis=1).max()))
   res[f'{k},{s}']=dict(both_projected_coverage_m2=[coverage,ar(b.Intersection(a))],candidate_short_area=expected,
    uncovered_raw_m2=dist,uncovered_at_10um_snap_m2=0.,compared_triangle_pairs=n,field_max_discrepancy=maxerr)
   for u,d in maxerr.items():assert d<3e-5,(lod,k,s,u,d)
 # Two old short cap triangles were inside the taller shell; all four corners fit its rectangular section.
 cap=[x for x in sh.values() if direction(x)==(1,1)]
 assert len(cap)==2
 shoes=[x for x in ll.values() if direction(x)==(1,1) or direction(x)==(1,-1)]
 assert len(shoes)==4
 upper=union([project(x,1,5) for x in shoes if direction(x)==(1,1)])
 lc=union([project(x,1,5) for x in cap])
 assert ar(lc.SymDifference(upper))==0.
 assert all(.60001<p[1]<10.79999 for x in cap for p in x['x'])
 fix[lod]=dict(laterals=res,capped_interior_m2=lc.GetArea(),lateral_uncovered_raw_sum_m2=sum(x['uncovered_raw_m2'] for x in res.values()))
(D/'area.json').write_text(json.dumps(fix,indent=2)+'\n')
print(json.dumps(fix,indent=2))
