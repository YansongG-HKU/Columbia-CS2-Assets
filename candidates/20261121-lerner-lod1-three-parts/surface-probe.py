from pathlib import Path
import bpy,sys,collections,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.kdtree import KDTree
D=Path(sys.argv[-1]).resolve(); S=D/'input/import-assets/LernerHall'; stem='NA_LernerHall_9x9'
rr=json.loads((D/'raw-pairs.json').read_text())
def load(p):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 ob,=[x for x in bpy.context.scene.objects if x.type=='MESH'];m=ob.data
 V=[ob.matrix_world@x.co for x in m.vertices]; F=[tuple(p.vertices) for p in m.polygons]
 graph=collections.defaultdict(set); fs=collections.defaultdict(list)
 for f in F:
  for i in f:graph[i].update(f)
 left=set(graph); Cs={}; inv={}
 while left:
  i=left.pop();q=[i]; seen={i}
  while q:
   j=q.pop(); a=graph[j]&left;left-=a;seen|=a;q.extend(a)
  k=min(seen);Cs[k]=sorted(seen)
  for i in seen:inv[i]=k
 for j,f in enumerate(F):fs[inv[f[0]]].append(j)
 print(p,len(V),len(F),ob.matrix_world,flush=True)
 return V,F,Cs,inv,fs
v,f,c,i,fs=load(S/(stem+'_LOD1.fbx')); points=[]
for r in rr:
 s=r['indices']; ctr=sum((v[a] for a in s),Vector())/3;points.append([v[x] for x in s])
 print('target',list(ctr),'comp',[(i[k],len(c[i[k]]),len(fs[i[k]])) for k in s])
for p in [S/(stem+'.fbx'),D/'main/fbx/split'/ (stem+'_LOD1.fbx')]:
 V,F,C,I,G=load(p)
 kd=KDTree(len(V))
 for j,a in enumerate(V):kd.insert(a,j)
 kd.balance()
 for corners in points:
  bycorner=[]
  for point in corners:
   acc={}
   for _,j,d in kd.find_range(point,0.50):
    if I[j] not in acc or d<acc[I[j]]: acc[I[j]]=d
   bycorner.append(acc)
  ids=set.intersection(*(set(a) for a in bycorner))
  vals=[(max(a[i] for a in bycorner), i, len(C[i]),len(G[i]),[list(map(fn,zip(*(V[j] for j in C[i])))) for fn in (min,max)]) for i in ids]
  print('ALL_CORNERS', [list(x) for x in corners],sorted(vals)[:12])
 T=BVHTree.FromPolygons(V,F,all_triangles=True)
 for r,l in enumerate(points):
  for q in [sum(l,Vector())/3,*l]:
   pv,nor,j,dd=T.find_nearest(q)
   print('NEAREST',r,list(q),list(pv),dd,I[F[j][0]],len(C[I[F[j][0]]]),len(G[I[F[j][0]]]),[list(map(fn,zip(*(V[j] for j in C[I[F[j][0]]])))) for fn in (min,max)])
