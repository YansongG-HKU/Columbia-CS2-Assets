Warning: truncated output (original token count: 17875)
Total output lines: 2598

"""Build a diagnostic tangent-frame candidate only on two verified neutral-normal swatches."""
import argparse,hashlib,json,math,sys
from pathlib import Path
from io_scene_fbx import parse_fbx,encode_bin
from mathutils import Vector
PINS={'near':'3a42b31830eddc816b1c9bdefb7145f22dfef5b7292248fc499964e8493d9780','mid':'86dd8d09614ff7bdeb8b1acb788a9cbf64a77e985f53aa0dd74555bc8296078e'}
ANCHORS={(0.7842459082603455,0.44651466608047485),(0.7022064328193665,0.21046608686447144)}
COUNTS={'near':(2672,2580),'mid':(1832,1836)}
M=dict(zip(b'BCZYILFDRSifdlbc',('add_bool','add_char','add_int8','add_int16','add_int32',
'add_int64','add_float32','add_float64','add_bytes','add_string','add_int32_array','add_float32_array',
'add_float64_array','add_int64_array','add_bool_array','add_byte_array')))
def one(n,k):
    a=[c for c in n.elems if c.id==k]
    if len(a)!=1:raise ValueError(k)
    return a[0]
def get(n,k):return one(n,k).props[0]
def xyz(a,i,n=3):return Vector(a[i*n:(i+1)*n])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clone(n):
    a=encode_bin.FBXElem(n.id)
    for k,v in zip(n.props_type,n.props):getattr(a,M[k])(v)
    a.elems=[clone(q) for q in n.elems]
    return a
def snap(n):
    props=() if n.id in (b'Tangents',b'Binormals') else tuple(n.props)
    return n.id,bytes(n.props_type),props,tuple(snap(q) for q in n.elems)
def arrays(root):
    d=one(one(root,b'Objects'),b'Geometry')
    uv=one(d,b'LayerElementUV');no=one(d,b'LayerElementNormal')
    t=one(d,b'LayerElementTangent'); b=one(d,b'LayerElementBinormal')
    for node in (uv,no,t,b):
        if get(node,b'MappingInformationType')!=b'ByPolygonVertex':raise ValueError('Unexpected mapping')
    return get(uv,b'UV'),get(uv,b'UVIndex'),get(no,b'Normals'),get(no,b'NormalsIndex'),get(t,b'Tangents'),get(b,b'Binormals')
def errors(n,t,b):
    if not all(math.isfinite(v) for a in (n,t,b) for v in a):return True
    if any(abs(x.length-1)>1e-4 for x in (n,t,b)):return True
    return max(abs(n.dot(t)),abs(n.dot(b)),abs(t.dot(b)))>1e-4
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('stage',choices=PINS);p.add_argument('source',type=Path);p.add_argument('output',type=Path);p.add_argument('report',type=Path)
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if a.output.resolve()==a.report.resolve() or a.output.exists() or a.report.exists() or sha(a.source)!=PINS[a.stage]:
        raise ValueError('Use pinned source and fresh separate files')
    normmap=a.source.parent/'NA_UrisHall_6x9_Normal.png'
    if sha(normmap)!='8308fad811e5d8c454c4e55cbf2c292f1b239d1433cacfb1617ac270bc21c01b':
        raise ValueError('Use original fixed neutral-swatch Normal map')
    tree,v=parse_fbx.parse(str(a.source));u,ui,n,ni,t,b=arrays(tree)
    if not len(t)==len(b)==len(ui)*3 or len(ni)!=len(ui) or len(ui)%3:raise ValueError('Layer length differs')
    untouched=snap(tree); old_t=tuple(t);old_b=tuple(b); planned={};target=0
    for i in range(0,len(ui),3):
        s=[tuple(xyz(u,ui[j],2)) for j in range(i,i+3)]
        if not s[0] in ANCHORS or s[0]!=s[1] or s[0]!=s[2]:continue
        target+=1
        for j in range(i,i+3):
            N,T,B=xyz(n,ni[j]),xyz(t,j),xyz(b,j)
            if not errors(N,T,B):continue
            if abs(N.length-1)>1e-4:raise ValueError('Existing normal cannot be preserved')
            C=N.normalized()
            old_det=C.dot(T.cross(B))
            sign=1 if old_det>1e-4 else -1  # valid loops on these two swatches are left-handed
            if T.length>1e-7:
                tangent=T-C*C.dot(T)
            elif B.length>1e-7:
                tangent=B.cross(C)*sign
            else:
                tangent=Vector((0,0,0))
            if tangent.length<1e-7:
                X=min((Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1))),key=lambda x:abs(x.dot(C)))
                tangent=X-C*C.dot(X)
            tangent.normalize()
            bitangent=C.cross(tangent).normalized()*sign
            if errors(N,tangent,bitangent):raise ValueError('Frame still invalid')
            for k in range(3):
                t[3*j+k]=tangent[k];b[3*j+k]=bitangent[k]
            planned[j]=(tuple(tangent),tuple(bitangent))
    if (target,len(planned))!=COUNTS[a.stage]:raise ValueError((target,len(planned)))
    with encode_bin.FBXElem.enable_multithreading_cm():r=clone(tree)
    encode_bin.write(str(a.output),r,v)
    disk,dv=parse_fbx.parse(str(a.output))
    if dv!=v or snap(disk)!=untouched:raise ValueError('Non-tangent layers differ')
    _,_,_,_,tt,bb=arrays(disk)
    for j in range(len(ui)):
        real=(tuple(tt[3*j:3*j+3]),tuple(bb[3*j:3*j+3]))
        expected=planned.get(j,(old_t[3*j:3*j+3],old_b[3*j:3*j+3]))
        if real!=expected:raise ValueError('Unexpected corner difference')
    record={'stage':a.stage,'sha_before':PINS[a.stage],'sha_after':sha(a.output),'target_triangles':target,
          'changed_tangent_frames':len(planned),'other_attributes_and_untargeted_corners_exact':True,
          'scope':'FBX stored frame diagnostic; not proof CS2 uses these frames, no game validation'}
    a.report.write_text(json.dumps(record,indent=2)+'\n')
    print('TANGENT_CANDIDATE_PASS',record)
if __name__=='__main__':main()
