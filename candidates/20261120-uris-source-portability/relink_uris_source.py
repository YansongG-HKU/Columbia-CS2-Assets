"""Relink only the eight assigned Uris bake maps; never overwrite the source."""
import argparse
from hashlib import file_digest, sha256
import json
from pathlib import Path
import sys
import bpy

STEM = 'NA_UrisHall_6x9'
SOURCE = '3bc48a79992641c1e42089d1dfec6b9b74e9bcd0777f2b07408bc587ab6148c3'
HASHES = {
    'BaseColor': '1318f23f71c978865f214251e0254626f92a4d1d4df88cbcb87e9f31a425bb8d',
    'Emissive': '96bb1126f74f49ec92c5045c4ce311c392a667bbbafb76aaa8f802e12b639d48',
    'MaskMap': '6eb31842d1dae7fc111a0ac320ee9cd12560cd4d3be818d32bdcc09f8b5bd511',
    'Normal': '8308fad811e5d8c454c4e55cbf2c292f1b239d1433cacfb1617ac270bc21c01b',
    'LOD2_BaseColor': '511b9ae93bc891aeb46d859402ec7cb78a7efc4ead553bd1a27d824cb9aa507b',
    'LOD2_Emissive': 'f820a5330c556efcb3d0782e7c3822d1cafb0b2a805fbe14473d45b3ac2808b5',
    'LOD2_MaskMap': 'c5da97a8cafa63314ffd3426589ebc63c0f8afaf777e6d3d5a83e0d52333ff49',
    'LOD2_Normal': '710bc43f717cc15aa94c3d67021cf2831f79fc38cb1fd6e32b0c75e3483aa80f',
}

def digest(path):
    with path.open('rb') as stream:
        return file_digest(stream, 'sha256').hexdigest()

def meshes():
    return sorted((o for o in bpy.data.objects if o.type == 'MESH'), key=lambda o: o.name)

def bindings():
    materials = {slot.material for o in meshes() for slot in o.material_slots if slot.material}
    return sorted((m.name, n.name, n.image.name)
                  for m in materials if m.use_nodes for n in m.node_tree.nodes
                  if n.type == 'TEX_IMAGE' and n.image and n.image.source == 'FILE')

def snapshot():
    data = []
    for o in meshes():
        m = o.data
        data.append([o.name, [list(row) for row in o.matrix_world], [list(v.co) for v in m.vertices],
                     [(list(p.vertices), p.material_index, p.use_smooth) for p in m.polygons],
                     [(layer.name, [list(l.uv) for l in layer.data]) for layer in m.uv_layers],
                     [slot.material.name if slot.material else None for slot in o.material_slots]])
    graphs = []
    for m in sorted((m for m in bpy.data.materials if m.use_nodes and m.users),key=lambda m:m.name):
        graphs.append((m.name, sorted((l.from_node.name, l.from_socket.identifier, l.to_node.name,
                      l.to_socket.identifier) for l in m.node_tree.links)))
    return sha256(json.dumps([data, graphs, bindings()], separators=(',', ':')).encode()).hexdigest()

def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--source', type=Path, required=True)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args(sys.argv[sys.argv.index('--')+1:])
    src, out = args.source.resolve(), args.output.resolve()
    if out.exists() or out.is_relative_to(src.parent) or digest(src) != SOURCE:
        raise ValueError('Source must be pinned and output directory must be fresh and separate')
    texture_dir = src.parent / 'textures'
    files = {f'{STEM}_{key}': texture_dir / f'{STEM}_{key}.png' for key in HASHES}
    for key, h in HASHES.items():
        if digest(files[f'{STEM}_{key}']) != h:
            raise ValueError('Texture hash mismatch: ' + key)
    bpy.ops.wm.open_mainfile(filepath=str(src), use_scripts=False)
    links = bindings()
    if len(links) != 12 or {im for _, _, im in links} != set(files):
        raise ValueError('Unexpected assigned file maps')
    before = snapshot()
    old_paths = {im.name: im.filepath for im in bpy.data.images if im.source == 'FILE'}
    for name in files:
        im = bpy.data.images[name]
        if im.packed_file or Path(im.filepath).name != files[name].name:
            raise ValueError('Unexpected original image binding')
        im.filepath = '//textures/' + files[name].name
    out.mkdir()
    (out / 'textures').mkdir()
    import shutil
    for f in files.values():
        shutil.copyfile(f, out / 'textures' / f.name)
    blend = out / src.name
    bpy.ops.wm.save_as_mainfile(filepath=str(blend), relative_remap=False)
    bpy.ops.wm.open_mainfile(filepath=str(blend), use_scripts=False)
    if snapshot() != before:
        raise ValueError('Geometry, UVs or material bindings changed')
    maps = []
    for im in (i for i in bpy.data.images if i.source == 'FILE'):
        if im.name in files:
            p = Path(bpy.path.abspath(im.filepath)).resolve()
            if p != out / 'textures' / files[im.name].name or digest(p) != digest(files[im.name]):
                raise ValueError('Reread image path/payload mismatch')
            im.reload()
            _ = im.pixels[0]
            if not im.has_data or len(im.pixels) == 0:
                raise ValueError('Assigned PNG did not decode: ' + im.name)
            expected_space = 'Non-Color' if im.name.endswith(('MaskMap','Normal')) else 'sRGB'
            if im.colorspace_settings.name != expected_space:
                raise ValueError('Unexpected image colour space')
            maps.append({'file':p.name,'dimensions':list(im.size),'colorspace':expected_space,'sha256':digest(p)})
        elif im.filepath != old_paths[im.name]:
            raise ValueError('Unassigned legacy path was altered')
    receipt = {'source_sha256':SOURCE,'candidate_blend_sha256':digest(blend),'unchanged_state_sha256':before,
               'mesh_objects':len(meshes()),'unchanged_bindings':links,'decoded_maps':sorted(maps,key=lambda m:m['file']),
               'unassigned_file_maps_preserved':sorted(set(old_paths)-set(files)),
               'scope':'editable-source portability only; no FBX geometry or game changes'}
    (out / 'readback.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('URIS_SOURCE_RELINK_PASS',len(maps),len(links),len(meshes()))

if __name__ == '__main__':
    main()
