"""Build a non-game, unregistered model of Lerner Hall's north glass/ramp assembly."""
import bpy,sys,math,json,collections,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
d=Path(sys.argv[sys.argv.index('--')+1]); d.mkdir(exist_ok=True,parents=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
SPAN=30.48; OFFSET=.9144
N=17; y0=-OFFSET
# Arup p25 Figs.5/6 relative trace: x = metres from grid 4 west; z=0 is a local glazing datum.
# End elevations of three illustrated north ramps differ by ~26–29 diagram pixels over ~491 px horizontal.
RISE=1.68
# Landing existence is documented by Hugh Dutton. Location and width are schematic only.
stations=(0.,8.90,10.45,19.83,21.38,SPAN)
step=RISE/(SPAN-(stations[2]-stations[1])-(stations[4]-stations[3]))
deck_z=(3.14,6.79,10.44)
DEPTH=2.60
def basez(x):
 return step*(min(x,stations[1])+max(0.,min(x,stations[3])-stations[2])+max(0.,x-stations[4]))
def glaze(x):return RISE*x/SPAN
def new_mat(n,col,r=.48,metal=0,glass=0,alpha=1):
 m=bpy.data.materials.new(n);m.diffuse_color=(*col,alpha);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF')
 p.inputs['Base Color'].default_value=(*col,1)
 p.inputs['Roughness'].default_value=r
 p.inputs['Metallic'].default_value=metal
 p.inputs['Transmission Weight'].default_value=glass
 p.inputs['IOR'].default_value=1.45
 return m
clear=new_mat('Point-fixed 22 mm clear laminated glass',(.67,.87,.87),.065,0,.96,.3)
translucent=new_mat('16 mm translucent walk glazing',(.29,.55,.52),.19,0,.50,.55)
steel=new_mat('Painted teal structural steel',(.078,.23,.24),.36,.44)
steel_dark=new_mat('Lower inside steel',(.065,.15,.17),.39,.37)
hardware=new_mat('Point bolts and stainless steel arms',(.44,.55,.56),.25,.72)
concrete=new_mat('Neutral local reference slab (render only)',(.27,.24,.2),.7,0)
def group(n):
 c=bpy.data.collections.new(n);bpy.context.scene.collection.children.link(c);return c
glass_c=group('01 North point-supported glazing')
deck_c=group('02 Three translucent ramps with two schematic landings each')
truss_c=group('03 Primary and secondary structure (study)')
bolt_c=group('04 Point fixings, no mullions')
context=group('00 Context (not exported)')
objects=[]
def move(o,c):
 for old in list(o.users_collection):old.objects.unlink(o)
 c.objects.link(o)
def mesh(n,v,faces,m,c,uv_local=None,export=True):
 # Blender ensures linked normals; make one closed connected mesh per panel or ramp.
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],faces);me.update(calc_edges=True)
 assert not me.validate()
 o=bpy.data.objects.new(n,me);c.objects.link(o);o.data.materials.append(m)
 if uv_local:
  uv=me.uv_layers.new(name='UV0')
  for p in me.polygons:
   for i in p.loop_indices:
    uv.data[i].uv=uv_local(v[me.loops[i].vertex_index])
 if export:objects.append(o)
 return o
closed_faces=((0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7))
# No mullions, only separated panel seams. Lower vision zone+spandrel repeated three times and upper view zone.
rows=[0.]
for feet in (8,4,8,4,8,4,10):rows.append(rows[-1]+feet*.3048)
BAY_X=[SPAN*i/N for i in range(N+1)]
for i,(a,b) in enumerate(zip(BAY_X,BAY_X[1:])):
 for j,(q,r) in enumerate(zip(rows,rows[1:])):
  u=a+.003;v=b-.003;l=q+.003;h=r-.003; y=-.011;t=.011
  verts=[(u,y,l+glaze(u)),(v,y,l+glaze(v)),(v,t,l+glaze(v)),(u,t,l+glaze(u)),
         (u,y,h+glaze(u)),(v,y,h+glaze(v)),(v,t,h+glaze(v)),(u,t,h+glaze(u))]
  mesh('Pane_%02d_%02d'%(i+1,j+1),verts,closed_faces,clear,glass_c,lambda p:((p[0]-u)/(v-u),(p[2]-glaze(p[0])-l)/(h-l)))
# Glass decks have uninterrupted group topology, with profiles split exactly at landings.
for j,z in enumerate(deck_z,1):
 V=[]
 for x in stations:
  h=z+basez(x)
  V += [(x,y0-DEPTH,h-.016),(x,y0,h-.016),(x,y0,h),(x,y0-DEPTH,h)]
 F=[(3,2,1,0)]
 for k in range(len(stations)-1):
  for a in range(4):F.append((4*k+a,4*k+(a+1)%4,4*(k+1)+(a+1)%4,4*(k+1)+a))
 off=4*(len(stations)-1);F+=[(off,off+1,off+2,off+3)]
 mesh('Ramp_north_%d_with_2_level_landings'%j,V,F,translucent,deck_c,lambda p:(p[0]/SPAN,(p[1]-(y0-DEPTH))/DEPTH))
# Tube geometry merged by material so thin physical members do not create separate draw objects.
rod=collections.defaultdict(lambda:[[],[]])
def bar(A,B,r,k,segments=8):
 a,b=Vector(A),Vector(B)
 delta=b-a;assert delta.length>1e-5
 f=delta.normalized();u=f.cross(Vector((0,0,1)))
 if u.length<1e-5:u=f.cross(Vector((0,1,0)))
 u.normalize();v=f.cross(u)
 vv,ff=rod[k];start=len(vv)
 for base in (a,b):
  for i in range(segments):
   a0=2*math.pi*i/segments;vv.append(tuple(base+r*(u*math.cos(a0)+v*math.sin(a0))))
 ff.append(tuple(start+i for i in range(segments-1,-1,-1)))
 ff.append(tuple(start+segments+i for i in range(segments)))
 for i in range(segments):
  j=(i+1)%segments;ff.append((start+i,start+j,start+segments+j,start+segments+i))
for z in deck_z:
 for x,y in zip(stations,stations[1:]):
  for Y in (y0-.05,y0-DEPTH+.10):
   bar((x,Y,z+basez(x)-.09),(y,Y,z+basez(y)-.09),.057,'ramp_frame')
   bar((x,Y,z+basez(x)+1.02),(y,Y,z+basez(y)+1.02),.021,'handrails',6)
 for i in range(32):
  a=SPAN*i/32.;b=SPAN*(i+1)/32.; za=z+basez(a);zb=z+basez(b)
  for Y in (y0-.05,y0-DEPTH+.10):bar((a,Y,za-.01),(a,Y,za+1.02),.018,'handrails',6)
  # Diagonally triangulated ramp grillage, no heavy rectangular panel framing.
  yy=(y0-.04,y0-DEPTH+.05) if i%2 else (y0-DEPTH+.05,y0-.04)
  bar((a,yy[0],za-.12),(b,yy[1],zb-.40),.033,'ramp_frame',6)
  bar((a,yy[1],za-.40),(b,yy[0],zb-.12),.026,'ramp_frame',6)
# Inclined façade truss, one lower and one upper chord; tension and compression distinguished.
section=[SPAN*i/6 for i in range(7)]
for z in (2.88,11.06):bar((0,y0,z),(SPAN,y0,z+RISE),.097,'ift_pipe',10)
for k,x in enumerate(section):
 if k not in (0,len(section)-1):
  bar((x,y0,2.88+glaze(x)),(x,y0,11.06+glaze(x)),.054,'ift_pipe',10)
 if k+1<len(section):
  q=section[k+1]
  za,zb=(2.88,11.06) if k%2 else (11.06,2.88)
  bar((x,y0,za+glaze(x)),(q,y0,zb+glaze(q)),.097 if k%3 else .038,'ift_pipe',10)
# Offset near the back edge of translucent ramps, not a transverse full hub fit.
rt_y=y0-DEPTH-.16
for z in (14.85,16.2):bar((0,rt_y,z),(SPAN,rt_y,z+RISE),.105,'rtt',10)
for i in range(12):
 a=SPAN*i/12.;b=SPAN*(i+1)/12.
 za,zb=(14.85,16.2) if i%2 else (16.2,14.85)
 bar((a,rt_y,za+glaze(a)),(b,rt_y,zb+glaze(b)),.051,'rtt',8)
for x in section[1:-1]:
 for z in deck_z:
  bar((x,rt_y,14.86+glaze(x)),(x,y0-DEPTH+.04,z+basez(x)-.08),.021,'rtt',6)
# Local paired attach arms at every other joint, no continuous bars along the glass face.
for z in deck_z:
 for i,x in enumerate(BAY_X[1:-1],1):
  if i%2==0:continue
  for east in (-1,1):
   for up in (-1,1):
    xn=x+.24*east; zh=z+glaze(x)+.27*up
    bar((x-.09*east,y0-.04,z+basez(x)-.08*up),(xn,-.035,zh),.019,'attachment_arms',6)
    bar((xn,-.034,zh),(xn,.020,zh),.046,'point_bolts',8)
for k,(v,f) in sorted(rod.items()):
 mat=hardware if k in ('attachment_arms','point_bolts') else steel_dark if k=='ramp_frame' else steel
 c=bolt_c if mat==hardware else truss_c
 mesh(k,v,f,mat,c)
# Audit the build: outward facing caps, edge closure and independent ramp plan continuity.
audit={}
for o in objects:
 m=o.data;E=collections.defaultdict(list);m.calc_loop_triangles()
 for p in m.polygons:
  v=tuple(p.vertices);assert p.area>1e-8
  for a,b in zip(v,v[1:]+v[:1]):E[tuple(sorted((a,b)))].append((a,b))
 vol=sum(m.vertices[t.vertices[0]].co.dot(m.vertices[t.vertices[1]].co.cross(m.vertices[t.vertices[2]].co)) for t in m.loop_triangles)/6
 assert all(len(es)==2 and es[0]==es[1][::-1] for es in E.values()) and vol>0,(o.name,vol)
 k=o.users_collection[0].name
 info=audit.setdefault(k,{'objects':0,'vertices':0,'triangles':0,'oriented_edges':0})
 for k,n in zip(('objects','vertices','triangles','oriented_edges'),(1,len(m.vertices),len(m.loop_triangles),len(E))):info[k]+=n
 if o.name.startswith(('Ramp_','Pane_')):
  vv=[x.co for x in m.vertices];ff=[tuple(t.vertices) for t in m.loop_triangles]
  tree=BVHTree.FromPolygons(vv,ff,all_triangles=True)
  assert not [(a,b) for a,b in tree.overlap(tree) if a<b and set(ff[a]).isdisjoint(ff[b])],o.name
assert len(glass_c.objects)==119 and len(deck_c.objects)==3
assert all(abs(basez(stations[i])-basez(stations[i+1]))<1e-7 for i in (1,3)) and abs(basez(SPAN)-RISE)<1e-7
rec=dict(status='Standalone study only; no building frame registration, no local geometry placement, no Editor',
 span_bearing_grids_m=SPAN,schematic_rise_m=RISE,rise_not_site_slope=True,offset_m=OFFSET,
 glazing_parameter_thickness_m=.022, ramp_parameter_thickness_m=.016,vertical_band_heights_ft=[8,4,8,4,8,4,10],
 front_ramp_width_m_provisional=DEPTH,landing_station_chain_m=list(stations), bay_count_from_schematic=N,
 local_x='West grid 4 to east grid 7',local_y='North positive, glass plane y=0',local_z='Arbitrary lower west glazing datum; no NAVD88 offset',
 audit=audit,only_joint_components_may_overlap=True)
(d/'hub-audit.json').write_text(json.dumps(rec,indent=2)+'\n')
# Generate a mesh-only interoperable review model; no original source data or building files changed.
bpy.ops.object.select_all(action='DESELECT')
for o in objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(d/'Lerner-north-hub-study.glb'),export_format='GLB',use_selection=True,export_materials='EXPORT',export_yup=True)
print('STUDY_QA',json.dumps(rec),flush=True)
# Neutral stage and same-scale outside/inside diagrams; standalone glazing is visible without masonry.
bpy.ops.mesh.primitive_plane_add(size=80,location=(15,-2,-.07))
floor=bpy.context.object;floor.name='Arbitrary stage (not actual grade)';move(floor,context);floor.data.materials.append(concrete)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.use_denoising=False;sc.cycles.samples=24
sc.cycles.max_bounces=8;sc.cycles.transmission_bounces=5
sc.render.threads_mode='FIXED';sc.render.threads=2;sc.render.resolution_x=1040;sc.render.resolution_y=650
sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
sc.world=bpy.data.worlds.new('Studio light');sc.world.use_nodes=True
sc.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.61,.69,.7,1)
sc.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.85
def sun(n,e,r):
 s=bpy.data.lights.new(n,'SUN');s.energy=e;s.angle=.18
 o=bpy.data.objects.new(n,s);sc.collection.objects.link(o);o.rotation_euler=r
sun('Primary',2.2,(.45,-.42,-.72));sun('Secondary',.7,(-.6,.36,.74))
l=bpy.data.cameras.new('Study camera');l.type='ORTHO';l.ortho_scale=39
c=bpy.data.objects.new('Study camera',l);sc.collection.objects.link(c);sc.camera=c
def render(n,v,t):
 c.location=Vector(v); c.rotation_euler=(Vector(t)-c.location).to_track_quat('-Z','Y').to_euler()
 sc.render.filepath=str(d/(n+'.png'));bpy.ops.render.render(write_still=True)
render('glass-oblique',(33,54,24),(SPAN/2,-1.6,8))
for o in glass_c.objects:o.hide_render=True
l.ortho_scale=39
render('ramps-exposed',(5,44,29),(SPAN/2,-1.7,8.5))
