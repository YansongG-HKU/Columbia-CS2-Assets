"""Write the independently planned closed Low Memorial LOD2 annulus to a candidate FBX."""
import collections,hashlib,json,sys
from pathlib import Path
from io_scene_fbx import parse_fbx,encode_bin
d=Path(__file__).resolve().parent;sys.path.insert(0,str(d))
from repair_batch import item,prop,clone,value,steered_edges,digest
p=d/'NA_ColumbiaLowLibrary_13x10_LOD2.fbx'
out=d/'low-tile-candidate'/p.name
P=json.loads((d/'low-annulus-plan.json').read_text())
U=json.loads((d/'low-tile-report.json').read_text())
assert digest(p)==P['baseline_sha256'] and not out.exists()
root,ver=parse_fbx.parse(str(p));g=item(item(root,b'Objects'),b'Geometry')
v,l,e=[prop(g,k) for k in (b'Vertices',b'PolygonVertexIndex',b'Edges')]
xyz=[tuple(v[i:i+3]) for i in range(0,len(v),3)]
F=[tuple(x if x>=0 else -1-x for x in l[i:i+3]) for i in range(0,len(l),3)]
assert len(F)==P['source_triangles']
keep=[k for k in range(len(F)) if k not in P['remove_downward_inside_disk_faces']]
A=[tuple(r) for r in P['add_upward_annulus_triangles']]
new=[F[k] for k in keep]+A
E=steered_edges(new)
assert len(new)==P['proposed_triangles'] and len(E)==P['proposed_oriented_manifold_edges']
assert all(len(r)==2 and r[0][:2]==r[1][:2][::-1] for r in E.values())
def repl(arr,seq):arr[:]=type(arr)(arr.typecode,seq)
def layer(key,attr):return prop(item(g,key),attr)
repl(l,(x if k<2 else -1-x for r in new for k,x in enumerate(r)))
repl(e,(x[0][2] for x in E.values()))
n=item(g,b'LayerElementNormal')
assert prop(n,b'MappingInformationType')==b'ByVertice' and prop(n,b'ReferenceInformationType')==b'IndexToDirect'
Vn=prop(n,b'Normals'); ni=prop(n,b'NormalsIndex'); idx=len(Vn)//3; old=list(ni)
assert len(old)==len(xyz)
Vn.extend((0,1,0));item(n,b'MappingInformationType').props[0]=b'ByPolygonVertex'
repl(ni,[old[j] for k in keep for j in F[k]]+[idx]*(3*len(A)))
s=layer(b'LayerElementSmoothing',b'Smoothing');old=list(s)
repl(s,[old[k] for k in keep]+[0]*len(A))
uv=item(g,b'LayerElementUV'); vals=prop(uv,b'UV');ix=prop(uv,b'UVIndex'); lut={}
for k,point in sorted(U['uv_by_vertex'].items()):
 lut[int(k)]=len(vals)//2;vals.extend(point)
old=list(ix);repl(ix,[z for k in keep for z in old[k*3:k*3+3]]+[lut[j] for f in A for j in f])
for tag,attr,basis in ((b'LayerElementBinormal',b'Binormals','raw_binormal'),(b'LayerElementTangent',b'Tangents','raw_tangent')):
 ar=layer(tag,attr);old=list(ar)
 repl(ar,[z for k in keep for z in old[k*9:k*9+9]]+U[basis]*(3*len(A)))
# Normalize the model's portability diagnostics separately: paths intentionally unchanged here.
with encode_bin.FBXElem.enable_multithreading_cm():payload=clone(root)
encode_bin.write(str(out),payload,ver)
again,v2=parse_fbx.parse(str(out));assert v2==ver and value(again)==value(root)
report=dict(input_sha256=digest(p),output_sha256=digest(out),untouched_vertices=len(xyz),
    triangles=len(new),indexed_directed_edges=len(E),removed_downward_disk_faces=len(F)-len(keep),
    added_atlased_annulus_faces=len(A),render_validation_pending=True)
(d/'low-fbx-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
