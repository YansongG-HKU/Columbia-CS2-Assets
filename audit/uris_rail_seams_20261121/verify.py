"""Fresh Blender readback with exact unchanged attributes, closed bound and visual ray metrics."""
from pathlib import Path
import bpy, math, json, collections, sys, hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(sys.argv[sys.argv.index('--')+1]).resolve()
BASE=D.parent/'cs2-uris-local'/'fresh'
A=json.loads((D/'raw.json').read_text())
T0=Path('/tmp/cs2-lowram.LpRNPF/uris-trial-fresh/UrisHall')
old_rows=json.loads((D.parent/'cs2-uris-local'/'raw.json').read_text())
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
 tag='' if name=='LOD0' else '_LOD1'
 file=f"NA_UrisHall_6x9{tag}.fbx";i=BASE/file;j=D/'fresh'/file
 assert H(i)==row['intermediate_sha256'] and H(j)==row['candidate_sha256']
 v,f,a,scene=load(i,row); w,g,b,scene1=load(j,row)
 assert all(x[1][0]>0 and x[1][1]>0 for x in scene1.values())
 assert len(f)==row['source_triangles'] and len(g)==row['candidate_triangles'] and scene==scene1 and v==w,(name,scene,scene1)
 assert HN(e(f))=={int(k):x for k,x in row['source_edges'].items()} and HN(e(g))=={int(k):x for k,x in row['candidate_edges'].items()}
 removed={i for r in row['seams'] for i in r['source_internal_faces']}
 kept=[i for i in range(len(f)) if i not in removed]; T={i:j for j,i in enumerate(kept)}
 normal_errors={}
 shells={i for s in row['seams'] for i in s['source_union_faces']}
 for j,i in enumerate(kept):
  x,y=a[i],b[j]
  assert f[i]==g[j] and x[2:]==y[2:] and all(k[0]==l[0] for k,l in zip(x[0],y[0]))
  ne=max(math.dist(k[1],l[1]) for k,l in zip(x[0],y[0]))
  if ne:normal_errors[i]=ne
 assert set(normal_errors)<=shells
 assert max(normal_errors.values(),default=0)<2.5e-5,(name,len(normal_errors),normal_errors)
 frame_errors={}
 for j,i in enumerate(kept):
  t=max(math.dist(a,b) for x,y in zip(a[i][1],b[j][1]) for a,b in ((x[0],y[0]),(x[2],y[2])))
  assert all(a[1]==b[1] for a,b in zip(a[i][1],b[j][1]))
  if t:frame_errors[i]=t
 print('TANGENT_ERROR',name,len(frame_errors),sorted(frame_errors.items(),key=lambda r:-r[1])[:12],flush=True)
 assert set(frame_errors)<=shells and max(frame_errors.values(),default=0)<2.5e-5
 # Cumulative comparison, independent geometry and Blender attributes against the unmodified trial.
 oo=old_rows[name];orig=T0/file;assert H(orig)==oo['trial_source_sha256']
 z,F,C,Cscene=load(orig,row);assert Cscene==scene
 initial=[i for i in range(len(F)) if i not in set(oo['removed_faces'])]
 fullkeep=[initial[i] for i in kept]
 assert all(tuple(w[x] for x in g[j])==tuple(z[x] for x in F[i]) and C[i]==a[kept[j]] and C[i][2:]==b[j][2:] for j,i in enumerate(fullkeep))
 B0=BVHTree.FromPolygons(v,f,all_triangles=True); B1=BVHTree.FromPolygons(w,g,all_triangles=True)
 out=[]
 for seam in row['seams']:
  ends=seam['source_internal_faces']; local=seam['source_union_faces']; lfixed=[i for i in local if i not in removed]
  f0=[f[i] for i in local];a0=[a[i] for i in local];f1=[g[T[i]] for i in lfixed];a1=[b[T[i]] for i in lfixed]
  C0=BVHTree.FromPolygons(v,f0,all_triangles=True); C1=BVHTree.FromPolygons(w,f1,all_triangles=True)
  vv=[v[k] for i in local for k in f[i]]
  dims=[(min(v[k] for v in vv),max(v[k] for v in vv)) for k in range(3)]
  TT=e(f1);assert len(TT)==30 and all(len(q)==2 and q[0]==q[1][::-1] for q in TT.values())
  # Interior test from either continuation, along the original extrusion, away from edge precision.
  n=0; moved=(0.,0.)
  for direct in (-1,1):
   O=24.4-.20*direct
   for a2 in range(15):
    for b2 in range(22):
     n+=1;P=Vector((dims[0][0]+(dims[0][1]-dims[0][0])*(a2+.13)/15,O,dims[2][0]+(dims[2][1]-dims[2][0])*(b2+.21)/22))
     d=Vector((0,direct,0)); q,_,_=evalhit(C0,v,f0,a0,P,d);s,_,_=evalhit(C1,w,f1,a1,P,d)
     assert q and s and abs(q.y-24.4)<1e-5 and abs(s.y-(dims[1][0] if direct<0 else dims[1][1]))<2e-5
     moved=(q.y,s.y)
  summaries={}
  for lab,data in [('isolated_rail',(C0,v,f0,a0,C1,w,f1,a1)),('whole_geometry',(B0,v,f,a,B1,w,g,b))]:
   A0,W0,F0,UV0,A1,W1,F1,UV1=data;N=0;R=[];ties=[]
   # Focus on seam y window, including other components, and check outlines on either longitudinal end too.
   for axis in (0,1,2):
    ii,jj=[l for l in range(3) if l!=axis]
    grid=list(dims);grid[1]=(24.18,24.62) if axis!=1 else dims[1]
    for sign in (-1,1):
     for ia in range(27):
      for ja in range(29):
       P=[0.]*3;P[axis]=dims[axis][1 if sign>0 else 0]+sign*(.6 if lab=='whole_geometry' else .03)
       for u,k,delt,Nn in [(ii,ia,.517,27),(jj,ja,.333,29)]:
        lo,hi=grid[u];eps=.10 if lab=='whole_geometry' else .035;P[u]=lo-eps+(hi-lo+2*eps)*(k+delt)/Nn
       d=[0.,0.,0.];d[axis]=-sign
       q,x,ix=evalhit(A0,W0,F0,UV0,Vector(P),Vector(d));s,y,iy=evalhit(A1,W1,F1,UV1,Vector(P),Vector(d))
       N+=1;assert (q is None)==(s is None),(name,lab,axis,sign,P,q,s)
       if q is None:continue
       de=math.dist(q,s); dif=math.dist(x,y)
       if lab=='whole_geometry' and dif>3e-6:
        ny=kept[iy];assert ix!=ny and ix not in removed and de<2e-5
        ties.append([ix,ny,de,dif]);dif=0.
       R.append((de,dif))
   xy=max(t[0] for t in R);um=max(t[1] for t in R)
   assert xy<2e-5 and um<3e-6 and (not ties or lab=='whole_geometry'),(name,lab,xy,um)
   summaries[lab]=dict(samples=N,hits=len(R),max_distance_m=xy,max_uv_delta_non_tied=um,ties=ties)
  out.append(dict(interior_rays=n,exterior_rays=summaries,ends=ends))
 # Use actual full bounds of both old encoded caps, inclusive of every triangulated nearby face.
 boxes=[[(min(v[q][ax] for q in f[i]),max(v[q][ax] for q in f[i])) for ax in range(3)] for i in sorted(removed)]
 def vicinity(V,F,indices):
  D={}
  for k,i in enumerate(indices):
   face=[tuple(V[j]) for j in F[k]]
   bb=[(min(w[ax] for w in face),max(w[ax] for w in face)) for ax in range(3)]
   if any(all(a0<=b1+1e-5 and b0<=a1+1e-5 for (a0,a1),(b0,b1) in zip(bb,bnd)) for bnd in boxes):D[i]=face
  return D
 local=vicinity(v,f,range(len(f)));fresh=vicinity(w,g,kept);assert set(local)-removed==set(fresh) and all(local[i]==fresh[i] for i in fresh)
 # Ray tie geometry (if any) may be outside the local cap probe. Save exact before/after faces.
 tied_geometry={}
 for s in out:
  for ix,iy,*_ in s['exterior_rays']['whole_geometry']['ties']:
   pair=tuple(sorted((ix,iy)))
   tied_geometry[','.join(map(str,pair))]=[[tuple(v[x]) for x in f[i]] for i in pair]
 verify[name]=dict(unchanged_trial_faces=len(g),texture_slots=scene1,triangle_counts=[len(F),len(f),len(g)],
  readback=out,recomputed_normal_errors=normal_errors,recomputed_tangent_errors=frame_errors,local_before=local,local_after=fresh,tied_geometry=tied_geometry)
 print(name,len(F),len(f),len(g),len(local),len(fresh),[[{k:v for k,v in c.items() if k!='ties'} for c in s['exterior_rays'].values()] for s in out],len(tied_geometry),flush=True)
(D/'verified.json').write_text(json.dumps(verify,indent=2)+'\n')
