"""Independent GLB readback: geometry counts, real two flat runs per ramp and clear glass."""
from pathlib import Path
import json,struct,sys,hashlib,collections,math
p=Path(sys.argv[1])
data=p.read_bytes()
magic, version, total=struct.unpack_from('<4sII',data)
assert (magic,version,total)==(b'glTF',2,len(data))
length,kind=struct.unpack_from('<I4s',data,12);assert kind==b'JSON'
doc=json.loads(data[20:20+length])
n2,k2=struct.unpack_from('<I4s',data,20+length)
assert k2==b'BIN\0' and 28+length+n2==len(data)
b=data[28+length:]
def decode(accessor):
 a=doc['accessors'][accessor]; v=doc['bufferViews'][a['bufferView']]
 cf={5121:'B',5123:'H',5125:'I',5126:'f'}[a['componentType']]
 nf={'SCALAR':1,'VEC3':3}[a['type']]
 fmt='<'+cf*nf; n=struct.calcsize(fmt); stride=v.get('byteStride',n); bo=v.get('byteOffset',0)+a.get('byteOffset',0)
 assert n<=stride and bo+(a['count']-1)*stride+n<=v.get('byteOffset',0)+v['byteLength']
 return [struct.unpack_from(fmt,b,bo+i*stride) for i in range(a['count'])]
groups=collections.Counter(); checks={}
for node in doc['nodes']:
 assert 'mesh' in node and 'camera' not in node
 assert not any(k in node for k in ('translation','scale','matrix','rotation')) # raw vertex verification in model frame
 name=node['name'];m=doc['meshes'][node['mesh']];assert len(m['primitives'])==1
 q=m['primitives'][0];assert q.get('mode',4)==4
 pos=decode(q['attributes']['POSITION'])
 ix=[i[0] for i in decode(q['indices'])]
 assert max(ix)<len(pos) and len(ix)%3==0
 tri=len(ix)//3
 g='pane' if name.startswith('Pane_') else 'ramp' if name.startswith('Ramp_') else 'steel/detail'
 groups[g+'_meshes']+=1;groups[g+'_triangles']+=tri
 # Weld quantized position independently to check manifold triangle mesh after export duplicates.
 keys=[tuple(round(k,6) for k in c) for c in pos]
 E=collections.defaultdict(list)
 for i in range(0,len(ix),3):
  ps=[keys[j] for j in ix[i:i+3]]
  assert len(set(ps))==3
  for a,c in zip(ps,ps[1:]+ps[:1]): E[tuple(sorted((a,c)))].append((a,c))
 assert all(len(v)==2 and v[0]==v[1][::-1] for v in E.values()),name
 if g in ('pane','ramp'):
  material=doc['materials'][q['material']]
  tf=material['extensions']['KHR_materials_transmission']['transmissionFactor']
  assert abs(tf-(.96 if g=='pane' else .50))<.00001
 if g=='ramp':
  h={}
  for x,yy,zz in pos: h[max(0.,round(x,3))]=max(yy,h.get(max(0.,round(x,3)),-1e3))
  x=sorted(h); z=[round(h[v],4) for v in x]; dif=[round(c-a,5) for a,c in zip(z,z[1:])]
  assert len(x)==6 and x[0]==0 and x[-1]==30.48 and dif[1]==dif[3]==0 and min(dif)>=0 and abs(sum(dif)-1.68)<.001
  checks[name]={'path_section_x_m':x,'top_yup_height_m':z,'flat_intervals':[[x[1],x[2]],[x[3],x[4]]],'rise_m':round(sum(dif),4)}
assert groups['pane_meshes']==119 and groups['ramp_meshes']==3
assert not doc.get('images') and 'KHR_materials_transmission' in doc['extensionsUsed']
r={'exact_glb_readback':{'byte_size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'glb_mesh_counts':dict(groups),
 'all_meshes_welded_positions_return_closed_oriented':True,'point_glass_transmission_verified':True,'three_ramp_sections':checks},
 'disclaimer':'No authoritative interior or exterior building registration, no CS2 interoperability asserted. Individual metal/support primitives can overlap intentionally.'}
p.with_name('glb-readback.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
