"""Check repaired entrance ornaments against the independently imported glass and window meshes."""
from pathlib import Path
import json,sys
import bpy
from mathutils.bvhtree import BVHTree
D=Path(sys.argv[-1]).resolve(); S=D/'fresh/import-assets/JohnJayHall'; stem='NA_JohnJayHall_8x4'
plan=json.loads((D/'donor-plan.json').read_text())
def load(s):
 before=set(bpy.context.scene.objects)
 bpy.ops.import_scene.fbx(filepath=str(S/(stem+s+'.fbx')),use_image_search=False)
 o,=[o for o in bpy.context.scene.objects if o.type=='MESH' and o not in before]
 return [o.matrix_world @ v.co for v in o.data.vertices],[tuple(f.vertices) for f in o.data.polygons]
bpy.ops.wm.read_factory_settings(use_empty=True)
v,f=load('_LOD1'); rr={}
# Directly compare repaired triangles and the proven original donor triangles in archive-equivalent world coordinates.
for ext in ('_LOD1_Gls','_LOD1_Win'):
 pos,faces=load(ext); target=BVHTree.FromPolygons(pos,faces,all_triangles=True,epsilon=1e-8)
 nv,nf=load(ext.replace('_LOD1',''))
 assert faces==nf and len(pos)==len(nv)
 vertex_delta=max((a-b).length for a,b in zip(pos,nv))
 assert vertex_delta<=.000002,(ext,vertex_delta)
 ret=[]
 for j,p in enumerate(plan['components']):
  ix=range(43774+20*j,43774+20*(j+1)); f0=[f[i] for i in ix]
  idx0=sorted({i for s in f0 for i in s}); l={i:k for k,i in enumerate(idx0)}
  obv=[v[i] for i in idx0]; obf=[tuple(l[i] for i in s) for s in f0]
  O=BVHTree.FromPolygons(obv,obf,all_triangles=True,epsilon=1e-8)
  Q=BVHTree.FromPolygons(p['world_vertices'],p['donor_triangles'],all_triangles=True,epsilon=1e-8)
  overlap=sorted(O.overlap(target)); original=sorted(Q.overlap(target))
  assert overlap==original,(j,ext,overlap,original)
  ret.append({'donor':j,'pairs':len(overlap)})
 rr[ext]={'matching_near_submesh_max_vertex_delta_m':vertex_delta,'donors':ret}
(D/'split-readback.json').write_text(json.dumps(rr,indent=2)+'\n')
print(rr)
