import bpy,sys,collections,json
from pathlib import Path
from mathutils.bvhtree import BVHTree
bpy.ops.wm.read_factory_settings(use_empty=True)
old,new,p=map(Path,sys.argv[sys.argv.index('--')+1:])
def load(p):
 u=set(bpy.context.scene.objects);bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False);o,=[o for o in bpy.context.scene.objects if o not in u and o.type=='MESH']
 a=[o.matrix_world@v.co for v in o.data.vertices]; f=[tuple(p.vertices) for p in o.data.polygons]; lf=[]; inds=[]
 for i,t in enumerate(f):
  if all(a[j].z>32 and abs(a[j].x)<18 and abs(a[j].y-9)<18 for j in t):inds.append(i);lf.append(t)
 b=BVHTree.FromPolygons(a,lf,all_triangles=True,epsilon=1e-7)
 hit={(inds[i],inds[j]) for i,j in b.overlap(b) if i<j and set(lf[i]).isdisjoint(lf[j])}
 return a,f,hit
V,F,A=load(old); vr,fr,B=load(new); assert F==fr and len(V)==len(vr)
d={i for i,(a,b) in enumerate(zip(V,vr)) if (a-b).length>1e-6}
desc=collections.Counter(); result=[]
for i,j in sorted(B-A):
 row=[]
 for k in (i,j):
  t=F[k]
  row.append({'face':k,'ids':t,'r':[round((V[i].x**2+(V[i].y-9)**2)**.5,3) for i in t],
             'oldz':[round(V[i].z,3) for i in t],'newz':[round(vr[i].z,3) for i in t],'changed':[i in d for i in t]})
 desc[tuple(sorted(tuple(sorted(s['oldz'])) for s in row))]+=1
 result.append(row)
p.write_text(json.dumps({'added_n':len(B-A),'before':len(A),'after':len(B),'groups':desc.most_common(36),'example':result[:40]},indent=2))
print('pairs',len(A),len(B),len(B-A),'top groups',desc.most_common(24))
