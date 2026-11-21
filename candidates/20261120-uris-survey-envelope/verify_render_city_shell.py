"""Independent Blender readback of calibrated CityGML shell and survey rim."""
import collections,json,sys,bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
base,fit,rim,out=map(Path,sys.argv[sys.argv.index('--')+1:]);assert out.is_dir()
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
a=imp(base);b=imp(fit);c=imp(rim)
ra=audit(a,0);rb=audit(b,0);rc=audit(c,68)
assert ra['verts']==rb['verts'] and ra['tris']==rb['tris']
assert ra['extent'][0][:2]==rb['extent'][0][:2] and ra['extent'][1][:2]==rb['extent'][1][:2]
(out/'blender-readback.json').write_text(json.dumps({'original_city':ra,'survey_envelope':rb,'roof_rim_detail':rc},indent=2)+'\n')
print('BLENDER_EXACT_IMPORT',json.dumps(rb),flush=True)
def mat(n,col,r=.7):
 m=bpy.data.materials.new(n);m.diffuse_color=col;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=r
 return m
wall=mat('Neutral wall',(.46,.51,.58,1)); roof=mat('Verified heights group',(.10,.42,.58,1))
old=mat('Historical upper geometry no current exact match',(.43,.36,.28,1)); hidden=mat('Hidden / underside',(.15,.18,.22,1))
for m in (wall,roof,old,hidden):b.data.materials.append(m)
for p in b.data.polygons:
 v=[b.data.vertices[i].co.z + 46.46 for i in p.vertices]
 p.material_index=(2 if min(v)>85 and p.normal.z>.9 else 1 if p.normal.z>.9 else 3 if p.normal.z<-.5 else 0)
a.hide_render=True;c.hide_render=True
bpy.ops.mesh.primitive_plane_add(size=200,location=(-10,-17,0))
ground=bpy.context.object;ground.name='Provisional site reference plane at 46.46m';ground.data.materials.append(mat('neutral base',(.5,.57,.63,1)))
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=12;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=850;sc.render.resolution_y=635;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Background');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.75
def sun(n,energy,rot):
 s=bpy.data.lights.new(n,type='SUN');s.energy=energy;s.angle=.1
 ob=bpy.data.objects.new(n,s);sc.collection.objects.link(ob);ob.rotation_euler=rot
sun('Key',2.1,(.65,-.35,-.6));sun('Fill',1.1,(-.63,.27,.55))
lens=bpy.data.cameras.new('Common ortho');lens.type='ORTHO';lens.ortho_scale=112
cam=bpy.data.objects.new('QA orthographic',lens);sc.collection.objects.link(cam);sc.camera=cam
for n,p,t in [('north', (85,95,76),(-12,-17,15)),('south',(-125,-84,75),(-13,-20,15))]:
 cam.location=Vector(p);cam.rotation_euler=(Vector(t)-cam.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(out/(n+'.png'));bpy.ops.render.render(write_still=True)
# Separate detail: never place the unintegrated rim in the envelope as a merged game asset.
b.hide_render=True;c.hide_render=False;ground.hide_render=True
for m in (roof,mat('Raised measured top',(.11,.58,.36,1)),wall):c.data.materials.append(m)
for v in c.data.polygons:
 z=max(c.data.vertices[i].co.z for i in v.vertices)
 v.material_index=(1 if z>9.58 and v.normal.z>.9 else 2 if v.normal.z<.1 else 0)
lens.ortho_scale=51;cam.location=Vector((49,60,33));cam.rotation_euler=(Vector((1,16,8.6))-cam.location).to_track_quat('-Z','Y').to_euler()
sc.render.filepath=str(out/'rim.png');bpy.ops.render.render(write_still=True)

