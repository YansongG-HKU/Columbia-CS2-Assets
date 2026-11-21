import bpy,sys,math,json,collections
from pathlib import Path
from mathutils import Vector
from mathutils.kdtree import KDTree
D=Path(sys.argv[sys.argv.index('--')+1]).resolve()
s=D/'input/import-assets/JohnJayHall'; p=s/'NA_JohnJayHall_8x4_LOD1.fbx'; near=s/'NA_JohnJayHall_8x4.fbx'
raw=json.loads((D/'raw-pairs.json').read_text())
def load(path):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(path),use_image_search=False)
 ob,=[o for o in bpy.context.scene.objects if o.type=='MESH'];m=ob.data;m.calc_loop_triangles()
 V=[ob.matrix_world@v.co for v in m.vertices];F=[list(f.vertices) for f in m.polygons]
 N=[ob.matrix_world.to_3x3()@f.normal for f in m.polygons]
 UV=[[list(m.uv_layers[0].data[i].uv) for i in f.loop_indices] for f in m.polygons]
 return V,F,N,UV,ob.matrix_world.copy()
V,F,N,UV,M=load(p);print('transform',list(map(tuple,M)),flush=True)
G=collections.defaultdict(list)
for i,f in enumerate(F):G[tuple(sorted(f))].append(i)
for a in raw:
 k=tuple(a['indices'])
 ids=G.get(k)
 assert ids and len(ids)==1,(ids,k)
 i=ids[0]
 vv=[V[x] for x in F[i]]; a['readback_face_id']=i;a['readback_world_xyz']=[list(v) for v in vv]
 a['readback_world_normal']=list(N[i].normalized());a['readback_uv_by_vertex']={int(j):k for j,k in zip(F[i],UV[i])}
 a['center']=list(sum(vv,Vector())/3)
 dif=[]
 for z0 in ('corner_uv_first','corner_uv_second'):
  t={int(k):v for k,v in a[z0].items()};dif.append(max(math.dist(t[i],v) for i,v in zip(F[i],UV[i])))
 a['against_two_sources_uv_max_deltas']=dif
 print(a['pair'],'center',a['center'],'n',a['readback_world_normal'],'uv-delta',dif)
paths=[near,D/'main/fbx/split/NA_JohnJayHall_8x4_LOD1.fbx']
for q in paths:
 O,H,N0,U0,T0=load(q); kd=KDTree(len(O))
 for i,x in enumerate(O):kd.insert(x,i)
 kd.balance()
 graph=collections.defaultdict(set); grp=collections.defaultdict(list)
 for f in H:
  for i in f:graph[i].update(f)
 c={}
 left=set(graph); components={}
 for seed in sorted(left):
  if seed not in left:continue
  left.remove(seed);ix={seed};st=[seed]
  while st:
   i=st.pop();ns=graph[i]&left
   left-=ns;ix|=ns;st.extend(ns)
  k=min(ix)
  for i in ix:c[i]=k
  oo=[O[i] for i in ix]
  components[k]={'v':len(ix),'bounds':[list(map(min,zip(*oo))),list(map(max,zip(*oo)))]}
 for i,f in enumerate(H):grp[c[f[0]]].append(i)
 for a in raw:
  c0=Vector(a['center'])
  samples=kd.find_range(c0,.52)
  ids=collections.Counter(c[i] for v,i,d in samples)
  name='near' if q==near else 'main_lod1'
  small=[{**components[z],'near_component_verts':counts,'component_key':z,'faces':len(grp[z])} for z,counts in ids.items()]
  a[name]=small
  print(name,a['pair'],small)
(D/'world-pairs.json').write_text(json.dumps(raw,indent=2)+'\n')
