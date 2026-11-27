"""Independent clean FBX reread. Preserve retained corners, identify contact types per donor."""
import bpy,sys,collections,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(sys.argv[-1]).resolve(); S=D/'input/import-assets/PupinHall'; C=D/'trial'; stem='NA_PupinHall_8x3'
P=json.loads((D/'donor-plan.json').read_text())['components']; retained=36594
bpy.ops.wm.read_factory_settings(use_empty=True)
def load(p):
 existing=set(bpy.context.scene.objects)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 o,=[o for o in bpy.context.scene.objects if o.type=='MESH' and o not in existing];m=o.data
 assert not m.validate(verbose=True,clean_customdata=False)
 assert all(p.area>1e-10 and len(p.vertices)==3 for p in m.polygons)
 V=[o.matrix_world@v.co for v in m.vertices];F=[tuple(t.vertices) for t in m.polygons]
 U=[tuple(tuple(m.uv_layers[0].data[i].uv) for i in t.loop_indices) for t in m.polygons]
 N=[tuple(tuple((o.matrix_world.to_3x3()@m.corner_normals[i].vector).normalized()) for i in t.loop_indices) for t in m.polygons]
 return V,F,U,N
A=lambda v:[list(map(min,zip(*v))),list(map(max,zip(*v)))]
p0=S/(stem+'_LOD1.fbx'); p1=C/p0.name
V,F,U,N=load(p0); v,f,u,n=load(p1); w,g,_,_=load(S/(stem+'.fbx'))
assert (len(V),len(F),len(v),len(f),len(g))==(24279,36644,24561,37258,82336)
affected={tuple(sorted(x['old_vertex_ids'])) for x in P}
keep=[i for i,a in enumerate(F) if tuple(sorted(a)) not in affected]
assert len(keep)==retained and A(V)==A(v)
assert all([V[k] for k in F[j]]==[v[k] for k in f[i]] and U[j]==u[i] and N[j]==n[i] for i,j in enumerate(keep))
def context(v,f):
 graph=collections.defaultdict(set)
 for q in f:
  for x in q:graph[x].update(q)
 left=set(graph); inv={}; cc={}
 while left:
  k=left.pop(); q=[k]; a={k}
  while q:
   j=q.pop(); b=graph[j]&left; q.extend(b);left-=b;a|=b
  i=min(a);cc[i]=(len(a),A([v[j] for j in a]))
  for x in a:inv[x]=i
 return v,f,BVHTree.FromPolygons(v,f,all_triangles=True,epsilon=1e-8),inv,cc
def overlaps(v,f,G,exclude_same=False):
 vv,ff,bvh,inv,cc=G
 bv=BVHTree.FromPolygons(v,f,all_triangles=True,epsilon=1e-8)
 old={tuple(sorted(tuple(v[i]) for i in q)) for q in f} if exclude_same else set()
 rr=collections.defaultdict(list);loc=[]
 host_pts={}
 for a,b in bv.overlap(bvh):
  xyz=[vv[i] for i in ff[b]]
  if tuple(sorted(tuple(p) for p in xyz)) in old:continue
  k=inv[ff[b][0]]
  r0,r1=A(xyz); u0,u1=A([v[i] for i in f[a]])
  contact=[[max(i,j) for i,j in zip(u0,r0)],[min(i,j) for i,j in zip(u1,r1)]]
  rr[k].append([a,b,contact])
 return {str(i):{'pairs':s,'host_vertices':cc[i][0],'host_bounds':cc[i][1]} for i,s in sorted(rr.items())}
rest=context(v,f[:retained]); near=context(w,g)
wins={}
for label in ('Gls','Win'):
 nw,nf,_,_=load(S/(stem+'_LOD1_'+label+'.fbx'))
 qw,qf,_,_=load(S/(stem+'_'+label+'.fbx'))
 assert nw==qw and nf==qf,(label,'submesh LOD0 and LOD1 differ')
 wins[label]=context(nw,nf)
res=[]; ix=retained; ss=0; allparts=[]
for j,p in enumerate(P):
 k=len(p['donor_triangles']); subset=f[ix:ix+k]
 ids=sorted({v for q in subset for v in q}); vi={o:i for i,o in enumerate(ids)}
 xyz=[v[a] for a in ids]; ff=[tuple(vi[a] for a in t) for t in subset]
 assert max((a-Vector(b)).length for a,b in zip(xyz,p['world_vertices']))<5e-6
 assert ff==[tuple(x) for x in p['donor_triangles']]
 assert max(math.dist(aa,bb) for a,b in zip(u[ix:ix+k],p['donor_uv_corners']) for aa,bb in zip(a,b))<1e-7
 E=collections.defaultdict(list)
 for t in ff:
  for x,y in zip(t,t[1:]+t[:1]):E[min(x,y),max(x,y)].append((x,y))
 assert len(E)==(18 if p['family']=='upper_rods' else 30) and all(len(es)==2 and es[0]==es[1][::-1] for es in E.values())
 bvh=BVHTree.FromPolygons(xyz,ff,all_triangles=True,epsilon=1e-8)
 assert all(not bvh.overlap(q) for q in allparts)
 allparts.append(bvh); ss+=len(E);ix+=k
 r={label:overlaps(xyz,ff,C,label=='near') for label,C in [('near',near),('mid',rest),*wins.items()]}
 res.append({'donor':j,'family':p['family'],'center':p['center'],'bounds':A(xyz),'near':r['near'],'mid':r['mid'],'Gls':r['Gls'],'Win':r['Win']})
 print(j,p['family'],[round(x,3) for x in p['center']],{a:{k:(len(t['pairs']),t['host_vertices']) for k,t in z.items()} for a,z in r.items()})
assert ix==len(f)
(D/'contacts.json').write_text(json.dumps({'paired_edges':ss,'unchanged_triangles':retained,'aabb_exact':A(v),'components':res},indent=2)+'\n')
