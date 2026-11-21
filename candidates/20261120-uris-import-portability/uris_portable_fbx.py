"""Create a seven-FBX Uris import candidate from pinned originals and replayed layers."""
import argparse, hashlib, json, math, shutil, sys
from pathlib import Path
import bpy
from io_scene_fbx import parse_fbx, encode_bin
from mathutils import Vector

STEM = 'NA_UrisHall_6x9'
FILES = {
    '': ('64277811ac5bd5a4af42925b8e26d272e4301385073067841af1738fb569e817', 7210),
    '_LOD1': ('7e793663c01b6ff65eaec8db82a5f82f1fb5d78a4c426a4bc7eff09dd2ce9b36', 4762),
    '_LOD2': ('88201d18179231b86247107f8db91fa4b8a3442bf101e0f4e912226525452b02', 72),
    '_Gls': ('7e9beba1858dab084b12b440aecd050500e4e1d0f1c3e4efe93a28f42535a8b7', 72),
    '_LOD1_Gls': ('42683e7493353ad9565c6ea0a58006b3e97a833ec1dea507e5646c135900748c', 72),
    '_Win': ('10ec2bfd4635763acb1b3cf66bec3ff9c7281da0797cb48f08318164d4904168', 80),
    '_LOD1_Win': ('14ea7cfd32ffd6fba6dcf8359a998f0348b1e88d7ad647bcbf38a3a65bbe2672', 80),
}
MAPS = ('BaseColor','Normal','MaskMap','ControlMask','Emissive')
TEXTURE_SHA256 = {
    'NA_UrisHall_6x9_BaseColor.png': '1318f23f71c978865f214251e0254626f92a4d1d4df88cbcb87e9f31a425bb8d',
    'NA_UrisHall_6x9_ControlMask.png': 'd707d23a521009e707bbbae2f4a4443fcde9bb3d7144b87cb6e440083a82cd4e',
    'NA_UrisHall_6x9_Emissive.png': '96bb1126f74f49ec92c5045c4ce311c392a667bbbafb76aaa8f802e12b639d48',
    'NA_UrisHall_6x9_LOD2_BaseColor.png': '511b9ae93bc891aeb46d859402ec7cb78a7efc4ead553bd1a27d824cb9aa507b',
    'NA_UrisHall_6x9_LOD2_ControlMask.png': 'b2ac5efa78e7eb86571502c6bdbed28a4efab5354fd55f57340f024cfd07476e',
    'NA_UrisHall_6x9_LOD2_Emissive.png': 'f820a5330c556efcb3d0782e7c3822d1cafb0b2a805fbe14473d45b3ac2808b5',
    'NA_UrisHall_6x9_LOD2_MaskMap.png': 'c5da97a8cafa63314ffd3426589ebc63c0f8afaf777e6d3d5a83e0d52333ff49',
    'NA_UrisHall_6x9_LOD2_Normal.png': '710bc43f717cc15aa94c3d67021cf2831f79fc38cb1fd6e32b0c75e3483aa80f',
    'NA_UrisHall_6x9_MaskMap.png': '6eb31842d1dae7fc111a0ac320ee9cd12560cd4d3be818d32bdcc09f8b5bd511',
    'NA_UrisHall_6x9_Normal.png': '8308fad811e5d8c454c4e55cbf2c292f1b239d1433cacfb1617ac270bc21c01b',
}
PATH_FIELDS = {b'FileName',b'Filename',b'RelativeFilename'}
METHODS = dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32',
    'add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array',
    'add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))

def digest(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def nodes(n):
    yield n
    for c in n.elems: yield from nodes(c)

def clone(n):
    r = encode_bin.FBXElem(n.id)
    for t,p in zip(n.props_type,n.props): getattr(r,METHODS[t])(p)
    r.elems = [clone(c) for c in n.elems]
    return r

def projection(n):
    return (n.id,bytes(n.props_type),tuple(n.props),tuple(projection(c) for c in n.elems))

def expected_images(suffix):
    if suffix.endswith(('_Gls','_Win')): return set()
    prefix = STEM + ('_LOD2' if suffix == '_LOD2' else '')
    return {prefix+'_'+m+'.png' for m in ('BaseColor','Normal','Emissive')}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('original','replayed','textures','output','clean'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    orig,replayed,tex,out,clean=(getattr(a,name).resolve() for name in ('original','replayed','textures','output','clean'))
    if any(d.exists() or any(d.is_relative_to(q) for q in (orig,replayed,tex))
           for d in (out,clean)) or out.is_relative_to(clean) or clean.is_relative_to(out):
        raise ValueError('Two fresh, separate output directories are required')
    sources={}
    for suffix,(sha,count) in FILES.items():
        name=STEM+suffix+'.fbx'
        f=(replayed if suffix.endswith(('_Gls','_Win')) else orig/'fbx/split')/name
        if digest(f)!=sha:raise ValueError('Invalid input hash: '+name)
        sources[suffix]=f
    texnames={STEM+prefix+'_'+m+'.png' for prefix in ('','_LOD2') for m in MAPS}
    for name in texnames:
        if digest(tex/name) != TEXTURE_SHA256[name]: raise ValueError('Texture hash mismatch: '+name)
        with (tex/name).open('rb') as stream:
            if stream.read(8)!=b'\x89PNG\r\n\x1a\n':raise ValueError('Not a PNG: '+name)
    settings=orig/'settings.json'
    if json.loads(settings.read_text()) != {'sharedAssets':{STEM+'_LOD1_'+m+'.png':STEM+'_'+m+'.png' for m in MAPS}}:
        raise ValueError('Unexpected LOD1 sharing settings')
    out.mkdir()
    for name in sorted(texnames):shutil.copyfile(tex/name,out/name)
    shutil.copyfile(settings,out/'settings.json')
    changes={}
    for suffix,src in sources.items():
        root,version=parse_fbx.parse(str(src))
        target=out/src.name
        wanted=expected_images(suffix)
        absolute=0; found=set()
        for elem in nodes(root):
            if elem.id not in PATH_FIELDS:continue
            if len(elem.props)!=1 or not isinstance(elem.props[0],bytes):raise ValueError('Malformed FBX path property')
            old=elem.props[0]
            new=old.replace(b'\\',b'/').rsplit(b'/',1)[-1]
            if new.decode() not in wanted:raise ValueError('Unexpected FBX image path')
            found.add(new.decode())
            if old!=new:
                absolute+=1
                elem.props[0]=new
        if found!=wanted or absolute!=(6 if wanted else 0):raise ValueError('Unexpected path field or texture count')
        if absolute:
            with encode_bin.FBXElem.enable_multithreading_cm(): payload=clone(root)
            encode_bin.write(str(target),payload,version)
        else:shutil.copyfile(src,target)
        again,v=parse_fbx.parse(str(target))
        if v!=version or projection(root)!=projection(again):raise ValueError('Non-path FBX data changed')
        changes[suffix]={'old_absolute_fields_removed':absolute,'pre_sha256':digest(src),'final_sha256':digest(target)}
    shutil.copytree(out,clean)
    result={}
    for suffix,src in sources.items():
        final=clean/src.name
        if digest(final)!=changes[suffix]['final_sha256']:raise ValueError('Clean copy changed')
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.fbx(filepath=str(final),use_image_search=False)
        images={}
        for im in bpy.data.images:
            if im.source!='FILE':continue
            path=Path(bpy.path.abspath(im.filepath)).resolve()
            if path.parent!=clean or path.name not in expected_images(suffix):
                raise ValueError('Image did not load from clean package')
            im.reload(); _=im.pixels[0]
            if not im.has_data:raise ValueError('Image did not decode')
            images[path.name]=list(im.size)
        meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
        if len(meshes)!=1:raise ValueError('Unexpected number of meshes')
        o=meshes[0]; m=o.data; m.calc_loop_triangles()
        if len(m.loop_triangles)!=FILES[suffix][1] or set(images)!=expected_images(suffix) or not m.uv_layers.active:
            raise ValueError(f'Missing mesh, UV or image set: {final.name} (triangles={len(m.loop_triangles)}, images={list(images)})')
        bad=0; bad_uv=0
        uv=m.uv_layers.active.data
        for tri in m.loop_triangles:
            a,b,c=[o.matrix_world@m.vertices[i].co for i in tri.vertices]
            bad+=int((b-a).cross(c-a).length_squared<=1e-18 or not all(math.isfinite(x) for vec in (a,b,c) for x in vec))
            A,B,C=[Vector(uv[i].uv) for i in tri.loops]
            d=(B[0]-A[0])*(C[1]-A[1])-(B[1]-A[1])*(C[0]-A[0])
            bad_uv+=int(not math.isfinite(d) or abs(d)<=1e-10)
        if bad or (suffix.endswith('_Gls') and bad_uv):
            raise ValueError(f'Degenerate geometry or glass UV in {final.name}')
        result[src.name]={**changes[suffix],'object':o.name,'triangles':len(m.loop_triangles),'degenerate_mesh_triangles':bad,
                          'near_zero_uv_area_triangles':bad_uv,'images_decoded':images}
    manifest={f.name:digest(f) for f in sorted(out.iterdir())}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'offline-readback.json').write_text(json.dumps({'files':result,'manifest_entries':len(manifest),
        'scope':'Blender only. No overlap/shape modifications in base mesh; no game tests.'},indent=2)+'\n')
    print('URIS_PORTABLE_IMPORT_PASS',len(result),len(manifest))

if __name__=='__main__':main()
