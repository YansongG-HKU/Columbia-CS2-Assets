"""Save a separate editable LOD1-only source and verify it reopens with packed geometry and local maps."""
import bpy,sys,json,hashlib
from pathlib import Path
D=Path(sys.argv[sys.argv.index('--')+1]).resolve()
p=D/'NA_LernerHall_9x9_LOD1.fbx'
out=D/'LernerHall-repaired-LOD1-editable.blend'
mode=sys.argv[-1] if sys.argv[-1]=='check' else 'save'
def audit():
 o,=[o for o in bpy.context.scene.objects if o.type=='MESH'];m=o.data
 assert len(m.polygons)==15304 and len(m.vertices)==7862 and len(m.uv_layers)==1
 image=[n.image for mat in m.materials if mat and mat.node_tree for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
 assert len(image)>=2
 a={}
 for i in image:
  name=Path(i.filepath).name
  target=D/name
  assert target.is_file()
  a[name]=hashlib.sha256(target.read_bytes()).hexdigest()
 return a
if mode=='save':
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 actual=audit()
 for n in bpy.data.images:
  if n.source=='FILE':
   name=Path(n.filepath).name
   assert (D/name).exists()
   n.filepath='//'+name
 bpy.context.preferences.filepaths.save_version=0
 assert not out.exists()
 bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False,compress=True)
bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False)
colors=audit()
for image in bpy.data.images:
 if image.source=='FILE':
  op=Path(bpy.path.abspath(image.filepath)).resolve()
  assert image.filepath.startswith('//') and op.parent==D and op.is_file()
  assert len(image.pixels)>0
print('REOPENED',out.name,colors)
