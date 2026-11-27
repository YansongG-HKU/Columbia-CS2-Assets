import collections,hashlib,math,sys,types
from pathlib import Path
# Import Blender's binary reader without starting Blender.
mod=types.ModuleType("io_scene_fbx")
mod.__path__=["/usr/share/blender/scripts/addons_core/io_scene_fbx"]
sys.modules["io_scene_fbx"]=mod
from io_scene_fbx import parse_fbx
def els(n,k):return [x for x in n.elems if x.id==k]
for f in map(Path,sys.argv[1:]):
 r,_=parse_fbx.parse(str(f)); print(f.name,hashlib.sha256(f.read_bytes()).hexdigest())
 for g in els(els(r,b'Objects')[0],b'Geometry'):
  a,b=[els(g,k)[0].props[0] for k in (b'Vertices',b'PolygonVertexIndex')]
  xyz=[tuple(a[i:i+3]) for i in range(0,len(a),3)]
  face=[]; bands=collections.defaultdict(list)
  for k in b:
   face.append(k if k>=0 else -1-k)
   if k>=0:continue
   p=[xyz[j] for j in face];face=[]
   y0,y1=min(t[1] for t in p),max(t[1] for t in p)
   if y0<27 or y1>37 or y1-y0>1e-5:continue
   if max(abs(t[0]) for t in p)>24 or min(t[2] for t in p)<-32 or max(t[2] for t in p)>14:continue
   cross=sum(u[0]*v[2]-u[2]*v[0] for u,v in zip(p,p[1:]+p[:1]))/2
   if abs(cross)>1e-8:bands[round(y0,5),cross<0].append((abs(cross),p))
  for (y,up),rows in sorted(bands.items()):
   area=sum(a for a,_ in rows);points=[u for _,p in rows for u in p]
   print(y,up,len(rows),round(area,3),[(round(min(t[i] for t in points),3),round(max(t[i] for t in points),3)) for i in (0,2)])
