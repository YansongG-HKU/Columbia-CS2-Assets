"""Render the three exact restored components isolated from the building, with frozen per-row camera."""
from pathlib import Path
import sys,bpy,math,json
from mathutils import Vector
D=Path(sys.argv[-1]).resolve()
L=json.loads((D/'donor-plan.json').read_text())['components']
raw=json.loads((D/'world-pairs.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.device='CPU';S.cycles.samples=7;S.cycles.use_denoising=False
S.render.threads_mode='FIXED';S.render.threads=2;S.render.film_transparent=True;S.render.image_settings.color_mode='RGBA'
S.render.resolution_x=440;S.render.resolution_y=245;S.render.resolution_percentage=100
S.world=bpy.data.worlds.new('Mapless');S.world.use_nodes=True;S.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.75
for e,rot in [(2.6,(.6,-.45,-.72)),(1.15,(-.50,.31,.46)),(.8,(.3,.5,1.57))]:
 l=bpy.data.lights.new('Directional','SUN');l.energy=e;ob=bpy.data.objects.new('Directional',l);S.collection.objects.link(ob);ob.rotation_euler=rot
camera=bpy.data.cameras.new('same angle');camera.type='ORTHO';cam=bpy.data.objects.new('same angle',camera);S.collection.objects.link(cam);S.camera=cam
for i,(old,part) in enumerate(zip(raw,L)):
 for j,(tag,verts,ff,rgb) in enumerate([('old',old['readback_world_xyz'],[(0,1,2)],(.76,.20,.075,1)),('new',part['world_vertices'],part['donor_triangles'],(.06,.45,.55,1))]):
  m=bpy.data.meshes.new(tag);m.from_pydata(verts,[],ff);m.update()
  o=bpy.data.objects.new(tag,m);S.collection.objects.link(o)
  mat=bpy.data.materials.new(tag);mat.use_nodes=True
  base=mat.node_tree.nodes.get('Principled BSDF');base.inputs['Base Color'].default_value=rgb;base.inputs['Roughness'].default_value=.65
  m.materials.append(mat)
  A=[tuple(map(fn,zip(*part['world_vertices']))) for fn in (min,max)]; aim=Vector(A[0]).lerp(Vector(A[1]),.5)
  camera.ortho_scale=6.12 if i==1 else 9.95
  cam.location=aim+Vector((8.,-16.,4.));cam.rotation_euler=(aim-cam.location).to_track_quat('-Z','Y').to_euler()
  S.render.filepath=str(D/f'{i}-{tag}.png');bpy.ops.render.render(write_still=True)
  bpy.data.objects.remove(o,do_unlink=True);bpy.data.meshes.remove(m)
