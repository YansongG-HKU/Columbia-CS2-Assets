import bpy,sys,collections,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
a,*paths=map(Path,sys.argv[sys.argv.index('--')+1:]); lines=a.read_text().splitlines()
for path in paths:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(path),use_image_search=False)
 o,=[x for x in bpy.context.scene.objects if x.type=='MESH']; m=o.data; v=[o.matrix_world@x.co for x in m.vertices]; m.calc_loop_triangles()
 print('FILE',path,'vert',len(v),'polys',len(m.polygons),'tris',len(m.loop_triangles),'apex',max(p.z for p in v))
 c=collections.Counter((round(p.z,4),round((p.x*p.x+(p.y-9)**2)**.5,4)) for p in v if p.z>33 and (p.x*p.x+(p.y-9)**2)<18**2)
 print('ring counts:',[(tag,n) for tag,n in c.most_common(90)])
 tree=BVHTree.FromPolygons(v,[tuple(p.vertices) for p in m.loop_triangles],all_triangles=True)
 q=[]
 for line in lines:
  x,y,z=map(float,line.split(','));hit=tree.ray_cast(Vector((x,y+9,100)),Vector((0,0,-1)))[0]
  q.append((x,y,z,hit.z if hit else None))
 a.with_name(str(path.stem)+('2-candidate' if 'trial' in str(path) else '')+'.json').write_text(json.dumps(q,separators=(',',':')))
 for r in (0,1,2,3,4,4.6,5,6,7,8,8.82,9,10,11,11.5,12,13,14,15,16):
  print('probe radius',r,[round(tree.ray_cast(Vector((x,y+9,100)),Vector((0,0,-1)))[0].z,4) for x,y in ((r,0),(-r,0),(0,r),(0,-r))])
