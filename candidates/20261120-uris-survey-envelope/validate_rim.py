"""Verify exported roof triangles at held points; separate sampled surfaces."""
import collections, json,gzip,hashlib,sys
from pathlib import Path
import numpy as np
w=Path(sys.argv[1]); csv=Path(sys.argv[2]); evidence=json.loads((w/'rim-study.json').read_text());p=w/'Uris-north-roof-rim-study.obj'
assert hashlib.sha256(p.read_bytes()).hexdigest()==evidence['obj_sha256']
with gzip.open(csv,'rt') as g:a=np.unique(np.loadtxt(g,delimiter=',',skiprows=1,usecols=range(6)),axis=0)
rings=json.loads((w/'facet-source-tags.json').read_text())['bands_by_face_in_export_order']
a=a[np.isin(a[:,4],evidence['held_out_ids']) & (a[:,3]==1)&(a[:,5]==1)]
xy=a[:,:2]-evidence['origin_epsg6347_m']; zr=a[:,2]
arc=a[:,:2]-evidence['centre_epsg6347_m']; deg=np.rad2deg(np.arctan2(arc[:,1],arc[:,0])); radial=np.linalg.norm(arc,axis=1)
m=(deg>30.1)&(deg<145.9)
higher=m&(radial>19.5)&(radial<23.)&(zr>=55.77)&(zr<=56.18)
low=m&(radial>15.)&(radial<24.)&(zr>=54.85)&(zr<=55.25)
V=[]; F=[]
for line in p.read_text().splitlines():
 x=line.split()
 if x[0]=='v':V.append([float(f) for f in x[1:]])
 if x[0]=='f':F.append([int(i)-1 for i in x[1:]])
V=np.array(V)
def height(which, candidate):
 q=xy[candidate];r=np.full(len(q),np.nan)
 for f,t in zip(F,rings):
  if t not in which:continue
  vv=V[f]; A=np.column_stack([vv[1,:2]-vv[0,:2],vv[2,:2]-vv[0,:2]])
  assert np.linalg.det(A)>1.e-4
  uv=(q-vv[0,:2])@np.linalg.inv(A).T
  b=np.c_[1-uv.sum(1),uv]; d=b.min(1)>=-1.e-8;h=b[d]@vv[:,2]+evidence['z0_navd88_m']
  old=r[d]
  assert np.all(np.isnan(old)|(abs(old-h)<1.e-7))
  r[d]=h
 return r

def evaluate(c,types):
 y=height(types,c); n=np.isfinite(y)
 m=np.abs(y[n]-zr[c][n])
 return {'window_n':int(c.sum()),'triangle_hit_n':int(n.sum()),'fraction_hit':float(n.mean()),'abs_height_p50_p90_p95_m':np.quantile(m,[.50,.90,.95]).round(4).tolist()}
s={'band_returns':evaluate(higher,{2}),'lower_returns':evaluate(low,{0,4})}
assert s['band_returns']['fraction_hit']>.85
assert s['lower_returns']['fraction_hit']>.90
assert s['band_returns']['abs_height_p50_p90_p95_m'][1]<.13
assert s['lower_returns']['abs_height_p50_p90_p95_m'][1]<.13
(w/'triangle-holdout.json').write_text(json.dumps(s,indent=2)+'\n');print(s)

