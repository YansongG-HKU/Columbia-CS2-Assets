"""Restore eight source-supported solid ornaments while preserving the rest of the FBX."""
import sys,hashlib,json,collections
from pathlib import Path
from io_scene_fbx import parse_fbx,encode_bin
p,o,j,out=map(Path,sys.argv[sys.argv.index('--')+1:])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads(j.read_text());assert sha(p)==plan['old_sha256'] and not o.exists()
def one(n,k):
 a=[x for x in n.elems if x.id==k]; assert len(a)==1,(k,len(a));return a[0]
def prop(n,k):return one(n,k).props[0]
root,version=parse_fbx.parse(str(p));assert version==7500
g=one(one(root,b'Objects'),b'Geometry')
categories={b'Properties70',b'GeometryVersion',b'Vertices',b'PolygonVertexIndex',b'Edges',b'LayerElementNormal',b'LayerElementUV',b'LayerElementMaterial',b'Layer'}
assert {n.id for n in g.elems}==categories
rawv,rawf,edges=[prop(g,k) for k in (b'Vertices',b'PolygonVertexIndex',b'Edges')]
oldv=[tuple(rawv[i:i+3]) for i in range(0,len(rawv),3)]
assert all((n<0)==(i%3==2) for i,n in enumerate(rawf))
oldf=[tuple(v if v>=0 else -1-v for v in rawf[i:i+3]) for i in range(0,len(rawf),3)]
NM=one(g,b'LayerElementNormal'); UV=one(g,b'LayerElementUV')
N,I=prop(NM,b'Normals'),prop(NM,b'NormalsIndex')
U,J=prop(UV,b'UV'),prop(UV,b'UVIndex')
assert prop(NM,b'MappingInformationType')==prop(UV,b'MappingInformationType')==b'ByPolygonVertex'
assert prop(NM,b'ReferenceInformationType')==prop(UV,b'ReferenceInformationType')==b'IndexToDirect'
assert prop(one(g,b'LayerElementMaterial'),b'MappingInformationType')==b'AllSame'
drop_f={i for t in plan['components'] for i in t['old_face_pair']}
drop_v={i for t in plan['components'] for i in t['old_vertex_ids']}
assert len(drop_f)==100 and len(drop_v)==150 and all((i in drop_f)==bool(set(f)&drop_v) for i,f in enumerate(oldf))
d=collections.defaultdict(list)
for i,f in enumerate(oldf):d[tuple(sorted(f))].append(i)
assert {i for a in d.values() if len(a)>1 for i in a}==drop_f
newv=[x for i,x in enumerate(oldv) if i not in drop_v]
original_count=len(newv)
mapping={r:n for n,r in enumerate(i for i in range(len(oldv)) if i not in drop_v)}
newf=[]; a=[];b=[]
for i,f in enumerate(oldf):
 if i not in drop_f:
  newf.append(tuple(mapping[q] for q in f))
  a.extend(I[3*i:3*i+3]);b.extend(J[3*i:3*i+3])
keep_count=len(newf)
nv=list(N); uv=list(U)
for r in plan['components']:
 off=len(newv)
 newv.extend(r['donor_raw_vertices'])
 for face,n,u in zip(r['donor_triangles'],r['donor_normals_corners'],r['donor_uv_corners']):
  newf.append(tuple(k+off for k in face))
  for ni,ui in zip(n,u):
   a.append(len(nv)//3);nv.extend(ni)
   b.append(len(uv)//2);uv.extend(ui)
assert len(newf)==37258 and len(newv)==24561 and len(a)==len(b)==3*len(newf)
assert len({tuple(sorted(x)) for x in newf})==len(newf)
assert len({i for f in newf for i in f})==len(newv)
assert all(tuple(newv[mapping[i]])==oldv[i] for i in mapping)
new_edges={}
for i,f in enumerate(newf):
 for j,(a0,b0) in enumerate(zip(f,f[1:]+f[:1])):
  new_edges.setdefault((min(a0,b0),max(a0,b0)),3*i+j)
pfx=lambda dt,v: dt.__setitem__(slice(None),type(dt)(dt.typecode,v))
pfx(rawv,(n for v in newv for n in v));pfx(rawf,(x if j<2 else -1-x for f in newf for j,x in enumerate(f)))
pfx(edges,new_edges.values());pfx(N,nv);pfx(I,a);pfx(U,uv);pfx(J,b)
methods=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32','add_int64',
 'add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
def clone(x):
 n=encode_bin.FBXElem(x.id)
 for t,v in zip(x.props_type,x.props):getattr(n,methods[t])(v)
 n.elems=[clone(y) for y in x.elems];return n
def as_value(x):return(x.id,bytes(x.props_type),tuple(x.props),tuple(as_value(y) for y in x.elems))
with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(root)
encode_bin.write(str(o),payload,version)
rt,v2=parse_fbx.parse(str(o)); assert v2==7500 and as_value(rt)==as_value(root)
oldtree,_=parse_fbx.parse(str(p))
oldg=one(one(oldtree,b'Objects'),b'Geometry')
for n,k,h in [(g,b'Vertices',oldg),(g,b'PolygonVertexIndex',oldg),(g,b'Edges',oldg),(NM,b'Normals',one(oldg,b'LayerElementNormal')),
 (NM,b'NormalsIndex',one(oldg,b'LayerElementNormal')),(UV,b'UV',one(oldg,b'LayerElementUV')),(UV,b'UVIndex',one(oldg,b'LayerElementUV'))]:
  pfx(prop(n,k),prop(h,k))
assert as_value(oldtree)==as_value(root)
report={'source_fbx_7500_sha256':sha(p),'candidate_fbx_7500_sha256':sha(o),'old_raw_triangles':len(oldf),'removed_reversed_pairs':50,'removed_old_triangles':len(drop_f),
 'copied_donor_triangles':664,'candidate_triangles':len(newf),'outer_geometric_unchanged_faces':keep_count,'external_texture_and_unchanged_arrays':True,'restored_donor_vertices':432}
out.write_text(json.dumps(report,indent=2)+'\n')
print(report)
