"""Replay the pinned Low Memorial Library mesh and atlas ROI in a fresh folder."""
import hashlib,json,sys,zipfile
from pathlib import Path
from PIL import Image
import zstandard
p=Path(__file__).resolve().parent
orig,out=map(Path,sys.argv[1:])
m=json.loads((p/'manifest.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(got,wanted,where):
 if got!=wanted:raise ValueError(f'{where}: expected {wanted}, received {got}')
assert not out.exists()
out.mkdir(parents=True)
r=m['fbx']; b=(orig/r['input']).read_bytes()
require(sha(b),r['input_sha256'],r['input'])
parts=[(p/t['file']).read_bytes() for t in r['patch']]
for part,t in zip(parts,r['patch']):require(sha(part),t['sha256'],t['file'])
o=zstandard.ZstdDecompressor(dict_data=zstandard.ZstdCompressionDict(b,dict_type=zstandard.DICT_TYPE_RAWCONTENT)).decompress(b''.join(parts),max_output_size=r['bytes'])
require(len(o),r['bytes'],r['output']);require(sha(o),r['output_sha256'],r['output'])
(out/r['output']).write_bytes(o)
box=tuple(m['box'])
with zipfile.ZipFile(p/'roi.zip') as z:
 require(sha((p/'roi.zip').read_bytes()),m['tile_archive_sha256'],'roi.zip')
 for row in m['textures']:
  base=(orig/row['input']); inp=base.read_bytes(); require(sha(inp),row['input_sha256'],row['input'])
  source=Image.open(base); image=source.convert('RGBA')
  if row['tile']:
   w,h=box[2]-box[0],box[3]-box[1]
   raw=z.read(row['tile']);require(len(raw),w*h*4,row['tile']);require(sha(raw),row['tile_sha256'],row['tile'])
   image.paste(Image.frombytes('RGBA',(w,h),raw),box=box)
   img=out/row['output']
   image.save(img,optimize=False,**{k:v for k,v in source.info.items() if k in ('exif','dpi','icc_profile')})
  else:
   img=out/row['output'];img.write_bytes(inp)
  reread=Image.open(img).convert('RGBA')
  require(sha(reread.tobytes()),row['output_rgba_sha256'],row['output'])
  print(row['output'],sha(img.read_bytes()))
