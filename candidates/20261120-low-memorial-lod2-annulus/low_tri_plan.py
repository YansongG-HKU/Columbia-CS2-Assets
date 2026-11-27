"""Plan a conforming, exact 8-to-24 annulus for Low Memorial's dome base."""
import collections,hashlib,json,math,sys,types
from pathlib import Path
mod=types.ModuleType('io_scene_fbx')
mod.__path__=['/usr/share/blender/scripts/addons_core/io_scene_fbx'];sys.modules[mod.__name__]=mod
from io_scene_fbx import parse_fbx
d=Path(__file__).parent
source=d/'NA_ColumbiaLowLibrary_13x10_LOD2.fbx'
def item(n,k):
 xs=[x for x in n.elems if x.id==k]
 if len(xs)!=1:raise ValueError(k)
 return xs[0]
def prop(n,k):return item(n,k).props[0]
def load(source):
 root,ver=parse_fbx.parse(str(source));g=item(item(root,b'Objects'),b'Geometry')
 v,b=[prop(g,k) for k in (b'Vertices',b'PolygonVertexIndex')]
 V=[tuple(v[i:i+3]) for i in range(0,len(v),3)]
 f=[]; F=[]
 for k in b:
  f.append(k if k>=0 else -1-k)
  if k<0:F.append(tuple(f));f=[]
 assert not f
 return g,V,F
def edges(F):
 E=collections.defaultdict(list)
 for i,f in enumerate(F):
  for x,y in zip(f,f[1:]+f[:1]):E[tuple(sorted((x,y)))].append((x,y,i))
 return E
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def area(p):return sum(cross(p[0],a,b) for a,b in zip(p[1:],p[2:]))/2
def inter(p,q):
 if area(q)<0:q=q[::-1]
 for a,b in zip(q,q[1:]+q[:1]):
  n=[]
  for x,y in zip(p[-1:]+p[:-1],p):
   u,v=cross(a,b,x),cross(a,b,y)
   if (u>=-1e-9)!=(v>=-1e-9):n.append(tuple(i+(j-i)*u/(u-v) for i,j in zip(x,y)))
   if v>=-1e-9:n.append(y)
  p=n
 return abs(area(p))
assert hashlib.sha256(source.read_bytes()).hexdigest()=='c0fa5c09cf99c442b0737f3ca00595fdc865f743672cda82bfcd875c9ab2df61'
g,V,F=load(source)
E=edges(F)
open_before={e for e,r in E.items() if len(r)==1};assert len(open_before)==8
outer=set(sum(map(list,open_before),[]));assert outer==set(range(260,268))
Y=V[260][1]; assert all(V[x][1]==Y for x in outer)
inner=set(range(268,292)); assert all(V[x][1]==Y for x in inner)
disks=[i for i,f in enumerate(F) if set(f)<=inner]
assert len(disks)==22
planar=[i for i,f in enumerate(F) if all(abs(V[j][1]-Y)<1e-8 for j in f)]
assert planar==disks
xy=lambda j:(V[j][0],V[j][2]+9)
angle=lambda j:math.atan2(xy(j)[1],xy(j)[0])%(2*math.pi)
oa,ia=map(lambda r:sorted(r,key=angle),(outer,inner))
A,B=[list(map(xy,r)) for r in (oa,ia)]
clear=min(cross(x,y,p)/math.dist(x,y) for x,y in zip(A,A[1:]+A[:1]) for p in B)
assert clear>0.5
disk_area=sum(area(list(map(xy,F[i]))) for i in disks);assert abs(disk_area-area(B))<1e-6
R=[]; o,i=oa[-1],ia[-1]
for j in sorted(outer|inner,key=angle):
 if j in outer:
  f=(o,j,i);o=j
 else:
  f=(o,j,i);i=j
 # The +Y side is clockwise in raw X/Z coordinates.
 p=list(map(xy,f))
 assert area(p)>1e-6
 R.append(f[::-1])
P=[list(map(xy,f)) for f in R]
actual=-sum(map(area,P)); assert abs(actual-area(A)+area(B))<1e-6
assert sum(inter(p,q) for k,p in enumerate(P) for q in P[k+1:])<1e-7
assert sum(inter(p,B) for p in P)<1e-7
new=[f for i,f in enumerate(F) if i not in disks]+R
assert all(len(e)==2 and e[0][:2]==e[1][:2][::-1] for e in edges(new).values())
# Any nonplanar source triangle can intersect this plane in a segment. Clip to the
# triangle interior and reject all unreconciled intersections with the annulus.
def hits(p,q,ring):
 lo,hi=0.,1.
 for a,b in zip(ring,ring[1:]+ring[:1]):
  x,z=cross(a,b,p)-1e-7,cross(a,b,q)-1e-7
  if x<0 and z<0:return False
  if x*z<0:
   t=x/(x-z)
   if x<0:lo=max(lo,t)
   else:hi=min(hi,t)
  if lo>hi:return False
 return True
for k,f in enumerate(F):
 if k in disks:continue
 v=[V[j] for j in f];dy=[p[1]-Y for p in v];ps=[]
 for a,b,z,w in zip(v,v[1:]+v[:1],dy,dy[1:]+dy[:1]):
  if abs(z)<1e-8:ps.append((a[0],a[2]+9))
  if z*w<0:
   t=z/(z-w);ps.append((a[0]+t*(b[0]-a[0]),a[2]+t*(b[2]-a[2])+9))
 assert not ps or not any(hits(ps[0],ps[-1],p[::-1]) for p in P),k
out=dict(baseline_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),coordinate_note='FBX vertical Y; Z center -9m',
  outer=oa,inner=ia,plane_m=Y,outer_area_m2=area(A),inner_area_m2=area(B),ring_area_m2=actual,
  min_clearance_inner_to_outer_m=clear,remove_downward_inside_disk_faces=disks,add_upward_annulus_triangles=R,
  source_triangles=len(F),proposed_triangles=len(new),proposed_oriented_manifold_edges=len(edges(new)))
(d/'low-annulus-plan.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
