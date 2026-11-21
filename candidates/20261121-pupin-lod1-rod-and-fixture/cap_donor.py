"""Make a separate fixed-cap donor plan only after loss report shows the west cap misses a post."""
from pathlib import Path
import sys,json,collections
D=Path(sys.argv[-1]).resolve()
# Reuse the same exact import and raw UV/normal extraction, but no donor search.
source=(D/'donor.py').read_text()
exec(source[:source.index('P0=')])
k,k1,k0=51424,33120,23369
ix,idx,oldix=nC[k],cC[k1],oC[k0]
assert list(map(len,(ix,idx,oldix)))==[20,20,6]
assert [len(nPF[k]),len(cPF[k1]),len(oPF[k0])]==[36,36,8]
err=max(max(min((nV[i]-cV[j]).length for j in idx) for i in ix),max(min((cV[i]-nV[j]).length for j in ix) for i in idx))
assert err<5e-6
old_face_keys={tuple(sorted(oF[j])) for j in oPF[k0]}
rawold,_=parse_fbx.parse(str(old))
oldgg,=[g for q in rawold.elems if q.id==b'Objects' for g in q.elems if g.id==b'Geometry']
a=val(oldgg,b'PolygonVertexIndex'); ff=[tuple(i if i>=0 else -1-i for i in a[j:j+3]) for j in range(0,len(a),3)]
drop_ids=[j for j,x in enumerate(ff) if tuple(sorted(x)) in old_face_keys]
assert len(drop_ids)==8 and all(set(ff[i]).issubset(oldix) for i in drop_ids)
comp=set(ix); oi={v:j for j,v in enumerate(ix)}; F=[]; Us=[]; Ns=[]; Ed=collections.defaultdict(list)
for j in nPF[k]:
 q=nf[j];assert set(q)<=comp
 F.append([oi[i] for i in q])
 Us.append([list(u[2*ui[3*j+b]:2*ui[3*j+b]+2]) for b in range(3)])
 Ns.append([list(n[ni[3*j+b]*3:ni[3*j+b]*3+3]) for b in range(3)])
 for a,b in zip(q,q[1:]+q[:1]):Ed[min(a,b),max(a,b)].append((a,b))
assert len(Ed)==54 and all(len(t)==2 and t[0]==t[1][::-1] for t in Ed.values())
assert all(-.001<x<1.001 for f in Us for a in f for x in a)
assert all(abs(Vector(a).length-1)<.001 for f in Ns for a in f)
data=json.loads((D/'donor-plan.json').read_text()); assert len(data['components'])==50
cap={'family':'west_fixture_cap','old_vertex_ids':oldix,'old_faces':drop_ids,'world_vertices':[list(nV[i]) for i in ix],
     'donor_raw_vertices':[nv[i] for i in ix],'donor_triangles':F,'donor_uv_corners':Us,'donor_normals_corners':Ns,
     'near_component_key':k,'main_old_source_component_key':k1,'donor_max_hausdorff_from_archival_m':err}
data['components'].append(cap)
(D/'donor-plan-with-cap.json').write_text(json.dumps(data,indent=2)+'\n')
print('Exact replacement',drop_ids,'two-source Hausdorff m',err)
