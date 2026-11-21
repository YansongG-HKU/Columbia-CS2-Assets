"""Reimport the exact unzipped Pupin Hall payload."""
from pathlib import Path
import json,sys,math
import bpy
from mathutils import Vector
asset,renders,report=(Path(x).resolve() for x in sys.argv[sys.argv.index('--')+1:])
stem='NA_PupinHall_8x3'
expected={'':82336,'_LOD1':37286,'_LOD2':84,'_Gls':112,'_LOD1_Gls':112,'_Win':1458,'_LOD1_Win':1458}
data={}
renders.mkdir()
def pull(suffix):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    p=asset/(stem+suffix+'.fbx')
    bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
    ob,=[o for o in bpy.context.scene.objects if o.type=='MESH']
    m=ob.data;m.calc_loop_triangles()
    if not m.uv_layers.active or len(m.loop_triangles)!=expected[suffix]:raise ValueError('Mesh/UV unexpected')
    coords=[ob.matrix_world@v.co for v in m.vertices]
    if not all(math.isfinite(c) for p in coords for c in p):raise ValueError('Nonfinite geometry')
    if any((coords[t.vertices[1]]-coords[t.vertices[0]]).cross(coords[t.vertices[2]]-coords[t.vertices[0]]).length_squared<=1e-18 for t in m.loop_triangles):
        raise ValueError('Degenerate geometry')
    bbox=[[op(t[k] for t in coords) for k in range(3)] for op in (min,max)]
    imgs={}
    for im in bpy.data.images:
        if im.source!='FILE':continue
        f=Path(bpy.path.abspath(im.filepath)).resolve()
        if f.parent!=asset or not f.is_file():raise ValueError('Unexpected image resolve path')
        im.reload();_=im.pixels[0];imgs[f.name]=list(im.size)
    d=(1024 if suffix=='_LOD2' else 4096)
    expected_imgs={f'{stem}{suffix if suffix=="_LOD2" else ""}_{n}.png' for n in ('BaseColor','Normal','Emissive')} if suffix in ('','_LOD1','_LOD2') else set()
    if set(imgs)!=expected_imgs or any(v!=[d,d] for v in imgs.values()):raise ValueError('Unexpected exact image inventory')
    data[p.name]={'triangles':len(m.loop_triangles),'bounds_m':bbox,'images':imgs}
    return ob,bbox

for suffix in expected:
    ob,bbox=pull(suffix)
    assert not ob.data.validate(verbose=True,clean_customdata=False)
bpy.ops.wm.read_factory_settings(use_empty=True)
decoded={}
for f in sorted(asset.glob('*.png')):
    im=bpy.data.images.load(str(f),check_existing=False);_=im.pixels[0]
    size=1024 if '_LOD2_' in f.name else 4096
    if list(im.size)!=[size,size]:raise ValueError('PNG dimensions unexpected')
    decoded[f.name]=list(im.size)
    bpy.data.images.remove(im)
if len(decoded)!=10:raise ValueError('Missing packaged PNG file')
report.write_text(json.dumps({'separate_FBX':data,'all_PNGs_decoded':decoded,
 'scope':'Offline package, independent mesh and texture checks, not combined shader or Editor test'},indent=2)+'\n')
print('PUPIN_TRIAL_PACKAGE_READBACK_PASS',len(data),len(decoded))
