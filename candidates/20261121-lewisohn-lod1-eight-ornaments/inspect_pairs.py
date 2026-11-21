"""Diagnose raw FBX reversed polygons and their actual edge, UV, and source relations."""
import collections,sys,pathlib,types,json
from pathlib import Path
from math import sqrt
mod=types.ModuleType('io_scene_fbx');mod.__path__=['/usr/share/blender/scripts/addons_core/io_scene_fbx'];sys.modules[mod.__name__]=mod
from io_scene_fbx import parse_fbx
import numpy as np
p=Path(sys.argv[1]); out=Path(sys.argv[2])
root,ver=parse_fbx.parse(str(p))
g,=[a for o in root.elems if o.id==b'Objects' for a in o.elems if a.id==b'Geometry']; print('geo',g.props)
one=lambda a,k:next(o for o in a.elems if o.id==k)
prop=lambda a,k:one(a,k).props[0]
V=np.array(prop(g,b'Vertices')).reshape(-1,3)
f=np.array(prop(g,b'PolygonVertexIndex')).reshape(-1,3);F=np.where(f<0,-1-f,f)
U=one(g,b'LayerElementUV');T=np.asarray(prop(U,b'UV')).reshape(-1,2); TV=np.asarray(prop(U,b'UVIndex')).reshape(-1,3)
groups=collections.defaultdict(list); edges=collections.defaultdict(list); vkeep=collections.Counter()
for i,a in enumerate(F):
 groups[tuple(sorted(a))].append(i)
 for k in a:vkeep[k]+=1
 for x,y in zip(a,np.roll(a,-1)):edges[min(x,y),max(x,y)].append((i,int(x),int(y)))
for p0 in g.elems:
 print(p0.id,[(x.id,[(type(y).__name__,len(y) if hasattr(y,'__len__') else y) for y in x.props]) for x in p0.elems][:20],[(type(v).__name__,len(v) if hasattr(v,'__len__') else v) for v in p0.props])
R=[]
for key,n in groups.items():
 if len(n)<2:continue
 assert len(n)==2
 tri0,tri1=F[n]
 pts=V[tri0]
 d=np.cross(pts[1]-pts[0],pts[2]-pts[0]); area=np.linalg.norm(d)*.5
 xyz=lambda m: m[:,[0,2,1]]*np.array([1,-1,1]) # raw metre coordinates, verifying Blender world separately
 w=xyz(pts); nrm=xyz(d[None,:])[0]/(2.*area)
 a0={int(v):p.tolist() for v,p in zip(tri0,T[TV[n[0]]])}
 a1={int(v):p.tolist() for v,p in zip(tri1,T[TV[n[1]]])}
 eq=max(np.linalg.norm(np.array(a0[i])-a1[i]) for i in a0)
 one0={'indices':[int(i) for i in key],'pair':[int(i) for i in n],
  'world_xyz':w.tolist(),'world_normal_first':nrm.tolist(),'area_m2':area,'corner_uv_first':a0,'corner_uv_second':a1,'max_same_vertex_uv_delta':eq,
  'vertex_num_faces':[int(vkeep[x]) for x in key],'neighbor_faces':{f'{int(x)}:{int(y)}':edges[min(x,y),max(x,y)] for x,y in zip(tri0,np.roll(tri0,-1))}}
 R.append(one0)
 print(n,'point center',w.mean(axis=0).round(4),'size',np.ptp(w,axis=0).round(4),'worldN',nrm.round(4),'area',area,'maxUV',eq,'face sets', [len(v) for v in one0['neighbor_faces'].values()])
out.write_text(json.dumps(R,indent=2)+'\n')
