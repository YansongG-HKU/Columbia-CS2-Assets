"""Repair only the hash-pinned complete nested post region from Uris Hall near/mid."""
from probe import one,val,read
from io_scene_fbx import parse_fbx,encode_bin
from pathlib import Path
import hashlib,sys,collections,json,math
D=Path(__file__).resolve().parent
BASE=Path('/tmp/cs2-lowram.LpRNPF/uris-trial-fresh/UrisHall')
ORIG=Path('/tmp/cs2-lowram.LpRNPF/uris-import-original/UrisHall/fbx/split')
PLAN=[('', '8130ab8a01159608512eacff9dd2031390f42cda01fa2415c7432217fdbe69e4',[1222,1223,1224,1225,1226,4787,4788,4789,4790,4791],
 [582,583,584,585,586,587,4147,4148,4149,4150,4151,4152],64277811),
 ('_LOD1','2629a324366f1133f3e3add41bebc1c6893477706871afebf59be91bd4ea9081',[490,491,492,493,494,2831,2832,2833,2834,2835],
 [288,289,290,291,292,293,2629,2630,2631,2632,2633,2634],7)]
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def edges(f):return zip(f,f[1:]+f[:1])
def transpose(q,n):return list(zip(*[iter(q)]*n))
def topo(F):
 c=collections.defaultdict(list)
 for i,row in enumerate(F):
  for a,b in edges(row):c[min(a,b),max(a,b)].append((a,b))
 return c
def hist(E):return dict(collections.Counter(map(len,E.values())))
def repair(tag,h,S,L,old_prefix):
 p=BASE/f'NA_UrisHall_6x9{tag}.fbx'; and_old=ORIG/p.name
 assert H(p)==h and H(and_old).startswith(str(old_prefix))
 r,version,g,v,f=read(p)
 _,_,_,v0,f0=read(and_old);assert v==v0 and f==f0
 assert version==7400 and all(len(row)==3 for row in f)
 assert {x.id for x in g.elems}=={b'Properties70',b'GeometryVersion',b'Vertices',b'PolygonVertexIndex',b'Edges',b'LayerElementSmoothing',b'LayerElementNormal',b'LayerElementBinormal',b'LayerElementTangent',b'LayerElementUV',b'LayerElementMaterial',b'Layer'}
 L=set(L);S=set(S); assert not S&L
 long=topo([f[i] for i in sorted(L)]);assert len(long)==18 and all(len(q)==2 and q[0]==q[1][::-1] for q in long.values())
 short=topo([f[i] for i in sorted(S)]); all_e=topo(f)
 Sv={j for i in S for j in f[i]};Lv={j for i in L for j in f[i]}
 dropV=Sv-Lv;assert len(Sv)==len(Lv)==8 and len(dropV)==4
 shared=Sv&Lv; assert all(len(r)==2 and all(x in shared for x in k) for k,r in long.items() if k in short)
 assert {k for k,r in short.items() if len(r)==1}=={k for k,r in short.items() if k in long}
 assert all(len(all_e[k])==(3 if k in long else len(r)) for k,r in short.items())
 assert all(not dropV.intersection(f[i]) for i in range(len(f)) if i not in S)
 bottom_y=max(v[i][1] for i in shared)
 top_y=min(v[i][1] for i in Lv-shared)
 yy=[v[i][1] for i in dropV]; assert max(yy)-min(yy)<1e-7 and bottom_y<min(yy) and max(yy)<top_y
 order=[i for i in range(len(v)) if i not in dropV];ids={j:i for i,j in enumerate(order)}
 KF=[i for i in range(len(f)) if i not in S]
 nf=[list(map(ids.__getitem__,f[i])) for i in KF]
 mapped_before=[f[i] for i in KF]
 after=topo(mapped_before); assert set(k for k in all_e if len(all_e[k])==1)==set(k for k in after if len(after[k])==1)==set()
 assert all(k in all_e for k in after) and all(after[k]==q for k,q in all_e.items() if k not in short)
 assert hist(after)=={k:c-(4 if k==3 else 9 if k==2 else 0) for k,c in hist(all_e).items()}
 ee={};
 for i,ff in enumerate(nf):
  for j,(a,b) in enumerate(edges(ff)):ee.setdefault((min(a,b),max(a,b)),3*i+j)
 U,N,B,T,M,K=[one(g,b'LayerElement'+x) for x in (b'UV',b'Normal',b'Binormal',b'Tangent',b'Material',b'Smoothing')]
 for layer,mode,ref in ((U,b'ByPolygonVertex',b'IndexToDirect'),(N,b'ByPolygonVertex',b'IndexToDirect'),(B,b'ByPolygonVertex',b'Direct'),(T,b'ByPolygonVertex',b'Direct'),(M,b'AllSame',b'IndexToDirect'),(K,b'ByPolygon',b'Direct')):
  assert val(layer,b'MappingInformationType')==mode and val(layer,b'ReferenceInformationType')==ref
 Kf=[3*j+k for j in KF for k in range(3)]
 A=[(val(g,b'Vertices'),[x for j in order for x in v[j]]),(val(g,b'PolygonVertexIndex'),[q if i<2 else -1-q for ff in nf for i,q in enumerate(ff)]),(val(g,b'Edges'),list(ee.values()))]
 for layer,k,n,keep in ((K,b'Smoothing',1,KF),(U,b'UVIndex',1,Kf),(N,b'NormalsIndex',1,Kf),(B,b'Binormals',3,Kf),(T,b'Tangents',3,Kf)):
  arr=val(layer,k);A.append((arr,[x for i in keep for x in arr[i*n:i*n+n]]))
 # Capture source arrays before editing to verify redundant UV and vector fields independently.
 u=transpose(val(U,b'UV'),2);ni=val(N,b'NormalsIndex');ui=val(U,b'UVIndex')
 n=transpose(val(N,b'Normals'),3);b=transpose(val(B,b'Binormals'),3);t=transpose(val(T,b'Tangents'),3)
 def record(i):
  return dict(x=[v[j] for j in f[i]],uv=[u[ui[j]] for j in range(3*i,3*i+3)],normal=[n[ni[j]] for j in range(3*i,3*i+3)],tangent=t[3*i:3*i+3],binormal=b[3*i:3*i+3])
 local={k:{i:record(i) for i in ss} for k,ss in [('long',L),('short',S)]}
 def assign(dst,src):dst[:]=type(dst)(dst.typecode,src)
 before=[list(a) for a,_ in A]
 for a,q in A:assign(a,q)
 methods=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32','add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array','add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
 def clone(x):
  e=encode_bin.FBXElem(x.id)
  for k,v in zip(x.props_type,x.props):getattr(e,methods[k])(v)
  e.elems=[clone(y) for y in x.elems];return e
 def sig(x):return(x.id,bytes(x.props_type),tuple(x.props),tuple(sig(y) for y in x.elems))
 dest=D/'out'/p.name;dest.parent.mkdir(exist_ok=True)
 with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(r)
 encode_bin.write(str(dest),payload,version)
 t,ver=parse_fbx.parse(str(dest)); assert ver==version and sig(t)==sig(r)
 for (a,q),old in zip(A,before):assign(a,old)
 assert sig(r)==sig(parse_fbx.parse(str(p))[0])
 return dict(original_canonical_sha256=H(and_old),trial_source_sha256=h,patch_sha256=H(dest),triangles_before=len(f),triangles_after=len(nf),
  removed_faces=sorted(S),kept_long_faces=sorted(L),
  removed_vertices=sorted(dropV),same_index_edges_before=hist(all_e),same_index_edges_after=hist(after),
  near_mid_geometry_equal_to_canonical_before=True,local=local)
if __name__=='__main__':
 ans={p[0] or 'LOD0':repair(*p) for p in PLAN}
 (D/'raw.json').write_text(json.dumps(ans,indent=2)+'\n')
