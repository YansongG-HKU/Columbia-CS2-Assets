"""Inspect coplanar overlap of full seed faces against all geometry, including separate vertices."""
from itertools import combinations
from pathlib import Path
import bpy, json, math, sys

def signed(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def clip(poly, tri):
    if signed(*tri)<0:tri=tri[::-1]
    for a,b in zip(tri,tri[1:]+tri[:1]):
        out=[]
        for u,v in zip(poly[-1:]+poly[:-1],poly):
            s,t=signed(a,b,u),signed(a,b,v)
            if (s>=0)!=(t>=0):
                q=s/(s-t)
                out.append(tuple(x+q*(y-x) for x,y in zip(u,v)))
            if t>=0:out.append(v)
        poly=out
        if len(poly)<3:return []
    return poly

def area(poly):
    return abs(sum(signed(poly[0],a,b) for a,b in zip(poly[1:],poly[2:])))*0.5 if len(poly)>2 else 0.

def uv_at(p,xy,uv):
    a,b,c=xy
    w=(signed(p,b,c),signed(a,p,c),signed(a,b,p)); d=signed(a,b,c)
    return tuple(sum(k*t[j] for k,t in zip(w,uv))/d for j in (0,1))

def measure(f,g):
    v,w=f['world'],g['world']; n,m=f['normal'],g['normal']; d=n.dot(m)
    if abs(d)<1-1e-6 or max(abs(n.dot(x-v[0])) for x in w)>1e-5:return None
    k=max(range(3),key=lambda i:abs(n[i]))
    a,b=([tuple(p[j] for j in range(3) if j!=k) for p in row] for row in (v,w))
    c=clip(a,b); result=area(c)/abs(n[k])
    if result<=1e-6:return None
    if f['uv'] is not None and g['uv'] is not None:
        duv=max(math.dist(uv_at(p,a,f['uv']),uv_at(p,b,g['uv'])) for p in c)
    else:
        duv=None
    return dict(first=f['id'],second=g['id'],first_area=area(a)/abs(n[k]),second_area=area(b)/abs(n[k]),area=result,same_facing=d>0,
                same_material=f['mat']==g['mat'],shared_vertex_indices=len(f['vertex_set'] & g['vertex_set']),max_uv_delta=duv,
                polygon_2d=c,projection_ignored_axis=k)

def main():
    fname,destination,ids=sys.argv[sys.argv.index('--')+1:]
    seed={int(x) for x in ids.split(',')}
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=fname,use_image_search=False)
    all_faces=[]
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH':continue
        data=ob.data; uvl=data.uv_layers.active
        for f in data.polygons:
            if len(f.vertices)!=3:continue
            xyz=[ob.matrix_world@data.vertices[i].co for i in f.vertices]
            norm=(xyz[1]-xyz[0]).cross(xyz[2]-xyz[0])
            if norm.length<1e-10:continue
            norm.normalize()
            bounds=[[op(x[i] for x in xyz) for i in range(3)] for op in (min,max)]
            mat=data.materials[f.material_index] if f.material_index<len(data.materials) else None
            all_faces.append(dict(id=[ob.name,f.index],vertex_set={(ob.name,i) for i in f.vertices},world=xyz,normal=norm,bounds=bounds,
               mat=mat.name if mat else None,uv=[tuple(uvl.data[i].uv) for i in f.loop_indices] if uvl else None))
    marked=[f for f in all_faces if f['id'][1] in seed]
    if len(marked)!=len(seed):raise RuntimeError("Missing or ambiguous seed faces")
    def intersects(a,b):
        return all(a[1][i]+1e-5>=b[0][i] and b[1][i]+1e-5>=a[0][i] for i in range(3))
    neighbors=[f for f in all_faces if any(intersects(f['bounds'],g['bounds']) for g in marked)]
    result=[]
    for f,g in combinations(neighbors,2):
        if not intersects(f['bounds'],g['bounds']):continue
        out=measure(f,g)
        if out:result.append(out)
    out=dict(seed_ids=sorted(seed),candidate_faces=len(neighbors),pairs=result,
        seed_faces=[dict(id=g['id'],world=[list(x) for x in g['world']],normal=list(g['normal']),material=g['mat'],uv=g['uv']) for g in marked])
    Path(destination).write_text(json.dumps(out,indent=2)+'\n')
    near=[r for r in result if r['first'][1] in seed and r['second'][1] in seed]
    print("LOCAL",len(neighbors),"pairs",len(result),"same",sum(r['same_facing'] for r in result),"zero_shared_same",
    sum(r['same_facing'] and r['shared_vertex_indices']==0 for r in result),"seed",[(r['first'][1],r['second'][1],round(r['area'],6),r['same_facing'],round(r['max_uv_delta'],6) if r['max_uv_delta'] is not None else None) for r in near])

if __name__=='__main__':main()
