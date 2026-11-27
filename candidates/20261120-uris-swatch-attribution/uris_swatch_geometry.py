import bpy,sys,collections,json,math
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
blend,near,mid,out=map(lambda p:Path(p).resolve(),args)
anchors={'A':(0.7842459082603455,0.44651466608047485),'B':(0.7022064328193665,0.21046608686447144)}
def vec_sum(u):return sum((Vector(x) for x in u),Vector((0,0)))/len(u)
def collect(o,donors=False):
    mesh=o.data;mesh.calc_loop_triangles();uvchan=mesh.uv_layers.active.data
    access=lambda ps:[tuple(uvchan[i].uv) for i in ps]
    verts={i:o.matrix_world@v.co for i,v in enumerate(mesh.vertices)}
    hit={k:[] for k in anchors}
    for f in mesh.loop_triangles:
        u=access(f.loops)
        if u[0]!=u[1] or u[0]!=u[2]:continue
        k=next((k for k,a in anchors.items() if a==u[0]),None)
        if k is None:continue
        p=[verts[i] for i in f.vertices];n=(p[1]-p[0]).cross(p[2]-p[0])
        size=[max(v[i] for v in p)-min(v[i] for v in p) for i in range(3)]
        # Triangle-box minimum positive interval is not a material label.
        hit[k].append((tuple(f.vertices),n.length/2,tuple(n.normalized()),size,
                       sum((p[0],p[1],p[2]),Vector())/3))
    result={}
    for k,rows in hit.items():
        used=set(i for f,*_ in rows for i in f)
        coords=[verts[i] for i in used]
        adj=collections.defaultdict(set)
        for j,(f,*_) in enumerate(rows):
            for a,b in zip(f,f[1:]+f[:1]):adj[tuple(sorted((a,b)))].add(j)
        nearf=collections.defaultdict(set)
        for shared in adj.values():
            for i in shared:nearf[i].update(shared-{i})
        remaining=set(range(len(rows)));cc=[]
        while remaining:
            todo=[remaining.pop()];seen=todo.copy()
            while todo:
                i=todo.pop()
                for j in nearf[i]&remaining:
                    remaining.remove(j);todo.append(j);seen.append(j)
            area=sum(rows[j][1] for j in seen)
            cc.append((len(seen),area))
        row={'faces':len(rows),'area_m2':sum(s for _,s,*_ in rows),
             'bounds':[[op(v[i] for v in coords) for i in range(3)] for op in (min,max)] if coords else None,
             'edge_connected_components':len(cc),'largest_components':sorted(cc,key=lambda x:x[1],reverse=True)[:10],
             'normal_bands':dict(collections.Counter(('z+' if n[2]>.95 else 'z-' if n[2]<-.95 else 'lateral') for _,_,n,*_ in rows)),
             'thin_surface_count_min_positive_aabb_le_0p20m':sum(min((x for x in s if x>1e-4),default=1000)<=.20 for _,_,_,s,_ in rows)}
        if donors:
            anchors_hit=[]
            for f in mesh.polygons:
                uv=access(f.loop_indices)
                if len(set(uv))<3:continue
                if (vec_sum(uv)-Vector(anchors[k])).length>1e-7:continue
                xyz=[list(verts[i]) for i in f.vertices]
                anchors_hit.append({'polygon':f.index,'coordinates':xyz,'area_m2':f.area,
                   'material_index':f.material_index,'shared_collapsed_vertices':len(set(f.vertices)&used),
                   'uv_corners':uv})
            row['noncollapsed_source_ngon_centroids_matching']=anchors_hit
        result[k]=row
    return result

def load(f):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(f),use_image_search=False)
    o,=[o for o in bpy.context.scene.objects if o.type=='MESH']
    return collect(o)
result={'near_fbx':load(near),'mid_fbx':load(mid)}
bpy.ops.wm.open_mainfile(filepath=str(blend),use_scripts=False)
result['source_near']=collect(bpy.data.objects['NA_UrisHall_6x9_Base'],True)
result['source_mid']=collect(bpy.data.objects['NA_UrisHall_6x9_LOD1_Base'],True)
out.write_text(json.dumps(result,indent=2)+'\n')
for group,r in result.items():
 for k,row in r.items():
  print(group,k,row['faces'],round(row['area_m2'],4),row['edge_connected_components'],row['normal_bands'],row['bounds'],[(x['polygon'],x['area_m2']) for x in row.get('noncollapsed_source_ngon_centroids_matching',[])])
