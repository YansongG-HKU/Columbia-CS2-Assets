"""Independent Blender OBJ and game FBX readback with roof-ray comparison."""
import collections,json,sys,bpy,statistics
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
out,old_path=map(Path,sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=str(out/'Low-Library-lidar-crown-study.obj'),forward_axis='Y',up_axis='Z')
new,=[o for o in bpy.context.scene.objects if o.type=='MESH']
bpy.ops.import_scene.fbx(filepath=str(old_path),use_image_search=False)
old,=[o for o in bpy.context.scene.objects if o is not new and o.type=='MESH']
def get(o):
 assert not o.data.validate(verbose=True,clean_customdata=False)
 v=[o.matrix_world@v.co for v in o.data.vertices]
 o.data.calc_loop_triangles(); f=[list(p.vertices) for p in o.data.loop_triangles]
 return v,f,BVHTree.FromPolygons(v,f,all_triangles=True,epsilon=1e-7)
V,F,T=get(new); ov,of,ot=get(old)
edges=collections.defaultdict(list)
for f in F:
 for i,j in zip(f,f[1:]+f[:1]):edges[min(i,j),max(i,j)].append((i,j))
assert all(len(a)==2 and a[0]==a[1][::-1] for a in edges.values())
hits=[(i,j) for i,j in T.overlap(T) if i<j and set(F[i]).isdisjoint(F[j])]
assert not hits,hits[:10]
vol=sum(V[i].dot(V[j].cross(V[k])) for i,j,k in F)/6
assert vol>1000 and min(p.area for p in new.data.polygons)>1.e-5
res=[];ref=[];delta=[];top=max(v.z for v in V)
for line in (out/'held-roof-local.csv').read_text().splitlines():
 x,y,z=map(float,line.split(','))
 new_hit=T.ray_cast(Vector((x,y,100)),Vector((0,0,-1)))[0]
 old_hit=ot.ray_cast(Vector((x,y+9,100)),Vector((0,0,-1)))[0]
 assert new_hit is not None and old_hit is not None and new_hit.z>0 and old_hit.z>30
 # Align XY crown centers, and apex heights only: pure shape comparison, not absolute old game datum.
 a=new_hit.z; b=old_hit.z-43+top
 res.append(abs(a-z));ref.append(abs(b-z));delta.append(a-b)
def qq(a):return [statistics.median(a),statistics.quantiles(a,n=100,method='inclusive')[89],statistics.quantiles(a,n=100,method='inclusive')[94]]
result={'new_vertices':len(V),'new_triangles':len(F),'oriented_paired_edges':len(edges),'open_edges':0,'non_adjacent_intersections':len(hits),'volume_m3_synthetic_closed_region_not_building_volume':vol,'old_fbx_triangles':len(of),'n_hold_rays':len(res),'mesh_vs_hold_abs_p50_p90_p95':qq(res),'old_apex_aligned_vs_hold_abs_p50_p90_p95':qq(ref),'new_minus_old_apex_aligned_max_m':max(delta),'new_minus_old_apex_aligned_min_m':min(delta)}
(out/'mesh-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
def material(name,col):
 m=bpy.data.materials.new(name);m.diffuse_color=col;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=col;p.inputs['Roughness'].default_value=.69;return m
for o in [new,old]:
 o.data.materials.clear();o.data.materials.append(material('Crown QA',(.15,.38,.53,1) if o is new else (.50,.39,.26,1)))
 for p in o.data.polygons:p.material_index=0;p.use_smooth=False
old.location.y-=9;old.location.z-=37.
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=16;sc.cycles.use_denoising=False
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=540;sc.render.resolution_y=310;sc.render.resolution_percentage=100
sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA'
sc.world=bpy.data.worlds.new('Environment');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=1.
for e,rot in [(2.1,(.65,-.55,-.4)),(.85,(-.68,.25,1.0))]:
 s=bpy.data.lights.new('Sun','SUN');s.energy=e
 o=bpy.data.objects.new('Sun',s);sc.collection.objects.link(o);o.rotation_euler=rot
lens=bpy.data.cameras.new('Comparison');lens.type='ORTHO';lens.ortho_scale=36
cam=bpy.data.objects.new('Comparison',lens);sc.collection.objects.link(cam);sc.camera=cam
cam.location=Vector((43,-51,24));cam.rotation_euler=(Vector((0,0,1.5))-cam.location).to_track_quat('-Z','Y').to_euler()
# Use a common Z cut for the game comparison; do not show the untouched body in this crop.
bpy.context.view_layer.update()
import bmesh
bm=bmesh.new();bm.from_mesh(old.data)
bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00001,plane_co=(old.matrix_world.inverted()@Vector((0,0,0))),plane_no=old.matrix_world.to_3x3().transposed()@Vector((0,0,1)),clear_inner=True)
bm.to_mesh(old.data);bm.free()
for name,obj,other in [('previous',old,new),('survey',new,old)]:
 obj.hide_render=False;other.hide_render=True;sc.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
