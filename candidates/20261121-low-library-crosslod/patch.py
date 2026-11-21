"""Apply survey-supported annular dome profile to pinned Low Library LOD0/LOD1. Keep lantern and lower toe untouched."""
import collections,hashlib,json,math,sys
from pathlib import Path
from io_scene_fbx import parse_fbx,encode_bin
from mathutils import Vector
src,dst,planfile,receipt=map(Path,sys.argv[sys.argv.index('--')+1:])
expect={'NA_ColumbiaLowLibrary_13x10.fbx':('2851492061a31f1e9bfcbde89e0d49ea1ce0fbd48f409cefb7ee5e3fff8b1f4c',108415,57901),'NA_ColumbiaLowLibrary_13x10_LOD1.fbx':('6652da3ce5725f773d16eeb6d6ef8bd9267733eb458252cf22b16164a845ae23',50407,27512)}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected,ntr,nvert=expect[src.name];assert sha(src)==expected and not dst.exists()
def item(n,k):
 a=[c for c in n.elems if c.id==k]; assert len(a)==1,(k,len(a));return a[0]
def p(n,k):return item(n,k).props[0]
def clone(n):
 m=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32','add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
 r=encode_bin.FBXElem(n.id)
 for t,a in zip(n.props_type,n.props):getattr(r,m[t])(a)
 r.elems=[clone(c) for c in n.elems];return r
def value(n):return (n.id,bytes(n.props_type),tuple(tuple(x) if hasattr(x,'typecode') else x for x in n.props),tuple(value(c) for c in n.elems))
def geo(root):return item(item(root,b'Objects'),b'Geometry')
root,ver=parse_fbx.parse(str(src));g=geo(root);assert ver==7400
vs=p(g,b'Vertices'); dims=list(vs); raw=p(g,b'PolygonVertexIndex'); ii=[i if i>=0 else -1-i for i in raw]; assert len(ii)==3*ntr and len(vs)==3*nvert
P=json.loads(planfile.read_text()); a={}
bands={float(i['old_height_m']):i for i in P['rings']}
n_hit=collections.Counter()
for i in range(len(vs)//3):
 x,y,z=vs[i*3:i*3+3]; rr=math.hypot(x,z+9); b=bands.get(round(y,4))
 if b:
  assert abs(rr-b['radius_m'])<.10,(x,y,z,rr)
  n_hit[round(y,4)]+=1
  a[i]=b['rise_m']; assert 0.<a[i]<1.0
  vs[i*3+1]+=a[i]
assert len(a)==96*len(bands) and set(n_hit.values())=={96},n_hit
N=item(g,b'LayerElementNormal'); ni=p(N,b'NormalsIndex'); nn=p(N,b'Normals')
TN=p(item(g,b'LayerElementTangent'),b'Tangents'); BN=p(item(g,b'LayerElementBinormal'),b'Binormals')
assert len(ni)==len(ii) and len(TN)==len(BN)==len(ii)*3
ng={}; basis_move=[]; mod_faces=0; non_unit_before=0; non_ortho_before=0
def put(ar,j,w):ar[j*3:(j+1)*3]=type(ar)(ar.typecode,tuple(w))
old_ni=list(ni);old_nn=list(nn)
for j in range(0,len(ii),3):
 face=ii[j:j+3]; d=[a.get(i,0.) for i in face]
 if not any(d):continue
 mod_faces+=1
 # The two station changes are a vertical affine shear on each triangle's XY domain.
 A,B,C=[Vector((dims[i*3],dims[i*3+2])) for i in face]
 u=B-A; v=C-A; det=u.x*v.y-u.y*v.x; assert abs(det)>1.e-5
 dx=((d[1]-d[0])*v.y-(d[2]-d[0])*u.y)/det
 dz=(u.x*(d[2]-d[0])-v.x*(d[1]-d[0]))/det
 for k in range(j,j+3):
  n=Vector(old_nn[3*ni[k]:3*ni[k]+3]); t=Vector(TN[3*k:3*k+3]); b=Vector(BN[3*k:3*k+3])
  ori=n.cross(t).dot(b); assert abs(ori)>.35
  non_unit_before+=int(max(abs(v.length-1) for v in (n,t,b))>1e-4)
  non_ortho_before+=int(max(abs(n.dot(t)),abs(n.dot(b)),abs(b.dot(t)))>1e-4)
  m=Vector((n.x-dx*n.y,n.y,n.z-dz*n.y)).normalized()
  nt=Vector((t.x,t.y+dx*t.x+dz*t.z,t.z)); nt=(nt-m*m.dot(nt)).normalized()
  nb=m.cross(nt)*(1 if ori>0 else -1)
  assert abs(m.dot(nt))<2e-7 and min(m.length,nt.length,nb.length)>.99999 and m.cross(nt).dot(nb)*ori>0.
  basis_move.append(math.degrees(n.normalized().angle(m)))
  key=tuple(round(x,8) for x in m)
  if key not in ng:ng[key]=len(nn)//3;nn.extend(m)
  ni[k]=ng[key]; put(TN,k,nt);put(BN,k,nb)
assert max(basis_move)<40
with encode_bin.FBXElem.enable_multithreading_cm(): payload=clone(root)
encode_bin.write(str(dst),payload,ver)
actual,v2=parse_fbx.parse(str(dst)); assert v2==ver and value(actual)==value(root)
# Restore all and only the revised arrays in memory; exact source equality proves no accidental changes.
baseline,_=parse_fbx.parse(str(src)); bg=geo(baseline)
for u,v in [(vs,p(bg,b'Vertices')),(nn,p(item(bg,b'LayerElementNormal'),b'Normals')),(ni,p(item(bg,b'LayerElementNormal'),b'NormalsIndex')),
 (TN,p(item(bg,b'LayerElementTangent'),b'Tangents')),(BN,p(item(bg,b'LayerElementBinormal'),b'Binormals'))]:
 u[:]=v
assert value(root)==value(baseline)
receipt.write_text(json.dumps({'before':sha(src),'after':sha(dst),'triangles':len(ii)//3,'moved_crown_vertices':len(a),'affected_dome_faces':mod_faces,'corrected_corners':mod_faces*3,'ring_movements':P['rings'],'max_corner_normal_rotation_deg':max(basis_move),'old_affected_nonunit_frames':non_unit_before,'old_affected_nonorthogonal_frames':non_ortho_before,'uv_topology_resource_nodes_exactly_unchanged':True},indent=2)+'\n')
