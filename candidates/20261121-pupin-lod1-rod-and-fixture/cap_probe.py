"""Trace each isolated reversed duplicate to the same intact independently reconstructed parts in two assets."""
import bpy,sys,collections,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from io_scene_fbx import parse_fbx
d=Path(sys.argv[sys.argv.index('--')+1]).resolve()
P=d/'input/import-assets/PupinHall'; near=P/'NA_PupinHall_8x3.fbx'; old=P/'NA_PupinHall_8x3_LOD1.fbx'; control=d/'main/fbx/split/NA_PupinHall_8x3_LOD1.fbx'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def mesh(p):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 o,=[o for o in bpy.context.scene.objects if o.type=='MESH'];m=o.data
 v=[o.matrix_world@x.co for x in m.vertices];f=[tuple(f.vertices) for f in m.polygons]
 edges=collections.defaultdict(set)
 for a in f:
  for i in a:edges[i].update(a)
 left=set(edges); comps={}; ids={}
 while left:
  k=left.pop();s={k};q=[k]
  while q:
   i=q.pop();n=edges[i]&left;s.update(n);left-=n;q.extend(n)
  ix=min(s);comps[ix]=sorted(s)
  for i in s:ids[i]=ix
 cp=collections.defaultdict(list)
 for i,f0 in enumerate(f):cp[ids[f0[0]]].append(i)
 return v,f,comps,cp,o.matrix_world.copy()
nV,nF,nC,nPF,nM=mesh(near);oV,oF,oC,oPF,oM=mesh(old);cV,cF,cC,cPF,cM=mesh(control)
assert max(abs(nM[i][j]-oM[i][j]) for i in range(4) for j in range(4))<.00001
raw,_=parse_fbx.parse(str(near));gg,=[g for q in raw.elems if q.id==b'Objects' for g in q.elems if g.id==b'Geometry']
one=lambda a,k:next(x for x in a.elems if x.id==k)
def val(a,k):return one(a,k).props[0]
rV=val(gg,b'Vertices'); nv=[tuple(rV[i:i+3]) for i in range(0,len(rV),3)]; assert len(nv)==len(nV)
fl=val(gg,b'PolygonVertexIndex'); nf=[tuple(i if i>=0 else -1-i for i in fl[m:m+3]) for m in range(0,len(fl),3)]
assert len(nf)==len(nF) and nf==nF
N=one(gg,b'LayerElementNormal'); U=one(gg,b'LayerElementUV')
n=val(N,b'Normals');ni=val(N,b'NormalsIndex');u=val(U,b'UV');ui=val(U,b'UVIndex')
assert val(N,b'MappingInformationType')==val(U,b'MappingInformationType')==b'ByPolygonVertex'
assert len(ni)==len(ui)==len(nf)*3

for label,V,C,FC in [('original',oV,oC,oPF),('near',nV,nC,nPF),('archival',cV,cC,cPF)]:
 for k,pts in C.items():
  if not 4<=len(pts)<=50:continue
  p=[V[i] for i in pts]
  a,b=[tuple(map(fn,zip(*p))) for fn in (min,max)]
  if a[2]>3.48 and b[2]<3.84 and -5.<a[0]<-4.7 and -11.5<a[1]<-11.42:
   print('CAP',label,k,len(pts),len(FC[k]),a,b,FC[k],pts)
