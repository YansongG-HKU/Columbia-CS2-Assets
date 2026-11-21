"""Locate major campus-facing facade planes in Lerner Hall's accepted FBXs."""
import collections
import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

def inspect(p):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(p),use_image_search=False)
    ob, = (o for o in bpy.data.objects if o.type=='MESH')
    ob.data.calc_loop_triangles()
    vectors=[ob.matrix_world@v.co for v in ob.data.vertices]
    records=collections.defaultdict(list)
    for tri in ob.data.loop_triangles:
        a,b,c=(vectors[v] for v in tri.vertices)
        cross=(b-a).cross(c-a)
        area=cross.length*.5
        if area < 0.03:
            continue
        direction=cross.normalized()
        if abs(direction.y) < .99999:
            continue
        if min(a.z,b.z,c.z)<0.4:
            continue
        y=round((a.y+b.y+c.y)/3,2)
        records[(y,direction.y<0)].append((area, [a,b,c]))
    planes=[]
    for (y, front), faces in records.items():
        total=sum(a for a,_ in faces)
        if total < 5:
            continue
        vertices=[pos for _,tri in faces for pos in tri]
        bounds=[[round(f(v[i] for v in vertices),4) for i in range(3)] for f in (min,max)]
        planes.append({'plane_y_m':y,'campus_facing':front,'triangles':len(faces),
                       'world_bounds_m':bounds,'total_triangle_area_m2':round(total,3)})
    return sorted(planes,key=lambda v:-v['total_triangle_area_m2'])

candidate, out=map(lambda p:Path(p).resolve(),sys.argv[sys.argv.index('--')+1:])
records={}
for p in sorted(candidate.glob('*.fbx')):
    if '_LOD2' not in p.name:
        records[p.name]=inspect(p)
out.write_text(json.dumps(records,indent=2)+'\n')
for k,v in records.items():
    print(k,len(v), json.dumps(v[:5]))
