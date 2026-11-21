from prep import *
from geos import tris2
from mesh import clean_surfaces
def build_shell(roof_replacement,z0,out):
 surfaces=[]
 for r in groups['RoofSurface']:
  assert np.ptp(r[:,2])<1e-6 and flat(r[:,:2])>0
  z=roof_replacement.get(float(r[0,2]),r[0,2])
  surfaces.append(('roof',*[np.c_[p,np.full(3,z)] for p in tris2(poly(r))]))
 assert flat(g[:,:2])<0
 surfaces.append(('floor',*[np.c_[p[::-1],np.full(3,g[0,2])] for p in tris2(gp)]))
 for r in groups['WallSurface']:
  v=r[np.argmax(np.linalg.norm(r[:,:2]-r[:1,:2],axis=1)),:2]-r[0,:2]
  v/=np.linalg.norm(v)
  q=np.round(np.c_[(r[:,:2]-r[:1,:2])@v,r[:,2]-r[0,2]],6)
  sign=np.sign(flat(q))
  assert poly(q).IsValid() and sign!=0
  td=[]
  for t in tris2(poly(q)):
   if sign<0:t=t[::-1]
   d=np.linalg.norm(t[:,None,:]-q[None,:,:],axis=-1)
   assert (d.min(axis=1)<2e-5).all()
   r0=r[np.argmin(d,axis=1)].copy()
   for i,p in enumerate(r0):r0[i,2]=roof_replacement.get(float(p[2]),p[2])
   td.append(r0)
  surfaces.append(('wall',*td))
 V,F,T=clean_surfaces(surfaces)
 edges=collections.defaultdict(list)
 for j,f in enumerate(F):
  for a,b in zip(f,f[1:]+f[:1]):edges[tuple(sorted((a,b)))].append((a,b,j))
 bad=[(V[list(k)].tolist(),v) for k,v in edges.items() if len(v)!=2 or v[0][:2]!=v[-1][:2][::-1]]
 print('vertices, triangles, edge count, bad:',len(V),len(F),len(edges),len(bad),bad[:5])
 assert not bad
 V[:,2]-=z0
 P=V[np.array(F)]
 signed=float((P[:,0]*np.cross(P[:,1],P[:,2])).sum()/6); assert signed>1
 assert (np.linalg.norm(np.cross(P[:,1]-P[:,0],P[:,2]-P[:,0]),axis=1)>1e-8).all()
 out.write_text('# Alfred Lerner Hall measuring shell, not game FBX; X Broadway to campus, Y north, Z metres.\n'
  '# CityGML OTI BIN 1082166 / DOITT_ID 397140; no entrance, glass, interior, or true below-grade claim.\n'
  'o Lerner_Survey_Massing\n'+''.join('v %.5f %.5f %.5f\n'%tuple(p) for p in V)+
  ''.join('f %d %d %d\n'%tuple(x+1 for x in p) for p in F))
 return dict(vertices=len(V),triangles=len(F),manifold_oriented_edges=len(edges),signed_volume_m3=signed,xyz_bounds_m=[V.min(axis=0).tolist(),V.max(axis=0).tolist()],z_zero_provisional_m=z0,sha256=hashlib.sha256(out.read_bytes()).hexdigest())
if __name__=='__main__':
 dest=D/'deliver';dest.mkdir(exist_ok=True)
 print(build_shell({},0,dest/'lerner-2014-city-shell.obj'))
