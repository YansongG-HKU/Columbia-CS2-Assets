"""Prove ZIP extraction resolves every imported FBX image inside the extracted delivery."""
import bpy,sys,json,hashlib
from pathlib import Path
d,o=map(Path,sys.argv[sys.argv.index('--')+1:]); d=d.resolve()
found={}
for p in sorted(d.glob('*.fbx')):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 slots={}
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH':continue
  for m in ob.data.materials:
   for node in m.node_tree.nodes if m and m.node_tree else []:
    if node.type!='TEX_IMAGE' or not node.image:continue
    image=node.image; path=Path(bpy.path.abspath(image.filepath)).resolve()
    assert path.parent==d and path.is_file() and len(image.pixels)>0,(p,image.filepath,d)
    assert path.suffix=='.png'
    slots[path.name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'found_in_extracted_folder':True}
 assert len(slots)>=2
 found[p.name]={'fbx_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'image_slots':slots}
assert len(found)==3
o.write_text(json.dumps(found,indent=2)+'\n')
