"""Independently reimport both game LOD2 FBXs and verify identical topology/UV/resources."""
import bpy,sys,json,collections,statistics,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
before,after,out=map(Path,sys.argv[sys.argv.index('--')+1:]); stem=before.stem
sep=('BaseColor','Normal','MaskMap','Emissive','ControlMask')
def quant(a):return [statistics.median(a),statistics.quantiles(a,n=100,method='inclusive')[89],statistics.quantiles(a,n=100,method='inclusive')[94]]
def geometry(o):
 m=o.data; vv=[o.matrix_world@v.co for v in m.vertices]; f=[list(p.vertices) for p in m.polygons]; assert all(len(x)==3 for x in f)
 E=collections.defaultdict(list)
 for a in f:
  for x,y in zip(a,a[1:]+a[:1]): E[min(x,y),max(x,y)].append((x,y))
 assert all(len(a)==2 and a[0]==a[1][::-1] for a in E.values())
 assert min(p.area for p in m.polygons)>1.e-5
 tree=BVHTree.FromPolygons(vv,f,all_triangles=True,epsilon=1e-7)
 I={(i,j) for i,j in tree.overlap(tree) if i<j and set(f[i]).isdisjoint(f[j])}
 bounds=[list(map(min,zip(*vv))),list(map(max,zip(*vv)))]
 uv=[tuple(v.uv) for v in m.uv_layers.active.data]
 return vv,f,tree,I,bounds,uv,len(E)
def load(path):
 objects=set(bpy.context.scene.objects); before_images=set(bpy.data.images)
 bpy.ops.import_scene.fbx(filepath=str(path),use_image_search=False)
 o,=[x for x in bpy.context.scene.objects if x not in objects and x.type=='MESH']
 decoded={}; imgs={}
 for tag in sep:
  q=path.with_name(stem+'_'+tag+'.png'); im=bpy.data.images.load(str(q),check_existing=False)
  assert len(im.pixels)>0 and im.size[0]>0
  imgs[tag]=im;decoded[tag]={'size':tuple(im.size),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
 slots=[node.image for m in o.data.materials if m and m.node_tree for node in m.node_tree.nodes if node.type=='TEX_IMAGE' and node.image]
 assert slots
 native={Path(im.filepath).name:len(im.pixels)>0 for im in slots}
 assert all(native.values()),native
 return o,decoded,imgs,native
bpy.ops.wm.read_factory_settings(use_empty=True)
ob,bt,bi,bn=load(before);oa,at,ai,an=load(after)
assert bt==at and bn==an
v0,f0,t0,i0,b0,u0,e0=geometry(ob);v1,f1,t1,i1,b1,u1,e1=geometry(oa)
assert b0==b1 and f0==f1 and u0==u1 and e0==e1==1104
assert not i1-i0,sorted(i1-i0)
delta=[(b-a) for a,b in zip(v0,v1)]
assert sum(x.length>1e-6 for x in delta)==48 and max(abs(x.x)+abs(x.y) for x in delta)<1e-5
assert all(0<x.z<.71 for x in delta if x.length>1e-6)
moved={i for i,x in enumerate(delta) if x.length>1.e-6}; impacted={i for i,f in enumerate(f0) if set(f)&moved}
assert not any(i in impacted or j in impacted for i,j in i1)
base_err=[]; fit_err=[]
for line in (out/'held-roof-local.csv').read_text().splitlines():
 x,y,z=map(float,line.split(',')); xy=Vector((x,y+9,100)); dr=Vector((0,0,-1))
 aa=t0.ray_cast(xy,dr)[0]; bb=t1.ray_cast(xy,dr)[0]
 assert aa is not None and bb is not None
 base_err.append(abs(aa.z-37-z));fit_err.append(abs(bb.z-37-z))
report={'blender_incoming_fbx_texture_slots_match_and_decode':an,'all_maps_dimensions_sha256_equal':at,'bounds_unchanged':b1,'vertices':len(v1),'triangles':len(f1),'oriented_paired_edges':e1,'all_uv_corners_equal':len(u1),'moved_vertices':len(moved),'affected_triangles':len(impacted),'old_scene_crossing_pairs_raw_bvh':len(i0),'new_scene_crossing_pairs_raw_bvh':len(i1),'new_crossing_pairs':len(i1-i0),'affected_crown_crossing_pairs':0,'n_hold':len(base_err),'old_apex_aligned_hold_p50_p90_p95':quant(base_err),'patched_apex_aligned_hold_p50_p90_p95':quant(fit_err)}
assert report['patched_apex_aligned_hold_p50_p90_p95'][1] < .7
(out/'fbx-readback.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
def shaded(o,imgs):
 mat=bpy.data.materials.new('Base color + tangent normal readback');mat.use_nodes=True
 ns=mat.node_tree.nodes;lk=mat.node_tree.links;p=ns.get('Principled BSDF')
 p.inputs['Roughness'].default_value=.64
 alb=ns.new('ShaderNodeTexImage');alb.image=imgs['BaseColor']
 nor=ns.new('ShaderNodeTexImage');nor.image=imgs['Normal'];nor.image.colorspace_settings.name='Non-Color'
 nm=ns.new('ShaderNodeNormalMap');lk.new(nor.outputs['Color'],nm.inputs['Color']);lk.new(nm.outputs['Normal'],p.inputs['Normal']);lk.new(alb.outputs['Color'],p.inputs['Base Color'])
 for i in range(len(o.data.materials)):o.data.materials[i]=mat
shaded(ob,bi);shaded(oa,ai)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=24;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=600;sc.render.resolution_y=350;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Environment');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.75
for e,rot in [(1.9,(.55,-.45,-.4)),(.65,(-.7,.28,1.0))]:
 s=bpy.data.lights.new('Sun','SUN');s.energy=e
 o=bpy.data.objects.new('Sun',s);sc.collection.objects.link(o);o.rotation_euler=rot
lens=bpy.data.cameras.new('Same crown view');lens.type='ORTHO';lens.ortho_scale=44
cam=bpy.data.objects.new('Same crown view',lens);sc.collection.objects.link(cam);sc.camera=cam
cam.location=Vector((37,-48,56));cam.rotation_euler=(Vector((0,9,34))-cam.location).to_track_quat('-Z','Y').to_euler()
for tag,obj,other in [('lod2-before',ob,oa),('lod2-after',oa,ob)]:
 obj.hide_render=False;other.hide_render=True;sc.render.filepath=str(out/(tag+'.png'));bpy.ops.render.render(write_still=True)
