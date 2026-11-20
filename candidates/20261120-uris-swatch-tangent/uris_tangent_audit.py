"""Audit lengths, orthogonality and handedness on original raw FBX tangent frames."""
import hashlib,json,math,sys
from collections import Counter
from pathlib import Path
from io_scene_fbx import parse_fbx
from mathutils import Vector
def one(n,k):
    a=[c for c in n.elems if c.id==k]
    if len(a)!=1:raise ValueError(k)
    return a[0]
def get(n,k):return one(n,k).props[0]
def lvec(a,i,n):return Vector(a[i*n:(i+1)*n])
def compute(path):
    tree,_=parse_fbx.parse(str(path));m=one(one(tree,b'Objects'),b'Geometry')
    U=one(m,b'LayerElementUV'); remap=get(U,b'UVIndex');u=get(U,b'UV')
    N=one(m,b'LayerElementNormal');ni=get(N,b'NormalsIndex'); nn=get(N,b'Normals')
    T=get(one(m,b'LayerElementTangent'),b'Tangents');B=get(one(m,b'LayerElementBinormal'),b'Binormals')
    if not len(T)==len(B)==3*len(remap) or not len(ni)==len(remap):raise ValueError('unexpected')
    anchors={(0.7842459082603455,0.44651466608047485),(0.7022064328193665,0.21046608686447144)}
    c={k:Counter() for k in ('hotspots','residual','nonpoint')}
    for o in range(0,len(remap),3):
        xy={tuple(lvec(u,remap[i],2)) for i in range(o,o+3)}
        label=('hotspots' if next(iter(xy)) in anchors else 'residual') if len(xy)==1 else 'nonpoint'
        c[label]['faces']+=1
        for j in range(o,o+3):
           n,t,b=lvec(nn,ni[j],3),lvec(T,j,3),lvec(B,j,3)
           c[label]['loops']+=1
           if not all(math.isfinite(v) for a in (n,t,b) for v in a):
               c[label]['non_finite']+=1;continue
           if t.length<1e-7 or b.length<1e-7:
               c[label]['zero_t_or_b']+=1;continue
           if any(abs(x.length-1)>1e-4 for x in (n,t,b)):c[label]['not_unit']+=1
           if max(abs(n.dot(t)),abs(n.dot(b)),abs(t.dot(b)))>1e-4:c[label]['nonorthogonal']+=1
           v=n.dot(t.cross(b))
           if v>1e-4:c[label]['right_handed']+=1
           elif v< -1e-4:c[label]['left_handed']+=1
           else:c[label]['no_handedness']+=1
    print(path.name,c)
    return {'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'classes':c}
*paths,out=map(Path,sys.argv[sys.argv.index('--')+1:])
out.write_text(json.dumps({p.name:compute(p) for p in paths},indent=2)+'\n')
