import bpy,sys,collections,json
from pathlib import Path
p,out=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=p,use_image_search=False)
o,=[o for o in bpy.context.scene.objects if o.type=='MESH'];m=o.data
a=[]
for v in m.vertices:
 x,y,z=o.matrix_world@v.co;a.append([x,y,z])
m.calc_loop_triangles()
Path(out).write_text(json.dumps({'name':o.name,'vertices':a,'triangles':[list(f.vertices) for f in m.loop_triangles]},separators=(',',':'))+'\n')
print(len(a),len(m.loop_triangles))
