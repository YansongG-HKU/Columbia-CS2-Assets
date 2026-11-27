"""Render two fixed-angle local views of exact FBX readbacks."""
from pathlib import Path
import bpy,sys,math,json
from mathutils import Vector
D=Path(sys.argv[-1]).resolve(); B='NA_PupinHall_8x3_LOD1.fbx'; src=D/'input/import-assets/PupinHall'
bpy.ops.wm.read_factory_settings(use_empty=True)
def load(p):
 old=set(bpy.context.scene.objects)
 bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
 o,=[o for o in bpy.context.scene.objects if o.type=='MESH' and o not in old]
 return o
o0=load(src/B);o1=load(D/'trial'/B)
plan=json.loads((D/'donor-plan-with-cap.json').read_text())['components']
dropped={tuple(sorted(r['old_vertex_ids'])) for r in plan[:-1]}
cap=set(plan[-1]['old_vertex_ids'])
K0={p.index for p in o0.data.polygons if tuple(sorted(p.vertices)) in dropped or set(p.vertices)&cap}
F=o0.data.polygons; target=range(36586,37286)
old_omit=dropped
def mat(n,rgb):
 m=bpy.data.materials.new(n);m.diffuse_color=rgb;m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=rgb;p.inputs['Roughness'].default_value=.70
 return m
plain=mat('Context geometry',(.46,.49,.50,1)); changed=mat('Eight component check',(.05,.38,.44,1)); old=mat('Existing collapsed strips',(.78,.36,.15,1))
for o,k in [(o0,K0),(o1,set(target))]:
 o.data.materials.clear();o.data.materials.append(plain);o.data.materials.append(old if o==o0 else changed)
 for p in o.data.polygons:p.material_index=int(p.index in k)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=12;sc.cycles.device='CPU';sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=740;sc.render.resolution_y=460;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Neutral');sc.world.use_nodes=True;sc.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.82
for e,rot in [(2.1,(.6,-.45,-.72)),(.8,(-.50,.31,.46))]:
 l=bpy.data.lights.new('Directional','SUN');l.energy=e;ob=bpy.data.objects.new('Directional',l);sc.collection.objects.link(ob);ob.rotation_euler=rot
C=bpy.data.cameras.new('Frozen view');C.type='ORTHO';C.ortho_scale=1.7
c=bpy.data.objects.new('Frozen view',C);sc.collection.objects.link(c);sc.camera=c
for area,target0,off,scale in [('roof',(24,-9.66,43.22),(6.0,-11.0,2.2),8.9),('entry',(-4.6,-11.20,3.19),(-3.7,-6.9,1.15),1.65)]:
 aim=Vector(target0);c.location=aim+Vector(off);c.rotation_euler=(aim-c.location).to_track_quat('-Z','Y').to_euler();C.ortho_scale=scale
 for tag,yes,no in [('before',o0,o1),('after',o1,o0)]:
  yes.hide_render=False;no.hide_render=True;sc.render.filepath=str(D/(area+'-'+tag+'.png'));bpy.ops.render.render(write_still=True)
