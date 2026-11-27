"""Remove only two proved internal common rings from the exact intermediate Uris candidate."""
from probe import one,val,read
from io_scene_fbx import parse_fbx,encode_bin
from pathlib import Path
from collections import defaultdict,Counter
import json,hashlib,math
D=Path(__file__).resolve().parent;BASE=D.parent/'cs2-uris-local'/'out'
PLAN=[('','cdfd0bb82d29e52125be32f81969bd9948524538bd794e347b9234cca712b873',[[372,3932],[378,3938]]),
      ('_LOD1','44018db0d7b73d3a13e8d60f177c7e3a8761bd9611a417e74087c88c21ef3e61',[[264,2600],[270,2606]])]
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def edges(f):return list(zip(f,f[1:]+f[:1]))
def ek(a,b):return min(a,b),max(a,b)
def topo(F):
 c=defaultdict(list)
 for i,row in enumerate(F):
  for a,b in edges(row):c[ek(a,b)].append((i,a,b))
 return c
def hist(a):return dict(Counter(len(x) for x in a.values()))
def repair(lod,h,stripes):
 p=BASE/f'NA_UrisHall_6x9{lod}.fbx'; assert H(p)==h
 r,version,g,v,f=read(p)
 assert version==7400 and all(len(row)==3 for row in f)
 assert {x.id for x in g.elems}=={b'Properties70',b'GeometryVersion',b'Vertices',b'PolygonVertexIndex',b'Edges',b'LayerElementSmoothing',b'LayerElementNormal',b'LayerElementBinormal',b'LayerElementTangent',b'LayerElementUV',b'LayerElementMaterial',b'Layer'}
 source=topo(f);S=set(i for a in stripes for i in a);assert len(S)==4
 ordered=[i for i in range(len(f)) if i not in S];F=[f[i] for i in ordered];result=topo(F)
 re={i:j for j,i in enumerate(ordered)}
 report=[]
 for stripe,heights in zip(stripes,[(.6,1.05),(3.75,4.65)]):
  ring={a for i in stripe for a in f[i]};assert len(ring)==4
  assert {tuple(round(q,5) for q in v[i]) for i in ring}=={(x,z,-24.4) for x in [23.6,23.74] for z in heights}
  border={k for k,l in topo([f[i] for i in stripe]).items() if len(l)==1};assert len(border)==4
  for k in border:
   c=source[k];l=result[k];assert len(c)==3 and len(l)==2 and l[0][1:]==l[1][1:][::-1]
   x,y=[f[ordered[i]] for i,a,b in l]; a,=set(x)-set(k);b,=set(y)-set(k)
   assert (v[a][2]+24.4)*(v[b][2]+24.4)<0 and all(abs(v[j][2]+24.4)>9 for j in (a,b))
  # Identify all faces of the two joined prisms, including both far end caps. The two side regions
  # are not inferred from the facing cap normals alone; they must have a closed oriented union.
  subset=[]
  for i,face in enumerate(f):
   if all(round(v[q][0],5) in (23.6,23.74) and round(v[q][1],5) in heights and round(v[q][2],5) in (-33.95,-24.4,24.1) for q in face):subset.append(i)
  assert len(subset)==22 and set(stripe)<set(subset),len(subset)
  keep=[j for j in subset if j not in S]; uni=topo([f[j] for j in keep])
  assert len(uni)==30 and all(len(l)==2 and l[0][1:]==l[1][1:][::-1] for l in uni.values())
  lo=[j for j in keep if min(v[q][2] for q in f[j])<-33.]
  hi=[j for j in keep if max(v[q][2] for q in f[j])>23.]
  assert len(lo)==len(hi)==10
  for a in (lo,hi):
   b=topo([f[i] for i in a]);assert {k for k,l in b.items() if len(l)==1}==border
  report.append(dict(source_internal_faces=stripe,source_union_faces=subset,two_half_shells=[lo,hi],world_z_nominal=heights,world_y_nominal_contact=24.4,
    nominal_area_m2=.14*(heights[1]-heights[0]),after_oriented_closed_union_triangle_edges=30))
 assert all(len(q)>1 for q in source.values()) and all(len(q)>1 for q in result.values())
 assert hist(result)=={2:hist(source)[2]+6,4:hist(source)[4]}
 # Any orientation/ownership outside the exact removed face perimeter is unchanged.
 s0={k:l for k,l in topo([f[i] for i in sorted(S)]).items()}
 assert all([(re[i],a,b) for i,a,b in l]==result[k] for k,l in source.items() if k not in s0)
 assert {i for a in F for i in a}=={i for a in f for i in a}
 o=set();ee=[]
 for i,face in enumerate(F):
  for j,(u,w) in enumerate(edges(face)):
   k=ek(u,w)
   if k not in o:o.add(k);ee.append(3*i+j)
 Q={k:one(g,b'LayerElement'+k) for k in (b'UV',b'Normal',b'Binormal',b'Tangent',b'Material',b'Smoothing')}
 lay=[(b'Smoothing',b'Smoothing',1,ordered),(b'UV',b'UVIndex',1,None),(b'Normal',b'NormalsIndex',1,None),(b'Binormal',b'Binormals',3,None),(b'Tangent',b'Tangents',3,None)]
 for k in Q:
  ll=Q[k]
  m=val(ll,b'MappingInformationType'); ref=val(ll,b'ReferenceInformationType')
  assert (m,ref)==((b'ByPolygon',b'Direct') if k==b'Smoothing' else (b'AllSame',b'IndexToDirect') if k==b'Material' else (b'ByPolygonVertex',b'Direct' if k in (b'Binormal',b'Tangent') else b'IndexToDirect'))
 C=[(val(g,b'PolygonVertexIndex'),[i if j<2 else -i-1 for a in F for j,i in enumerate(a)]),(val(g,b'Edges'),ee)]
 loops=[i*3+j for i in ordered for j in range(3)]
 for k,n,m,kept in lay:
  a=val(Q[k],n); assert len(a)==m*(len(f) if kept else 3*len(f))
  C.append((a,[x for i in (kept or loops) for x in a[m*i:m*(i+1)]]))
 def assign(a,b):a[:]=type(a)(a.typecode,b)
 B=[list(a) for a,b in C]
 for a,b in C:assign(a,b)
 methods=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32','add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
 def clone(x):
  e=encode_bin.FBXElem(x.id)
  for k,v in zip(x.props_type,x.props):getattr(e,methods[k])(v)
  e.elems=[clone(j) for j in x.elems];return e
 def sig(x):return(x.id,bytes(x.props_type),tuple(x.props),tuple(sig(y) for y in x.elems))
 dest=D/'out'/p.name;dest.parent.mkdir(exist_ok=True)
 with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(r)
 encode_bin.write(str(dest),payload,version)
 q,n=parse_fbx.parse(str(dest));assert n==version and sig(q)==sig(r)
 for (a,b),c in zip(C,B):assign(a,c)
 assert sig(r)==sig(parse_fbx.parse(str(p))[0])
 return dict(intermediate_sha256=h,candidate_sha256=H(dest),source_triangles=len(f),candidate_triangles=len(F),source_edges=hist(source),candidate_edges=hist(result),seams=report,
  disabled_static_surface_normals=False,unedited_uv_normals_tangent_bitangent_faces=len(F))
if __name__=='__main__':
 d={p[0] or 'LOD0':repair(*p) for p in PLAN}
 (D/'raw.json').write_text(json.dumps(d,indent=2)+'\n')
