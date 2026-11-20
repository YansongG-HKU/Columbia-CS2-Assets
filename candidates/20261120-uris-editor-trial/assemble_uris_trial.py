"""Deterministically assemble and verify a Uris Hall offline Editor trial."""
from pathlib import Path
import argparse,hashlib,json,shutil,zipfile
p=argparse.ArgumentParser(description=__doc__)
for k in ('portable','tangents','output','zip','extract'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args()
original,new,out,archive,extract=(getattr(a,k).resolve() for k in ('portable','tangents','output','zip','extract'))
for q in (out,archive,extract):
    if q.exists() or q.is_relative_to(original) or q.is_relative_to(new):raise ValueError('Use fresh destination')
if out.is_relative_to(extract) or extract.is_relative_to(out) or archive.is_relative_to(extract) or archive.is_relative_to(out):
    raise ValueError('Separate destinations')
def sha(b):return hashlib.sha256(b).hexdigest()
stem='NA_UrisHall_6x9'
models=('', '_LOD1','_LOD2','_Gls','_Win','_LOD1_Gls','_LOD1_Win')
maps=('BaseColor','Normal','MaskMap','ControlMask','Emissive')
pattern={stem+s+'.fbx' for s in models}|{f'{stem}{t}_{m}.png' for t in ('','_LOD2') for m in maps}|{'settings.json'}
manifest=json.loads((original/'manifest.json').read_text())
if set(manifest)!=pattern:raise ValueError('Unexpected portable inventory')
replace={'NA_UrisHall_6x9.fbx':'8130ab8a01159608512eacff9dd2031390f42cda01fa2415c7432217fdbe69e4',
         'NA_UrisHall_6x9_LOD1.fbx':'2629a324366f1133f3e3add41bebc1c6893477706871afebf59be91bd4ea9081'}
for q in (out,extract):q.mkdir()
contents=out/'UrisHall';contents.mkdir()
for f in sorted(pattern):
    payload=(original/f).read_bytes()
    if sha(payload)!=manifest[f]:raise ValueError('Portable file does not match manifest: '+f)
    if f in replace:
        payload=(new/f).read_bytes()
        if sha(payload)!=replace[f]:raise ValueError('Tangent candidate SHA mismatch: '+f)
        manifest[f]=replace[f]
    (contents/f).write_bytes(payload)
(out/'SHA256SUMS.txt').write_text(''.join(f'{manifest[k]}  UrisHall/{k}\n' for k in sorted(manifest)))
(out/'README.txt').write_text(
    'Uris Hall / Columbia University: offline technical trial, NOT ready for publication.\n'
    'Only UrisHall/ is the asset directory. The package combines three path-safe body FBXs, tested\n'
    'near/mid glass and window layers without preview shader overrides, 10 original PNGs and settings.\n'
    'Near and mid use a limited fix for two neutral-normal material swatches, not a full UV rebake.\n'
    'Outstanding: shell overlap and seams; residual UV/lighting; as-built registration; in-game Editor.\n'
    'Do not publish. If a compatible local cloud editor exists, import in a disposable project first.\n',
    encoding='utf-8')
names={f'UrisHall/{f}' for f in pattern}|{'README.txt','SHA256SUMS.txt'}
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name in sorted(names):
        info=zipfile.ZipInfo(name,(2026,11,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,(out/name).read_bytes(),compresslevel=6)
with zipfile.ZipFile(archive) as z:
    if len(z.namelist())!=len(names) or set(z.namelist())!=names or z.testzip() is not None:
        raise ValueError('Incomplete or damaged archive')
    for name in names:
        path=extract/name;path.parent.mkdir(parents=True,exist_ok=True)
        payload=z.read(name)
        if name.startswith('UrisHall/') and sha(payload)!=manifest[Path(name).name]:
            raise ValueError('Archive payload hash mismatch: '+name)
        path.write_bytes(payload)
report={'payload_files':len(pattern),'crc_and_manifest_ok':True,'bytes':archive.stat().st_size,'archive_sha256':sha(archive.read_bytes()),
        'input_portability_manifest_sha256':sha((original/'manifest.json').read_bytes()),'asset':manifest}
(out/'package-qa.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
