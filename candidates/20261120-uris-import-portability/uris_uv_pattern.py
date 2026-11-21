import bpy, sys,collections,json,math
from pathlib import Path
name,out=sys.argv[sys.argv.index('--')+1:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(Path(name).resolve()),use_image_search=False)
o,=[o for o in bpy.context.scene.objects if o.type=='MESH']; m=o.data; m.calc_loop_triangles()
uv=m.uv_layers.active.data
hist=collections.Counter(); keys=collections.Counter(); extents=collections.Counter()
for t in m.loop_triangles:
 u=[tuple(uv[i].uv) for i in t.loops]
 a,b,c=u; d=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 if abs(d)>1e-10: continue
 counts=len(set(u)); label={1:'exact_one_uv',2:'exact_two_uv',3:'three_near_collinear_uv'}[counts]
 hist[label]+=1
 keys[(label,tuple(sorted(set(u))))]+=1
 coords=[o.matrix_world@m.vertices[i].co for i in t.vertices]
 sizes=[max(p[i] for p in coords)-min(p[i] for p in coords) for i in range(3)]
 extents[(label,str(sizes.index(min(sizes))))]+=1
report={'file':Path(name).name,'counts':hist,'largest_groups':[(k[0],k[1],n) for k,n in keys.most_common(12)],'total_uv_patterns':len(keys),
 'min_extent_axis':[(k[0],k[1],v) for k,v in extents.items()]}
Path(out).write_text(json.dumps(report,indent=2)+'\n')
print(name,dict(hist),len(keys),keys.most_common(3))
