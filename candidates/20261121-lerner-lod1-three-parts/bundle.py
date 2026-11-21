from pathlib import Path
import zipfile, hashlib, json
D=Path(__file__).resolve().parent; T=D/'trial'; S=D/'input/import-assets/LernerHall'
extras=list(T.glob('*.blend')); assert len(extras)==1
files={p.name:p for p in T.iterdir() if p.suffix!='.blend'}
import sys
sys.path.insert(0,str(D.parent/'cs2-portable-audit'))
from scan import scan,parse_fbx
excluded={p.name:p for p in S.glob('*_Gls.fbx')}
assert set(excluded)=={'NA_LernerHall_9x9_Gls.fbx','NA_LernerHall_9x9_LOD1_Gls.fbx'}
assert all(scan(p)==[{'triangles':0}] for p in excluded.values())
for path in excluded.values():
 root,_=parse_fbx.parse(str(path))
 g,=[v for e in root.elems if e.id==b'Objects' for v in e.elems if v.id==b'Geometry']
 assert len(next(n.props[0] for n in g.elems if n.id==b'Vertices'))==0
assert set(files)|set(excluded)=={p.name for p in S.iterdir()} and set(files).isdisjoint(excluded)
same=sorted(n for n,f in files.items() if f.read_bytes()==(S/n).read_bytes())
assert len(same)==15 and set(files)-set(same)=={'NA_LernerHall_9x9_LOD1.fbx'}
manifest={n:hashlib.sha256(f.read_bytes()).hexdigest() for n,f in sorted(files.items())}
(D/'manifest.json').write_text(json.dumps({'sha256_import_files':manifest,'unchanged_15_files':same,'omitted_only_from_trial_due_to_empty_geometry':{n:hashlib.sha256(f.read_bytes()).hexdigest() for n,f in excluded.items()}},indent=2)+'\n')
p=D/'Lerner-Hall-CS2-offline-trial.zip'
with zipfile.ZipFile(p,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,f in sorted(files.items()):z.write(f,'import-assets/LernerHall/'+n)
 z.write(extras[0],'import-assets/LernerHall/'+extras[0].name)
 for n in ('README.md','manifest.json','repair-receipt.json','contacts.json'):z.write(D/n,n)
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 z.extractall(D/'fresh')
 for n,h in manifest.items():
  assert hashlib.sha256((D/'fresh/import-assets/LernerHall'/n).read_bytes()).hexdigest()==h
print(p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
