import bpy,sys,collections,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(sys.argv[-1]).resolve(); S=D/'input/import-assets/LernerHall'; C=D/'trial'; stem='NA_LernerHall_9x9'
plan=json.loads((D/'donor-plan.json').read_text())['components']
bpy.ops.wm.read_factory_settings(use_empty=True)
def load(p):
 before=set(bpy.context.scene.objects)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 ob,=[o for o in bpy.context.scene.objects if o not in before and o.type=='MESH'];m=ob.data
 V=[ob.matrix_world @ v.co for v in m.vertices];F=[tuple(t.vertices) for t in m.polygons]
 U=[tuple(tuple(m.uv_layers[0].data[i].uv) for i in t.loop_indices) for t in m.polygons]
 N=[tuple(tuple((ob.matrix_world.to_3x3()@m.corner_normals[i].vector).normalized()) for i in t.loop_indices) for t in m.polygons]
 assert not m.validate(verbose=True,clean_customdata=False)
 assert all(p.area>1e-10 and len(p.vertices)==3 for p in m.polygons)
 return ob,V,F,U,N
A=lambda v:[list(map(min,zip(*v))),list(map(max,zip(*v)))]
p0=S/(stem+'_LOD1.fbx'); p1=C/p0.name; pn=S/(stem+'.fbx')
o,V,F,U,N=load(p0);a,v,f,u,n=load(p1); q,w,g,uu,nn=load(pn)
assert [len(F),len(f),len(g),len(v)]==[15271,15304,30084,7862]
pm={tuple(sorted(x['old_vertex_ids'])) for x in plan}
keep=[i for i,s in enumerate(F) if tuple(sorted(s)) not in pm]
assert len(keep)==15268 and A(V)==A(v)
for i,j in enumerate(keep):
 assert [V[k] for k in F[j]]==[v[k] for k in f[i]] and U[j]==u[i] and N[j]==n[i]
r={}
owe,wwn,gwn,_,_=load(S/(stem+'_Win.fbx'))
ow,ww,gw,_,_=load(S/(stem+'_LOD1_Win.fbx'))
assert wwn==ww and gwn==gw
def parts(vv,ff):
 graph=collections.defaultdict(set)
 for s in ff:
  for i in s:graph[i].update(s)
 left=set(graph); gs={}; inv={}
 while left:
  k=left.pop(); p={k}; l=[k]
  while l:
   a=l.pop(); b=left & graph[a];left-=b;p|=b;l.extend(b)
  j=min(p);gs[j]=sorted(p)
  for x in p:inv[x]=j
 return gs,inv
def diff(v,f,contextV,contextF):
 cs,inv=parts(contextV,contextF)
 L=BVHTree.FromPolygons(v,f,all_triangles=True,epsilon=1e-8)
 J=BVHTree.FromPolygons(contextV,contextF,all_triangles=True,epsilon=1e-8)
 approx=collections.defaultdict(list)
 planKey=set(tuple(sorted(tuple(x) for x in [v[i] for i in q])) for q in f)
 for a,b in L.overlap(J):
  ff=contextF[b]
  if tuple(sorted(tuple(contextV[i]) for i in ff)) in planKey:continue
  j=inv[ff[0]]
  row=sorted(tuple(contextV[i]) for i in ff)
  approx[j].append([a,b,row])
 return {k:{'n':len(ts),'geometry':A([contextV[i] for i in cs[k]]),'n_v':len(cs[k]),'world_face_corners':ts} for k,ts in approx.items()}
for j,p in enumerate(plan):
 s=f[15268+j*12:15268+(j+1)*12]
 ind=sorted({k for a in s for k in a}); um={a:i for i,a in enumerate(ind)}
 vv=[v[a] for a in ind]; ff=[tuple(um[a] for a in t) for t in s]
 assert max((a-Vector(b)).length for a,b in zip(vv,p['world_vertices']))<.00001
 assert ff==[tuple(x) for x in p['donor_triangles']]
 assert max(math.dist(aa,bb) for a,b in zip(u[15268+12*j:15268+12*(j+1)],p['donor_uv_corners']) for aa,bb in zip(a,b))<1e-7
 E=collections.defaultdict(list)
 for t in ff:
  for x,y in zip(t,t[1:]+t[:1]): E[min(x,y),max(x,y)].append((x,y))
 assert len(E)==18 and all(len(val)==2 and val[0]==val[1][::-1] for val in E.values())
 near=diff(vv,ff,w,g); current=diff(vv,ff,v,f[:15268])
 excluded=diff(vv,ff,v,f[15268:15268+j*12]+f[15268+12*(j+1):]);assert not excluded
 near_pairs=sorted((a,tuple(tuple(round(k,5) for k in c) for c in pts)) for hh in near.values() for a,b,pts in hh['world_face_corners'])
 current_pairs=sorted((a,tuple(tuple(round(k,5) for k in c) for c in pts)) for hh in current.values() for a,b,pts in hh['world_face_corners'])
 assert near_pairs==current_pairs,(j,near_pairs,current_pairs)
 wi=diff(vv,ff,ww,gw)
 r[str(j)]={'bound':A(vv),'near':near,'candidate':current,'window':wi,'exact_near_inherited_body_contact_pairs_10um':len(current_pairs),'window_parity_near_mid':True}
 print(j,{k:{key:(x['n'],x['n_v'],x['geometry']) for key,x in val.items()} for k,val in r[str(j)].items() if isinstance(val,dict)})
(D/'contacts.json').write_text(json.dumps(r,indent=2)+'\n')
