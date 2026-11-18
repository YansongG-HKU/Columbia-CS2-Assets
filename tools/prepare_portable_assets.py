"""Conservative portable CS2 asset copy, not a texture or geometry optimizer.
Run using Blender's Python and io_scene_fbx, e.g.:
blender -b --factory-startup --python-exit-code 1 --python prepare_portable_assets.py -- --repository ./repository --output ./portable --clean ./readback --buildings AveryHall,LewisohnHall
Output and clean folders must not exist and must remain outside the input repository.
Original files are never overwritten. Existing geometry defects remain defects.
Requires layout Building/{textures,cs2_import_candidates,settings.json,*.blend}.
No game/editor import, COK certification or publishing is performed.
"""
import array
from io_scene_fbx import parse_fbx,encode_bin
import bpy,pathlib,json,hashlib,struct,shutil
import argparse,sys
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=argparse.ArgumentParser();a.add_argument('--repository',required=True);a.add_argument('--output',required=True);a.add_argument('--buildings',required=True);a.add_argument('--clean',required=True);a=a.parse_args(args)
R=pathlib.Path(a.repository).resolve();O=pathlib.Path(a.output).resolve();names=a.buildings.split(',')
assert not O.exists(), 'Output must be new to prevent overwriting a prior candidate'
assert not O.is_relative_to(R), 'Keep isolated output outside original repository'
C=pathlib.Path(a.clean).resolve();assert not C.exists();assert not C.is_relative_to(R);assert C!=O;assert not C.is_relative_to(O);assert not O.is_relative_to(C)
O.mkdir(parents=True);out={}
for name in names:
 assert name and '/' not in name and '\\' not in name and name not in ['.','..']
 assert (R/name/'cs2_import_candidates').is_dir()
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snap():
 d={}
 for o in bpy.data.objects:
  if o.type!='MESH':continue
  m=o.data;m.calc_loop_triangles()
  geo=hashlib.sha256();uv=hashlib.sha256()
  for v in m.vertices:geo.update(struct.pack('3f',*v.co))
  for f in m.polygons:geo.update(struct.pack(str(len(f.vertices))+'I',*f.vertices))
  for layer in m.uv_layers:
   for l in layer.data:uv.update(struct.pack('2f',*l.uv))
  d[o.name]={'geometry_sha':geo.hexdigest(),'uv_sha':uv.hexdigest(),'triangles':len(m.loop_triangles),'loops':len(m.loops),'uv_outside':sum(any(x<-.00001 or x>1.00001 for x in l.uv) for layer in m.uv_layers for l in layer.data),'images':sorted({n.image.name for mat in m.materials if mat and mat.use_nodes for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image})}
 return d
for name in names:
 src=R/name;imp=O/'import-assets'/name;dst=O/'source'/name;imp.mkdir(parents=True,exist_ok=True);dst.mkdir(parents=True,exist_ok=True)
 for p in (src/'textures').glob('*.png'):shutil.copy2(p,imp/p.name)
 for p in (src/'cs2_import_candidates').glob('*.fbx'):shutil.copy2(p,imp/p.name)
 shutil.copy2(src/'settings.json',imp/'settings.json')
 for f in ['README.md','SOURCES.txt']:
  if (src/f).exists():shutil.copy2(src/f,dst/f)
 blend=next(src.glob('*.blend'));bpy.ops.wm.open_mainfile(filepath=str(blend),use_scripts=False);before=snap()
 for im in bpy.data.images:
  if im.source=='FILE':
   assert not im.packed_file
   imagepath=pathlib.Path(bpy.path.abspath(im.filepath));assert (imp/imagepath.name).exists()
   im.filepath='//../../import-assets/'+name+'/'+imagepath.name
 bpy.ops.wm.save_as_mainfile(filepath=str(dst/blend.name),relative_remap=False)
 bpy.ops.wm.open_mainfile(filepath=str(dst/blend.name),use_scripts=False);after=snap();assert before==after
 images=[]
 for im in bpy.data.images:
  if im.source=='FILE':
   p=pathlib.Path(bpy.path.abspath(im.filepath)).resolve();assert p.is_relative_to(O);assert p.exists();im.reload()
   images.append({'path':im.filepath,'size':list(im.size),'packed':bool(im.packed_file)})
 files=[{'name':p.name,'bytes':p.stat().st_size,'sha256':h(p),'source_sha256':h(src/'textures'/p.name)} for p in imp.glob('*.png')]
 out[name]={'before':before,'after':after,'images':images,'textures':files,'texture_bytes':sum(f['bytes'] for f in files),'baseline_all_bytes':sum(p.stat().st_size for p in src.rglob('*') if p.is_file()),'import_layer_bytes':sum(p.stat().st_size for p in imp.rglob('*') if p.is_file()),'source_layer_bytes':sum(p.stat().st_size for p in dst.rglob('*') if p.is_file())}
 (O/'verification.json').write_text(json.dumps(out,indent=2))

print('PREPARE_DONE')

METHODS = {
    ord("B"): "add_bool", ord("C"): "add_char", ord("Z"): "add_int8",
    ord("Y"): "add_int16", ord("I"): "add_int32", ord("L"): "add_int64",
    ord("F"): "add_float32", ord("D"): "add_float64", ord("R"): "add_bytes",
    ord("S"): "add_string", ord("i"): "add_int32_array",
    ord("l"): "add_int64_array", ord("f"): "add_float32_array",
    ord("d"): "add_float64_array", ord("b"): "add_bool_array",
    ord("c"): "add_byte_array",
}


def normalized_digest(root):
    """Hash all decoded nodes and typed properties, including version."""
    digest = hashlib.sha256()
    def visit(elem):
        digest.update(struct.pack("<I", len(elem.id)) + elem.id)
        digest.update(struct.pack("<I", len(elem.props)))
        for kind, value in zip(elem.props_type, elem.props):
            digest.update(bytes([kind]))
            if isinstance(value, array.array):
                blob = value.typecode.encode() + value.tobytes()
            elif isinstance(value, bytes):
                blob = value
            else:
                blob = repr(value).encode()
            digest.update(struct.pack("<Q", len(blob)) + blob)
        digest.update(struct.pack("<I", len(elem.elems)))
        for child in elem.elems:
            visit(child)
    visit(root)
    return digest.hexdigest()


D=O
rows=[]
for f in (O/'import-assets').rglob('*.fbx'):
 root,ver=parse_fbx.parse(str(f));changes=[]
 def fix(n):
  if n.id in [b'FileName',b'Filename',b'RelativeFilename']:
   for i,v in enumerate(n.props):
    new=v.replace(b'\\',b'/').split(b'/')[-1];assert (f.parent/new.decode()).is_file();changes.append([v.decode(),new.decode()]);n.props[i]=new
  for e in n.elems:fix(e)
 fix(root);expected=normalized_digest(root)
 def clone(n):
  a=encode_bin.FBXElem(n.id)
  for k,v in zip(n.props_type,n.props):getattr(a,METHODS[k])(v)
  a.elems=[clone(x) for x in n.elems];return a
 with encode_bin.FBXElem.enable_multithreading_cm():out=clone(root)
 encode_bin.write(str(f),out,ver);rt,v=parse_fbx.parse(str(f));assert normalized_digest(rt)==expected
 rows.append({'file':str(f.relative_to(O)),'only_path_changes':True,'version':ver,'normalized_tree_after_intended_path_change':expected,'changes':changes})
(O/'fbx_path_changes.json').write_text(json.dumps(rows,indent=2))
C.mkdir(parents=True)
for folder in ['source','import-assets']:shutil.copytree(O/folder,C/folder,dirs_exist_ok=True)
checked=[]
for f in (C/'import-assets').rglob('*.fbx'):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(f),use_image_search=False)
 images=[]
 for im in bpy.data.images:
  if im.source=='FILE':
   q=pathlib.Path(bpy.path.abspath(im.filepath)).resolve();assert q.is_relative_to(C) and q.is_file();im.reload();_=im.pixels[0];assert im.has_data;images.append(str(q.relative_to(C)))
 meshes=[]
 for ob in bpy.data.objects:
  if ob.type=='MESH':ob.data.calc_loop_triangles();meshes.append({'object':ob.name,'triangles':len(ob.data.loop_triangles)})
 checked.append({'file':str(f.relative_to(C)),'images_loaded':images,'meshes':meshes})
for f in (C/'source').rglob('*.blend'):
 bpy.ops.wm.open_mainfile(filepath=str(f),use_scripts=False)
 for im in bpy.data.images:
  if im.source=='FILE':
   q=pathlib.Path(bpy.path.abspath(im.filepath)).resolve();assert q.is_relative_to(C) and q.is_file();im.reload();_=im.pixels[0];assert im.has_data
(O/'clean_path_verification.json').write_text(json.dumps({'clean_copy':str(C),'use_image_search':False,'FBX':checked,'blend_images_decoded':True},indent=2));print('CLEAN_PASS',len(checked))

manifest={str(p.relative_to(O)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['source','import-assets'] for p in (O/folder).rglob('*') if p.is_file()}
(O/'manifest.json').write_text(json.dumps(manifest,indent=2))
source=json.loads((O/'verification.json').read_text());mismatches=[]
for row in checked:
 building=pathlib.Path(row['file']).parts[1]
 for mesh in row['meshes']:
  key=mesh['object'];lookup=source[building]['after'];expected=lookup.get(key,lookup.get(key+'_Base',{})).get('triangles')
  if expected!=mesh['triangles']:mismatches.append({'building':building,'object':key,'source_triangles':expected,'fbx_triangles':mesh['triangles'],'status':'KNOWN_OR_NEW_BLOCKER_REQUIRES_REVIEW_NOT_FIXED'})
(O/'source_to_fbx_count_differences.json').write_text(json.dumps(mismatches,indent=2))
print('MANIFEST_DONE',len(manifest),'COUNT_DIFFERENCES',len(mismatches))
