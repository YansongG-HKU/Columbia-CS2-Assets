"""Trace each isolated reversed duplicate to the same intact 12-vertex ornament in two assets."""
import bpy,sys,collections,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from io_scene_fbx import parse_fbx
d=Path(sys.argv[sys.argv.index('--')+1]).resolve()
P=d/'input/import-assets/JohnJayHall'; near=P/'NA_JohnJayHall_8x4.fbx'; old=P/'NA_JohnJayHall_8x4_LOD1.fbx'; control=d/'main/fbx/split/NA_JohnJayHall_8x4_LOD1.fbx'
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
P0=json.loads((d/'world-pairs.json').read_text())
done=set(); plan=[]
ct=lambda v,ii:sum((v[i] for i in ii),Vector())/len(ii)
def choose(v,cs,fs,center):
 out=[]
 for k,pts in cs.items():
  if len(pts)!=12 or len(fs[k])!=20:continue
  Q=ct(v,pts)
  heights=[v[i].z for i in pts]
  if abs(min(heights)-2.88)>.00002 or abs(max(heights)-3.54)>.00002:continue
  dist=(Q.xy-center.xy).length;out.append((dist,k,pts))
 q=sorted(out);assert q[0][0]<.0033 and q[1][0]>.26,q[:4]
 return q[0]
for r in P0:
 vv=r['indices']; ctr=Vector(r['center'])
 dist,k,ix=choose(nV,nC,nPF,ctr); ds,k1,idx=choose(cV,cC,cPF,ctr)
 assert k not in done;done.add(k)
 assert all(min((nV[i]-cV[j]).length for j in idx)<.000015 for i in ix)
 comp=set(ix); oi={v:j for j,v in enumerate(ix)}; V=[nv[i] for i in ix]; F=[]; Us=[]; Ns=[]
 rings=collections.defaultdict(list)
 for j in nPF[k]:
  q=nf[j];assert set(q)<=comp
  F.append([oi[i] for i in q]);
  Us.append([list(u[2*ui[3*j+b]:2*ui[3*j+b]+2]) for b in range(3)])
  Ns.append([list(n[ni[3*j+b]*3:ni[3*j+b]*3+3]) for b in range(3)])
  for a,b in zip(q,q[1:]+q[:1]):rings[min(a,b),max(a,b)].append((a,b))
 assert all(len(a)==2 and a[0]==a[1][::-1] for a in rings.values()) and len(rings)==30
 for u0,n0 in zip(Us,Ns):
  assert all(-.001<x<1.001 for uv in u0 for x in uv)
  assert all(abs(Vector(a).length-1)<.001 for a in n0)
 vol=sum(nV[a].dot(nV[b].cross(nV[c])) for a,b,c in (nF[i] for i in nPF[k]))/6
 assert .001<vol<.004,vol
 plan.append({'old_vertex_ids':vv,'old_face_pair':r['pair'],'center':list(ctr),'world_vertices':[list(nV[i]) for i in ix],
   'donor_raw_vertices':V,'donor_triangles':F,'donor_uv_corners':Us,'donor_normals_corners':Ns,
   'near_component_key':k,'main_old_source_component_key':k1,'source_near_basis':list(map(list,nM)),
   'donor_max_hausdorff_from_archival_m':max(min((nV[i]-cV[j]).length for j in idx) for i in ix),
   'valid_solid_volume_m3':vol,'nearest_original_component_center_xy_delta_m':dist})
 print('pair',r['pair'],'donors',k,k1,'bound height',min(nV[i].z for i in ix),max(nV[i].z for i in ix),'max error',plan[-1]['donor_max_hausdorff_from_archival_m'])
(d/'donor-plan.json').write_text(json.dumps({'old_sha256':sha(old),'near_donor_sha256':sha(near),'archival_7400_sha256':sha(control),'components':plan},indent=2)+'\n')
