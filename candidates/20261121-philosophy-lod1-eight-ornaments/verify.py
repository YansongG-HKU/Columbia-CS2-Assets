"""Independently check FBX parity, exact unchanged positions/UV, and separate intended ornament seating."""
import bpy,sys,collections,json,hashlib,csv,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
D=Path(sys.argv[sys.argv.index('--')+1]).resolve()
src=D/'input/import-assets/PhilosophyHall'; trial=D/'trial'
p0=src/'NA_PhilosophyHall_6x4_LOD1.fbx'; p1=trial/p0.name
tag='NA_PhilosophyHall_6x4'; tags=('BaseColor','Normal','MaskMap','ControlMask','Emissive')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
data=json.loads((D/'donor-plan.json').read_text())
s0=set(); logs=[]
bpy.ops.wm.read_factory_settings(use_empty=True)
def load(p):
 keep=set(bpy.context.scene.objects)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 o,=[o for o in bpy.context.scene.objects if o not in keep and o.type=='MESH'];m=o.data
 assert not m.validate(verbose=True,clean_customdata=False)
 V=[o.matrix_world@v.co for v in m.vertices]
 f=[tuple(p.vertices) for p in m.polygons]
 U=[[tuple(m.uv_layers[0].data[l].uv) for l in p.loop_indices] for p in m.polygons]
 N=[[tuple((o.matrix_world.to_3x3()@m.corner_normals[k].vector).normalized()) for k in p.loop_indices] for p in m.polygons]
 assert all(p.area>1e-9 and len(p.vertices)==3 for p in m.polygons)
 im={}
 for c in tags:
  path=p.with_name(tag+'_'+c+'.png'); i=bpy.data.images.load(str(path),check_existing=False); assert len(i.pixels)>0
  im[c]={'sha256':sha(path),'dimensions':tuple(i.size)}
 native=[n.image for a in m.materials if a and a.node_tree for n in a.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
 assert len(native)>=2
 for i in native:
  path=Path(bpy.path.abspath(i.filepath)).resolve()
  assert path.parent==p.parent and path.is_file() and len(i.pixels)>0,(i.filepath,p)
 return o,V,f,U,N,im
o0,V,F,U,N,im=load(p0)
o1,v,f,u,n,m=load(p1);assert m==im
assert len(V)==12279 and len(F)==19264 and len(v)==12351 and len(f)==19416
old_omit={tuple(sorted(a['old_vertex_ids'])) for a in data['components']}
K=[i for i,ff in enumerate(F) if tuple(sorted(ff)) not in old_omit]; assert len(K)==19256
# Retained positions, winding, UVs and custom normals match at each corresponding corner.
assert all(tuple(V[a])==tuple(v[b]) for i,j in enumerate(K) for a,b in zip(F[j],f[i]))
assert all(U[j]==u[i] for i,j in enumerate(K))
nd=max(math.dist(j,k) for ii,o in enumerate(K) for j,k in zip(N[o],n[ii])); assert nd<.00012
A=lambda v:[list(map(min,zip(*v))),list(map(max,zip(*v)))]
assert A(V)==A(v)
convex={}; local={}; contacts=[]; edges8=0
parts={}; target=range(19256,19416)
T=BVHTree.FromPolygons(v,f,all_triangles=True,epsilon=1e-8)
over=T.overlap(T)
for j,p in enumerate(data['components']):
 fids=range(19256+20*j,19256+20*(j+1)); subset=[f[i] for i in fids]; ids=sorted({k for r in subset for k in r})
 E=collections.defaultdict(list)
 for r in subset:
  for a,b in zip(r,r[1:]+r[:1]):E[min(a,b),max(a,b)].append((a,b))
 assert len(ids)==12 and len(E)==30 and all(len(a)==2 and a[0]==a[1][::-1] for a in E.values())
 edges8+=len(E)
 md=max(min((v[a]-Vector(b)).length for b in p['world_vertices']) for a in ids)
 assert md<.000004
 for ii in fids:parts[ii]=j
 for k,ff in zip(fids,p['donor_uv_corners']):
  assert max(math.dist(aa,bb) for aa,bb in zip(ff,u[k]))<1e-7
 group_points=[v[i] for i in ids]
 convex[j]={'center':p['center'],'n_faces':len(subset),'bounds':A(group_points),'max_error_m_vs_near':md}
# The western/eastern pedestal bezels in the portable model slope a few millimetres above
# the original near-tier flat top datums. Match the actual pedestal/capital owner, not a guessed common z.
graph=collections.defaultdict(set)
for face in f[:19256]:
 for a in face:graph[a].update(face)
owner={}
cache={}
def owner_for(fid):
 i=f[fid][0]
 if i in owner:return cache[owner[i]]
 q=[i]; nodes={i}
 while q:
  k=q.pop()
  new=graph[k]-nodes
  q.extend(new);nodes|=new
 k=min(nodes);cap=A([v[i] for i in nodes]);e={'v':len(nodes),'bounds':cap,'start':k}
 for i in nodes:owner[i]=k
 cache[k]=e;return e
hosts={}

for j,k in over:
 if j>=k or (j not in parts and k not in parts):continue
 if not set(f[j]).isdisjoint(f[k]):continue
 if j in parts and k in parts:
  raise RuntimeError(('donor crossed donor',j,k))
 ind=j if j in parts else k; oth=k if j in parts else j
 q=[v[a] for a in f[ind]]; t=[v[a] for a in f[oth]]
 z0=max(min(d.z for d in q),min(d.z for d in t));z1=min(max(d.z for d in q),max(d.z for d in t))
 host=owner_for(oth)
 b0,b1=host['bounds']; part=convex[parts[ind]];cx,cy,cz=part['center']
 near=(b0[0]-.015<cx<b1[0]+.015 and b0[1]-.015<cy<b1[1]+.015)
 if near and b1[2]<9.72 and b0[2]<9.61 and z1<=9.72:where='lower_existing_pedestal_seat'
 elif near and b0[2]>10.28 and b1[2]>10.34 and z0>=10.28:where='upper_existing_capital_seat'
 else:where='outside_approved_sockets'
 hosts[host['start']]=host
 contacts.append((parts[ind],where,oth,z0,z1))
report={'raw_export_triangles':19416,'before_blender_triangles':19264,'targeted_donor_components':convex,'donor_oriented_edges':edges8,
 'unchanged_faces_with_exact_corner_positions_uv':len(K),'untouched_corner_normals_max_distance':nd,'absolute_bounds':A(v),'five_unchanged_lod1_shared_maps':m,
 'bvh_triangles_touching_rest_breakdown':dict(collections.Counter(h[1] for h in contacts)),
 'known_contact_host_components':hosts,'outside_seats': [x for x in contacts if x[1]=='outside_approved_sockets']}
(D/'verify-receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('LOCAL_RECEIPT',json.dumps(report),flush=True)
assert not report['outside_seats'],report['outside_seats'][:15]
# Render the same shaded magnified crop. Use a single proof color only for restored local components.
def mat(n,rgb):
 m=bpy.data.materials.new(n);m.diffuse_color=rgb;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=rgb;p.inputs['Roughness'].default_value=.70
 return m
plain=mat('Context geometry',(.46,.49,.50,1)); changed=mat('Eight component check',(.05,.38,.44,1)); old=mat('Existing collapsed strips',(.78,.36,.15,1))
K0={i for i,ff in enumerate(F) if tuple(sorted(ff)) in old_omit}
for o,k in [(o0,K0),(o1,set(target))]:
 o.data.materials.clear();o.data.materials.append(plain);o.data.materials.append(old if o==o0 else changed)
 for p in o.data.polygons:p.material_index=int(p.index in k)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=22;sc.cycles.device='CPU';sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=670;sc.render.resolution_y=500;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Neutral');sc.world.use_nodes=True;sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.82
for e,rot in [(2.1,(.6,-.45,-.72)),(.8,(-.50,.31,.46))]:
 l=bpy.data.lights.new('Directional','SUN');l.energy=e;ob=bpy.data.objects.new('Directional',l);sc.collection.objects.link(ob);ob.rotation_euler=rot
C=bpy.data.cameras.new('Frozen view');C.type='ORTHO';C.ortho_scale=1.7
c=bpy.data.objects.new('Frozen view',C);sc.collection.objects.link(c);sc.camera=c
aim=Vector((4.,-5.50,9.98));c.location=aim+Vector((3.4,-6.9,1.6));c.rotation_euler=(aim-c.location).to_track_quat('-Z','Y').to_euler()
for tag,yes,no in [('before',o0,o1),('after',o1,o0)]:
 yes.hide_render=False;no.hide_render=True;sc.render.filepath=str(D/(tag+'-ornament.png'));bpy.ops.render.render(write_still=True)
