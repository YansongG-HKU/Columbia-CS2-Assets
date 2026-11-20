"""Independently import original and tangent candidates; compare mesh/UV/normal state."""
import bpy,hashlib,json,struct,sys
from pathlib import Path
original,candidate,out=[Path(x).resolve() for x in sys.argv[sys.argv.index('--')+1:]]
def snap(f):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(f),use_image_search=False)
    ob,=[o for o in bpy.context.scene.objects if o.type=='MESH'];m=ob.data
    m.calc_loop_triangles()
    h=hashlib.sha256()
    for v in m.vertices:h.update(struct.pack('3f',*(ob.matrix_world@v.co)))
    for p in m.polygons:
        h.update(struct.pack('II',len(p.vertices),p.material_index))
        for j in p.vertices:h.update(struct.pack('I',j))
    uv=m.uv_layers.active.data
    for l in m.loops:
        h.update(struct.pack('2f',*uv[l.index].uv))
        h.update(struct.pack('3f',*m.corner_normals[l.index].vector))
    images={}
    for im in bpy.data.images:
        if im.source!='FILE':continue
        path=Path(bpy.path.abspath(im.filepath)).resolve()
        if path.parent!=f.parent or not path.is_file():raise ValueError('External texture not in package')
        im.reload();_=im.pixels[0];images[path.name]=list(im.size)
    if len(images)!=3 or any(v!=[4096,4096] for v in images.values()):raise ValueError('Wrong texture table')
    return {'mesh_corner_state_sha256':h.hexdigest(),'triangles':len(m.loop_triangles),'images':images,'materials':[ma.name for ma in m.materials]}
report={}
for f in sorted(candidate.glob('*.fbx')):
    old,new=snap(original/f.name),snap(f)
    if old!=new:raise ValueError(f'Reimport from clean folders changed non-tangent attributes: {f.name}')
    report[f.name]=new
if len(report)!=2:raise ValueError('Expected both FBXs')
out.write_text(json.dumps(report,indent=2)+'\n')
print('CLEAN_TANGENT_REIMPORT_PASS',len(report))
