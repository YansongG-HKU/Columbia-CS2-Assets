from pathlib import Path
import zipfile, hashlib, json
D=Path(__file__).resolve().parent; T=D/'trial'; S=D/'input/import-assets/JohnJayHall'
extras=list(T.glob('*.blend')); assert len(extras)==1
files={p.name:p for p in T.iterdir() if p.suffix!='.blend'}
assert set(files)=={p.name for p in S.iterdir()}
same=sorted(n for n,f in files.items() if f.read_bytes()==(S/n).read_bytes())
assert len(same)==17 and set(files)-set(same)=={'NA_JohnJayHall_8x4_LOD1.fbx'}
manifest={n:hashlib.sha256(f.read_bytes()).hexdigest() for n,f in sorted(files.items())}
(D/'manifest.json').write_text(json.dumps({'sha256_import_files':manifest,'unchanged_17_files':same},indent=2)+'\n')
p=D/'John-Jay-Hall-CS2-offline-trial.zip'
with zipfile.ZipFile(p,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,f in sorted(files.items()):z.write(f,'import-assets/JohnJayHall/'+n)
 z.write(extras[0],'import-assets/JohnJayHall/'+extras[0].name)
 for n in ('README.md','manifest.json','repair-receipt.json','verify-receipt.json'):z.write(D/n,n)
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 z.extractall(D/'fresh')
 for n,h in manifest.items():
  assert hashlib.sha256((D/'fresh/import-assets/JohnJayHall'/n).read_bytes()).hexdigest()==h
print(p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
