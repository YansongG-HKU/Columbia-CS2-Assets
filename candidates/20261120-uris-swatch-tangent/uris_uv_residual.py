"""Rank and attribute unresolved exact single-point Uris UV triangles by true area."""
from collections import defaultdict
import json, math,sys
from pathlib import Path
import bpy
from mathutils import Vector
fn,out=map(lambda x:Path(x).resolve(),sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(fn),use_scripts=False)
excluded={(0.7842459082603455,0.44651466608047485),(0.7022064328193665,0.21046608686447144)}
results={}
for lod,offset in [('near',0),('mid',130)]:
    obj=bpy.data.objects['NA_UrisHall_6x9_'+('LOD1_' if lod=='mid' else '')+'Base']
    m=obj.data;m.calc_loop_triangles()
    layer=m.uv_layers.active.data
    uv=lambda loops:[tuple(layer[i].uv) for i in loops]
    coords=lambda seq:[list(obj.matrix_world@m.vertices[i].co-Vector((offset,0,0))) for i in seq]
    groups=defaultdict(list); centroids=defaultdict(list)
    def add_centroid(p):
        u=uv(p.loop_indices)
        if len(set(u))<3:return
        c=sum((Vector(x) for x in u),Vector((0,0)))/len(u)
        centroids[tuple(c)].append(p.index)
    for p in m.polygons:add_centroid(p)
    for f in m.loop_triangles:
        u=uv(f.loops)
        if len(set(u))!=1 or u[0] in excluded:continue
        pts=[Vector(x) for x in coords(f.vertices)]
        n=(pts[1]-pts[0]).cross(pts[2]-pts[0])
        sizes=[max(p[i] for p in pts)-min(p[i] for p in pts) for i in range(3)]
        d=min((x for x in sizes if x>1e-4),default=0)
        groups[u[0]].append(dict(poly=f.polygon_index,vertices=list(f.vertices),coords=[list(x) for x in pts],area=n.length/2,normal=list(n.normalized()),min_projected_width=d))
    records=[]
    for k,faces in groups.items():
        hits=centroids.get(k,[])
        ds=[]
        for i in hits:
            p=m.polygons[i]; ids=set(p.vertices)
            dst=[x['poly'] for x in faces if ids.intersection(x['vertices'])]
            ds.append({'source_polygon':i,'adjacent_triangles':len(dst),'area_m2':p.area,'uv':uv(p.loop_indices),'coords':coords(p.vertices)})
        records.append(dict(uv=k,count=len(faces),area_m2=sum(x['area'] for x in faces),
            all_thin=all(x['min_projected_width']<=.2 for x in faces),
            donors=ds,samples=sorted(faces,key=lambda r:r['area'],reverse=True)[:3]))
    records.sort(key=lambda r:r['area_m2'],reverse=True)
    missing=sum(r['count'] for r in records if not r['donors'])
    print(lod,'unresolved',sum(r['count'] for r in records),'groups',len(records),'without_exact_donor',missing)
    for r in records[:8]:print(r['uv'],r['count'],round(r['area_m2'],4),r['all_thin'],[(d['source_polygon'],d['adjacent_triangles']) for d in r['donors']],[(s['poly'],[round(x,4) for x in s['normal']],round(s['area'],4)) for s in r['samples']])
    results[lod]=records
out.write_text(json.dumps(results,indent=2)+'\n')
