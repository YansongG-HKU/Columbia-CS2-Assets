"""Independently read six FBXs; verify local geometry invariants, compare held rays, and render."""
import bpy,sys,collections,json,hashlib,statistics,struct,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
d,old_far=map(Path,sys.argv[sys.argv.index('--')+1:]); d=d.resolve(); trial=d/'trial'
stem='NA_ColumbiaLowLibrary_13x10'
names=[stem,stem+'_LOD1',stem+'_LOD2']
S=('BaseColor','Normal','MaskMap','Emissive','ControlMask')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.read_factory_settings(use_empty=True)
pcoords=[list(map(float,l.split(','))) for l in (d/'held-roof-local.csv').read_text().splitlines()]
special=[list(map(float,l.split(','))) for l in (d/'shoulder-held-local.csv').read_text().splitlines()]
previous_far=json.loads((d/'previous-far-rays.json').read_text()); assert all(a[:3]==b for a,b in zip(previous_far,pcoords)) and len(previous_far)==len(pcoords)
bins=['inner_0_2p75','mid_2p75_10p5','outer_10p5_11p42']
groups=[bins[0] if math.hypot(x,y)<2.75 else bins[1] if math.hypot(x,y)<10.5 else bins[2] for x,y,z in pcoords]
def qs(a):return [statistics.median(a),statistics.quantiles(a,n=100,method='inclusive')[89],statistics.quantiles(a,n=100,method='inclusive')[94]]
def loads(path,tier):
 bpy.ops.wm.read_factory_settings(use_empty=True)
 path=path.resolve()
 bpy.ops.import_scene.fbx(filepath=str(path),use_image_search=False)
 o,=[o for o in bpy.context.scene.objects if o.type=='MESH'];m=o.data;p=o.matrix_world
 V=[p@v.co for v in m.vertices]; T=[tuple(q.vertices) for q in m.polygons]; assert all(len(f)==3 for f in T)
 topo=hashlib.sha256(); UV=hashlib.sha256(); slot=hashlib.sha256()
 for f in T:topo.update(struct.pack('<3I',*f))
 for u in m.uv_layers.active.data:UV.update(struct.pack('<2f',*u.uv))
 for f in m.polygons:slot.update(struct.pack('<I',f.material_index))
 bounds=list(map(list,zip([*map(min,zip(*V))],[*map(max,zip(*V))])))
 local=[]; high=[]; indices=[]
 all_edges=collections.defaultdict(int)
 for i,f in enumerate(T):
  uv=[V[j] for j in f]
  if not all(v.z>32 and abs(v.x)<18 and abs(v.y-9)<18 for v in uv):continue
  local.append(f);indices.append(i)
  if min(v.z for v in uv)>36:high.append(i)
 assert len(local)>130
 tree=BVHTree.FromPolygons(V,local,all_triangles=True,epsilon=1e-7)
 raw_pairs={(indices[i],indices[j]) for i,j in tree.overlap(tree) if i<j and set(local[i]).isdisjoint(local[j])}
 for f in local:
  for x,y in zip(f,f[1:]+f[:1]):all_edges[min(x,y),max(x,y)]+=1
 z=[]
 for x,y,_ in pcoords+special:
  h=tree.ray_cast(Vector((x,y+9,100)),Vector((0,0,-1)))[0]; assert h is not None and h.z>36
  z.append(float(h.z))
 native={}
 for node in (u for mat in m.materials if mat and mat.node_tree for u in mat.node_tree.nodes if u.type=='TEX_IMAGE' and u.image):
  k=Path(node.image.filepath).name; native[k]=len(node.image.pixels)>0
 assert len(native)>=2 and all(native.values()),(path,native)
 tex={}
 images={}
 for tag in S:
  name=(names[2] if tier==2 else names[0])+'_'+tag+'.png'
  q=path.with_name(name)
  im=bpy.data.images.load(str(q),check_existing=False); assert im.pixels[0]>=0
  tex[tag]={'sha256':sha(q),'shape':list(im.size)}
  images[tag]=im
 return o,m,V,T,raw_pairs,{'sha256':sha(path),'faces':len(T),'vertices':len(V),'bounds_by_axis':bounds,'topology_sha256':topo.hexdigest(),
      'material_index_sha256':slot.hexdigest(),'uv_sha256':UV.hexdigest(),'corners':len(m.uv_layers.active.data),
      'all_5_maps':tex,'native_FBX_slots_decode':native,'crown_local_triangles':len(local),'local_edge_incidence_counts':dict(collections.Counter(all_edges.values())),
      'old_or_new_local_bvh_pairs':len(raw_pairs)},z,images
def render(obj,images,out,side=False):
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=20;sc.cycles.device='CPU';sc.cycles.use_denoising=False
 sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=540;sc.render.resolution_y=310;sc.render.resolution_percentage=100
 sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
 sc.world=bpy.data.worlds.new('Environment');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.85
 mat=bpy.data.materials.new('Diffuse plus normal');mat.use_nodes=True
 n=mat.node_tree.nodes;l=mat.node_tree.links;pbs=n.get('Principled BSDF'); pbs.inputs['Roughness'].default_value=.65
 t=n.new('ShaderNodeTexImage'); t.image=images['BaseColor'];l.new(t.outputs['Color'],pbs.inputs['Base Color'])
 r=n.new('ShaderNodeTexImage'); r.image=images['Normal'];r.image.colorspace_settings.name='Non-Color';no=n.new('ShaderNodeNormalMap');l.new(r.outputs['Color'],no.inputs['Color']);l.new(no.outputs['Normal'],pbs.inputs['Normal'])
 for k in range(len(obj.data.materials)):obj.data.materials[k]=mat
 for e,rot in [(1.9,(.65,-.45,-.4)),(.8,(-.70,.3,1.0))]:
  light=bpy.data.lights.new('Sun','SUN');light.energy=e;s=bpy.data.objects.new('Key',light);sc.collection.objects.link(s);s.rotation_euler=rot
 cam=bpy.data.cameras.new('Matching view');cam.type='ORTHO';cam.ortho_scale=38
 ob=bpy.data.objects.new('Matching view',cam);sc.collection.objects.link(ob);sc.camera=ob
 C=Vector((0,9,37.5))
 ob.location=C+Vector((29,-55,20 if not side else 4));ob.rotation_euler=(C-ob.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(out);bpy.ops.render.render(write_still=True)
refz=[p[2] for p in pcoords]; rec=[]; samples={}
for tier,name in enumerate(names):
 old=(d/(name+'.fbx')) if tier<2 else old_far
 new=trial/(name+'.fbx')
 ob,mo,vo,to,ix0,ra,z0,im0=loads(old,tier)
 def hold(a):return qs([abs(u-37-v) for u,v in zip(a,refz)])
 ra['held_xyz_common_apex_datum_abs_p50_p90_p95_m']=hold(z0)
 if tier==0:render(ob,im0,d/'near-before.png')
 del ob,mo,im0
 ob,mo,vo1,t1,ix1,rb,z1,im1=loads(new,tier)
 stable=('faces','vertices','bounds_by_axis','topology_sha256','material_index_sha256','uv_sha256','corners','all_5_maps','native_FBX_slots_decode','crown_local_triangles','local_edge_incidence_counts')
 assert all(ra[f]==rb[f] for f in stable),[f for f in stable if ra[f]!=rb[f]]
 assert not ix1-ix0,sorted(ix1-ix0)[:40]
 dv=[q-p for p,q in zip(vo,vo1)]; moved={i for i,v in enumerate(dv) if v.length>1e-6}
 assert len(moved)==(768 if tier<2 else 72)
 assert all(abs(v.x)+abs(v.y)<1e-5 and 0<v.z<.75 for i,v in enumerate(dv) if i in moved)
 changed={i for i,f in enumerate(t1) if moved.intersection(f)}
 assert all(mo.polygons[i].area>1e-5 for i in changed)
 assert not any(i in changed or j in changed for i,j in ix1),[(i,j) for i,j in ix1 if i in changed or j in changed][:40]
 rb.update({'held_xyz_common_apex_datum_abs_p50_p90_p95_m':hold(z1),'moved_vertices':len(moved),'affected_tris':len(changed),'new_local_pairs':len(ix1-ix0),'pairs_touching_affected_triangles_in_result':0})
 if tier<2:assert rb['held_xyz_common_apex_datum_abs_p50_p90_p95_m'][0]<.21
 rec.append({'tier':tier,'before':ra,'after':rb})
 samples[tier]=(z0[:len(pcoords)],z1[:len(pcoords)])
 rb['additional_held_shoulder_navd88_abs_p50_p90_p95_m']=qs([abs(a-37-p[2]) for a,p in zip(z1[len(pcoords):],special)])
 ra['additional_held_shoulder_navd88_abs_p50_p90_p95_m']=qs([abs(a-37-p[2]) for a,p in zip(z0[len(pcoords):],special)])
 json.dump(rec,(d/'individual-readback.json').open('w'),indent=2)
 render(ob,im1,d/f'lod{tier}-after.png')
 render(ob,im1,d/f'lod{tier}-side.png',True)
z0,z1=samples[0];m0,m1=samples[1];f0,f1=samples[2]
assert z0==m0 and z1==m1
def compare(u,v,group=None):
 return qs([abs(x-y) for i,(x,y) in enumerate(zip(u,v)) if group is None or groups[i]==group])
result={'n_hold':len(refz),'data_note':'All three models compared in original game coordinates without per-model shifting. For absolute LiDAR residual only, a shared local offset uses game LOD2 apex z43 as survey central z88. No installation/ground registration.',
 'near_mid_before_and_after_are_exactly_equal_at_all_ray_origins':True,
 'near_far_previous_untouched_near_and_already_corrected_far_p50_p90_p95':compare(z0,[p[3] for p in previous_far]),
 'near_far_after_this_batch_p50_p90_p95':compare(z1,f1),
 'n_additional_held_at_shoulder_annulus':len(special),
 'near_far_after_near_mid_only_shoulder_before_p50_p90_p95':compare(z1,[p[3] for p in previous_far]),
 'near_far_before_this_batch_by_range':{g:compare(z0,[p[3] for p in previous_far],g) for g in bins},
 'near_far_after_this_batch_by_range':{g:compare(z1,f1,g) for g in bins},
 'near_far_before_both_batches_p50_p90_p95':compare(z0,f0),'groups_counts':dict(collections.Counter(groups))}
assert result['near_far_after_this_batch_p50_p90_p95'][0] < .25
assert result['near_far_after_this_batch_by_range']['outer_10p5_11p42'][0] < .25
(d/'crosslod-readback.json').write_text(json.dumps(result,indent=2)+'\n')
print('VERIFIED',result)
