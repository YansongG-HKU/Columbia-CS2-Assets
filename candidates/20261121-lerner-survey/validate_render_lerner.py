"""Independent Blender readback of calibrated CityGML shell for Lerner Hall."""
import collections,json,sys,bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
base,fit,old_fbx,out=map(Path,sys.argv[sys.argv.index('--')+1:]);assert out.is_dir()
bpy.ops.wm.read_factory_settings(use_empty=True)
def imp(fp):
 before=set(bpy.context.scene.objects)
 bpy.ops.wm.obj_import(filepath=str(fp),forward_axis='Y',up_axis='Z')
 return next(o for o in bpy.context.scene.objects if o not in before and o.type=='MESH')
def audit(o,open_expected,nonadj=True):
 m=o.data; assert not m.validate(verbose=True,clean_customdata=False)
 vv=[o.matrix_world@v.co for v in m.vertices]; ii=[tuple(p.vertices) for p in m.polygons]
 E=collections.defaultdict(list);minarea=min(p.area for p in m.polygons)
 for f in ii:
  assert len(f)==3
  for x,y in zip(f,f[1:]+f[:1]):E[tuple(sorted((x,y)))].append((x,y))
 boundary=[k for k,v in E.items() if len(v)==1]
 assert len(boundary)==open_expected and minarea>1.e-5
 assert all(len(v)==1 or (len(v)==2 and v[0]==v[1][::-1]) for v in E.values())
 vol=sum(vv[a].dot(vv[b].cross(vv[c])) for a,b,c in ii)/6
 if not open_expected: assert vol>10000
 disjoint=[]
 if nonadj:
  tree=BVHTree.FromPolygons(vv,ii,all_triangles=True,epsilon=1e-7)
  for i,j in tree.overlap(tree):
   if i>=j or not set(ii[i]).isdisjoint(ii[j]):continue
   disjoint.append((i,j))
  assert not disjoint,disjoint
 return {'verts':len(vv),'tris':len(ii),'oriented_two_face_edges':len(E)-len(boundary),'open_cut_edges':len(boundary),
  'disjoint_triangle_intersections':len(disjoint),'min_face_area_m2':minarea,
  'signed_volume_m3':vol if not open_expected else None,
  'extent':[list(map(min,zip(*vv))),list(map(max,zip(*vv)))]}
a=imp(base); b=imp(fit)
ra=audit(a,0); rb=audit(b,0)
assert ra['extent'][0][:2]==rb['extent'][0][:2] and ra['extent'][1][:2]==rb['extent'][1][:2]
bpy.ops.import_scene.fbx(filepath=str(old_fbx))
old=[x for x in bpy.context.scene.objects if x.type=='MESH' and x not in (a,b)]
assert len(old)==1
m=old[0]; m.data.calc_loop_triangles()
vv=[m.matrix_world@v.co for v in m.data.vertices]
print('OLD_FBX',m.name,len(m.data.loop_triangles),list(map(min,zip(*vv))),list(map(max,zip(*vv))))
(out/'blender-readback.json').write_text(json.dumps({'city_reference':ra,'calibrated_candidate':rb,'old_game_lod2':{'name':m.name,'triangle_count':len(m.data.loop_triangles),'original_world_extent':[list(map(min,zip(*vv))),list(map(max,zip(*vv)))]}},indent=2)+'\n')
m.hide_render=True
def mat(n,col,r=.7):
 m=bpy.data.materials.new(n);m.diffuse_color=col;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=r
 return m
wall=mat('Neutral wall',(.46,.51,.58,1)); roof=mat('Verified heights group',(.10,.42,.58,1))
hot=mat('Roof tier measured separately',(.055,.40,.50,1))
low=mat('Historical upper structures not inferred from LiDAR',(.48,.33,.21,1))
hidden=mat('Underside',(.14,.16,.18,1))
for mm in (wall,hot,low,hidden):b.data.materials.append(mm)
for p in b.data.polygons:p.material_index=(1 if p.normal.z>.9 and abs(p.center.z-22.81)<.01 else 2 if p.normal.z>.9 else 3 if p.normal.z<-.5 else 0)
a.hide_render=True
bpy.ops.mesh.primitive_plane_add(size=160,location=(0,0,0))
ground=bpy.context.object
ground.name='Provisional grade datum, not measured terrain geometry'
ground.data.materials.append(mat('Neutral reference plane',(.50,.57,.63,1)))
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=24;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=760;sc.render.resolution_y=520;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Background');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.75
def sun(n,energy,rot):
 s=bpy.data.lights.new(n,type='SUN');s.energy=energy;s.angle=.1
 ob=bpy.data.objects.new(n,s);sc.collection.objects.link(ob);ob.rotation_euler=rot
sun('Key',2.1,(.65,-.35,-.6));sun('Fill',1.1,(-.63,.27,.55))
lens=bpy.data.cameras.new('Common ortho');lens.type='ORTHO';lens.ortho_scale=110
cam=bpy.data.objects.new('QA orthographic',lens);sc.collection.objects.link(cam);sc.camera=cam
for n,p,t in [('campus', (81,79,71),(0,0,13)),('broadway',(-93,-55,65),(0,0,13))]:
 cam.location=Vector(p);cam.rotation_euler=(Vector(t)-cam.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(out/(n+'.png'));bpy.ops.render.render(write_still=True)
