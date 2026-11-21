"""Fresh Blender readback with exact unchanged attributes, closed bound and visual ray metrics."""
from pathlib import Path
import bpy, math, json, collections, sys, hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(sys.argv[sys.argv.index('--')+1]).resolve()
BASE=Path('/tmp/cs2-lowram.LpRNPF/uris-trial-fresh/UrisHall')
A=json.loads((D/'raw.json').read_text())
verify={}
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(x, asset):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(x),use_image_search=False)
 ob,=[a for a in bpy.context.scene.objects if a.type=='MESH'];m=ob.data; m.calc_loop_triangles()
 assert not m.validate(verbose=True,clean_customdata=False)
 scene={i.name:(Path(i.filepath).name,tuple(i.size)) for i in bpy.data.images if i.source=='FILE'}
 field=[[[tuple(m.uv_layers.active.data[j].uv),tuple(m.corner_normals[j].vector)] for j in f.loop_indices] for f in m.polygons]
 m.calc_tangents()
 field=[(ff,[(tuple(m.loops[j].tangent),float(m.loops[j].bitangent_sign),tuple(m.loops[j].bitangent)) for j in f.loop_indices],f.material_index,f.use_smooth) for ff,f in zip(field,m.polygons)]
 v=[o.matrix_world@z.co for z in m.vertices for o in [ob]]; tf=[tuple(t.vertices) for t in m.loop_triangles]; ids=[t.polygon_index for t in m.loop_triangles]
 assert ids==list(range(len(m.polygons)))
 return v,tf,field,scene
def e(F):
 E=collections.defaultdict(list)
 for ff in F:
  for a,b in zip(ff,ff[1:]+ff[:1]):E[min(a,b),max(a,b)].append((a,b))
 return E
def HN(E):return dict(collections.Counter(map(len,E.values())))
def evalhit(B,V,F,U,P,d):
 q,_,ix,_=B.ray_cast(P,d,200)
 if q is None:return None,None,ix
 a,b,c=[V[k] for k in F[ix]]
 sub=lambda a,b:tuple(float(x)-float(y) for x,y in zip(a,b));s=sub(b,a);t=sub(c,a);p=sub(q,a)
 dot=lambda a,b:sum(x*y for x,y in zip(a,b))
 aa,ab,bb=dot(s,s),dot(s,t),dot(t,t);pa,pb=dot(p,s),dot(p,t);n=aa*bb-ab*ab;assert n>0
 r=(pa*bb-pb*ab)/n;w=(pb*aa-pa*ab)/n
 y=[a[0] for a in U[ix][0]];uv=tuple(a*(1-r-w)+b*r+c*w for a,b,c in zip(*y))
 return q,uv,ix
for name,row in A.items():
 file=f"NA_UrisHall_6x9{'' if name=='LOD0' else '_LOD1'}.fbx";i=BASE/file;j=D/'fresh'/file
 assert H(i)==row['trial_source_sha256'] and H(j)==row['patch_sha256']
 v,f,a,scene=load(i,row); w,g,b,scene1=load(j,row)
 assert len(f)==row['triangles_before'] and len(g)==row['triangles_after'] and scene==scene1,(name,scene,scene1)
 assert all(x[1][0]>0 and x[1][1]>0 for x in scene1.values())
 assert len(w)+4==len(v)
 S=set(row['removed_faces']);L=set(row['kept_long_faces']);V=set(row['removed_vertices'])
 F=[i for i in range(len(f)) if i not in S]; J={i:j for j,i in enumerate(F)}
 assert all(tuple(v[k] for k in f[i])==tuple(w[k] for k in g[j]) for j,i in enumerate(F))
 corner_exact={(i,k) for i in F for k in range(3) if a[i][0][k]!=b[J[i]][0][k]}
 assert not corner_exact and all(a[i][2:]==b[J[i]][2:] for i in F),name
 # Blender regenerates tangents from all topology; stored FBX tangents remain byte-exact but
 # quantify any recomputed effect on the pre-existing and surrounding triangles independently.
 dT={};
 for i in F:
  q=max(math.dist(ta,tb) for old,new in zip(a[i][1],b[J[i]][1]) for ta,tb in ((old[0],new[0]),(old[2],new[2])))
  if q>1e-8:dT[i]=q
 assert not any(x[1]!=y[1] for i in F for x,y in zip(a[i][1],b[J[i]][1]))
 assert max(dT.values(),default=0.)<.0001,(name,len(dT),max(dT.values(),default=0))
 assert HN(e(f))=={int(k):vv for k,vv in row['same_index_edges_before'].items()}
 assert HN(e(g))=={int(k):vv for k,vv in row['same_index_edges_after'].items()}
 tall=sorted(L);short=sorted(S);oldfocus=sorted(S|L)
 # Retained closed twelve-face solid, separately verified after FBX reload.
 t=e([g[J[k]] for k in tall]); assert len(t)==18 and all(len(l)==2 and l[0]==l[1][::-1] for l in t.values())
 dims=[(min(q[k] for i in tall for m in f[i] for q in [v[m]]),max(q[k] for i in tall for m in f[i] for q in [v[m]])) for k in range(3)]
 B0=BVHTree.FromPolygons(v,f,all_triangles=True);B1=BVHTree.FromPolygons(w,g,all_triangles=True)
 f0=[f[k] for k in oldfocus];a0=[a[k] for k in oldfocus];f1=[g[J[k]] for k in tall];a1=[b[J[k]] for k in tall]
 C0=BVHTree.FromPolygons(v,f0,all_triangles=True);C1=BVHTree.FromPolygons(w,f1,all_triangles=True)
 trials={}; 
 for lab,mesh in [('isolated_post',(C0,v,f0,a0,C1,w,f1,a1)),('full_building',(B0,v,f,a,B1,w,g,b))]:
  d1,v0,f0_,a0_,d2,v1,f1_,a1_=mesh
  result=[]
  miss_disagreement=0; ties=[];n=0
  for ax in (0,1,2):
   k,l=[x for x in range(3) if x!=ax]
   for side in (-1,1):
    for p in range(27):
     for q in range(37):
      o=[0.]*3;d=[0.]*3
      kk,ll=dims[k],dims[l];pad=(.039 if lab=='isolated_post' else .11)
      a2,b2=kk[0]-pad,kk[1]+pad;c2,d2_=ll[0]-pad,ll[1]+pad
      o[k]=a2+(b2-a2)*(p+.127)/27;o[l]=c2+(d2_-c2)*(q+.333)/37
      o[ax]=dims[ax][1 if side>0 else 0]+side*(.04 if lab=='isolated_post' else 1.25);d[ax]=-side
      n+=1
      p0,u0,x=evalhit(d1,v0,f0_,a0_,Vector(o),Vector(d));p1,u1,y=evalhit(d2,v1,f1_,a1_,Vector(o),Vector(d))
      if (p0 is None)!=(p1 is None):miss_disagreement+=1;continue
      if p0 is None:continue
      sep,duv=math.dist(p0,p1),math.dist(u0,u1)
      if lab=='full_building' and duv>=3.e-6 and sep<2e-5:
       true_y=F[y]; assert x!=true_y
       ties.append(dict(before_face=x,after_face_old_id=true_y,was_removed=x in S,sep_m=sep,uv_delta=duv))
       result.append((sep,0.))
      else:result.append((sep,duv))
  max_p=max(z[0] for z in result);max_uv=max(z[1] for z in result)
  assert miss_disagreement==0 and max_p<2e-5 and max_uv<3e-6,(name,lab,max_p,max_uv,miss_disagreement)
  trials[lab]=dict(first_hit_max_m=max_p,uv_delta_max=max_uv,n=n,n_hits=len(result),coincident_first_hit_choices=ties)
 under=[]
 for i in range(15):
  for j in range(19):
   (x0,x1),(y0,y1),(z0,z1)=dims
   o=Vector((x0+(x1-x0)*(i+.37)/15,y0+(y1-y0)*(j+.57)/19,6.5));d=Vector((0,0,1))
   p,_,_=evalhit(C0,v,f0,a0,o,d);q,_,_=evalhit(C1,w,f1,a1,o,d)
   assert p and q and abs(p.z-7.2)<2e-5 and abs(q.z-10.8)<2e-5
   under.append([p.z,q.z])
 # Full seed bounding region after triangulation, including other surfaces and other vertex IDs.
 seeds=[tuple(tuple(v[k]) for k in f[i]) for i in tall+short]
 sbb=[[(min(q[k] for q in m),max(q[k] for q in m)) for k in range(3)] for m in seeds]
 def vicinity(V,F,ind):
  res={}
  for k,i in enumerate(ind):
   tr=[tuple(V[j]) for j in F[k]]; bb=[(min(q[t] for q in tr),max(q[t] for q in tr)) for t in range(3)]
   if any(all(a0<=b1+1e-5 and b0<=a1+1e-5 for (a0,a1),(b0,b1) in zip(bb,bnd)) for bnd in sbb):res[i]=tr
  return res
 before=vicinity(v,f,range(len(f)));after=vicinity(w,g,F)
 assert set(before)-S==set(after) and all(before[i]==after[i] for i in after)
 verify[name]=dict(removed=sorted(S),retained_uv_normals_faces=len(F),texture_slots=scene1,regenerated_tangent_faces_changed=len(dT),
  regenerated_tangent_max_diff=max(dT.values(),default=0.),
  oriented_closed_post_edges=18,first_hit_tests=trials,inside_positive_z_tests=len(under),local_before=before,local_after=after)
 print(name,{k:v for k,v in verify[name].items() if not k.startswith('local_') and k!='first_hit_tests'},flush=True)
(D/'verified.json').write_text(json.dumps(verify,indent=2)+'\n')
