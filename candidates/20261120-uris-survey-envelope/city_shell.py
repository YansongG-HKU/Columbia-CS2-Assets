"""Derive original and re-elevated Uris shell from official 2014 planimetric CityGML."""
import collections,ctypes as ct,json,hashlib,sys,xml.etree.ElementTree as XML
from pathlib import Path
import numpy as np
from pyproj import Transformer
from osgeo import ogr
ogr.UseExceptions()
source,points,dest=map(Path,sys.argv[1:]);dest.mkdir(exist_ok=True)
local=np.array([587623.1421979353,4518097.006500896]); z0=46.46
split_tolerance=.002
def flat(seq):
    a=np.asarray(seq)
    return float(np.sum(a[:,0]*np.roll(a[:,1],-1)-a[:,1]*np.roll(a[:,0],-1))*.5)
def ring(r):
    a=ogr.Geometry(ogr.wkbLinearRing)
    for x,y in r:a.AddPoint_2D(float(x),float(y))
    a.CloseRings();return a
def polygon(p):
    q=ogr.Geometry(ogr.wkbPolygon);q.AddGeometry(ring(p));return q

L=ct.CDLL('libgeos_c.so.1')
def fun(name,types,re):
    o=getattr(L,name);o.restype=re;o.argtypes=types;return o
ptr=ct.c_void_p; i32=ct.c_int
ctx=fun('GEOS_init_r',[],ptr)()
reader=fun('GEOSWKTReader_create_r',[ptr],ptr)(ctx)
writer=fun('GEOSWKTWriter_create_r',[ptr],ptr)(ctx)
read=fun('GEOSWKTReader_read_r',[ptr,ptr,ct.c_char_p],ptr)
write=fun('GEOSWKTWriter_write_r',[ptr,ptr,ptr],ptr)
free=fun('GEOSFree_r',[ptr,ptr],None)
destroy=fun('GEOSGeom_destroy_r',[ptr,ptr],None)
tr=fun('GEOSConstrainedDelaunayTriangulation_r',[ptr,ptr],ptr)
def tris2(p):
    a=read(ctx,reader,p.ExportToWkt().encode())
    b=tr(ctx,a)
    assert b
    s=write(ctx,writer,b);g=ogr.CreateGeometryFromWkt(ct.string_at(s).decode())
    free(ctx,s);destroy(ctx,b);destroy(ctx,a)
    ans=[]
    for o in g:
        z=np.array(o.GetGeometryRef(0).GetPoints())[:-1,:2]
        assert len(z)==3
        ans.append(z if flat(z)>0 else z[::-1])
    return ans

T=Transformer.from_crs(2263,6347,always_xy=True)
B=XML.parse(source).find('.//{*}Building')
assert B.find('{*}name').text=='Bldg_13210013985'
groups=collections.defaultdict(list)
for node in B.findall('{*}boundedBy'):
    n,=node[:]
    tag=n.tag.split('}')[-1]
    for o in n.findall('.//{*}Polygon'):
        a=np.fromstring(o.find('.//{*}posList').text,sep=' ').reshape(-1,3)
        assert np.max(np.linalg.norm(a[:1]-a[-1:],axis=1))<1e-4
        x,y=T.transform(*a[:-1,:2].T)
        # Round all coordinates in working metre basis. Near tangent duplicate edges are still explicitly checked.
        p=np.round(np.c_[np.c_[x,y]-local,a[:-1,2]*1200/3937],5)
        assert len(p)>=3
        groups[tag].append(p)
caps=collections.defaultdict(list)
for p in groups['RoofSurface']:
    assert np.ptp(p[:,2])<1e-5
    caps[float(p[0,2])].append(p)
wall=groups['WallSurface']
ground,=groups['GroundSurface']
assert flat(ground[:,:2])<0
cityrings={}; polyface={}
for h,g in sorted(caps.items()):
    ins=[polygon(p[:,:2]) for p in g if flat(p[:,:2])>0]
    holes=[polygon(p[:,:2]) for p in g if flat(p[:,:2])<0]
    assert len(ins)==1
    q=ins[0]
    for h0 in holes:
        assert q.Contains(h0)
        q=q.Difference(h0)
    assert q.IsValid() and q.GetGeometryName()=='POLYGON'
    cityrings[h]=[np.asarray(r.GetPoints())[:-1,:2] for r in q]
    polyface[h]=q
data=np.load(points)['a']; xy=data[:,:2]-local; zs=data[:,2]
held=np.isin(data[:,4],[1135,1136]); qual=(data[:,3]==1)&(data[:,5]==1)
new_z={}; receipt={}
targets={54.7647:[54.85,55.25],56.7114:[57.40,57.80],60.3025:[60.5,60.99],62.9883:[62.55,63.05],
         63.0023:[62.55,63.05],82.7137:[82.9,83.34]}
def inside_d(p,xy):
    x,y=xy.T;b=np.zeros(len(x),dtype=bool);d2=np.full(len(x),99999.)
    for u,v in zip(p,np.roll(p,-1,axis=0)):
        g=v-u
        if abs(g[1])>1e-9:
            b^=((v[1]>y)!=(u[1]>y))&(x<g[0]*(y-u[1])/g[1]+u[0])
        w=xy-u; dv=w-np.clip((w@g)/(g@g),0,1)[:,None]*g
        d2=np.minimum(d2,np.einsum('ij,ij->i',dv,dv))
    return b,d2
for h,poly in cityrings.items():
    zone=np.ones(len(xy),bool)
    for i,p in enumerate(poly):
        inside,d=inside_d(p,xy)
        zone&=(inside if i==0 else ~inside)&(d>.60**2)
    zone&=qual
    nearest=min(targets,key=lambda l:abs(l-h))
    if abs(nearest-h)>.002:
        receipt[h]={'action':'retain historical tier; no one-to-one height correspondence',
          'all_window_train_count':int(sum(zone&~held)),'all_window_holdout_count':int(sum(zone&held))}
        continue
    lo,hi=targets[nearest]; valid=zone&(zs>lo)&(zs<hi)
    t=zs[valid&~held]; v=zs[valid&held]; z=float(np.median(t))
    assert (len(t)>100 and len(v)>80 and np.quantile(abs(v-z),.9)<.18 and abs(z-h)<1.1)
    new_z[h]=z
    receipt[h]={'action':'fit primary matched stable height only','calibrated_navd88_m':z,
        'comparison_historical_minus_observation_not_absolute_survey_error':h-z,
        'train_in_band_n':len(t),'hold_in_band_n':len(v),
        'train_inside_all_z_n':int(sum(zone&~held)),'hold_inside_all_z_n':int(sum(zone&held)),
        'hold_abs_vertical_p50_p90_p95_m':np.quantile(abs(v-z),[.5,.9,.95]).tolist()}
print(json.dumps(receipt,indent=1))
surfaces=[]
for h,p in polyface.items():
    surfaces.append(('roof',*[np.c_[a,np.full(3,h)] for a in tris2(p)]))
gr=polygon(ground[:,:2]);assert gr.IsValid()
surfaces.append(('ground',*[np.c_[a[::-1],np.full(3,ground[0,2])] for a in tris2(gr)]))
for a in wall:
    # Project each original, nearly planar face along its longest horizontal direction.
    vec=a[np.argmax(np.linalg.norm(a[:,:2]-a[:1,:2],axis=1)),:2]-a[0,:2]
    vec/=np.linalg.norm(vec)
    dr=(a[:,:2]-a[:1,:2])@vec; dv=a[:,2]-a[0,2]
    plane=np.round(np.c_[dr,dv],7)
    q=polygon(plane)
    assert q.IsValid(), plane
    sign=np.sign(flat(plane))
    A=[]
    for tt in tris2(q):
        if sign<0:tt=tt[::-1]
        a0=[]
        for pt in tt:
            j=np.argmin(np.linalg.norm(plane-pt,axis=1))
            assert np.linalg.norm(plane[j]-pt)<1e-5
            a0.append(a[j])
        A.append(np.array(a0))
    surfaces.append(('wall',*A))
def clean_surfaces(items):
    V=[]; vi={}; F=[]; tags=[]
    def vertex(p):
        k=tuple(np.round(p,5))
        if k in vi:return vi[k]
        vi[k]=len(V);V.append(k);return vi[k]
    for label,*ts in items:
        for vv in ts:
            ff=tuple(map(vertex,vv))
            assert len(set(ff))==3
            F.append(ff);tags.append(label)
    P=np.array(V); new=[]; lab=[]
    # Noding of existing T-junctions only; no averaging, no wrong-plane stitching.
    # Do not split with points below/above true measured edge endpoints.
    for tag,f in zip(tags,F):
        border=[]; split=False
        for i,j in zip(f,f[1:]+f[:1]):
            u=P[i];g=P[j]-u
            rel=P-u;t=(rel@g)/(g@g)
            ds=np.linalg.norm(rel-t[:,None]*g,axis=1)
            c=np.flatnonzero((t>1e-5)&(t<1-1e-5)&(ds<split_tolerance))
            c=sorted(c,key=lambda k:t[k]);border.extend((i,*c))
            split|=bool(c)
        if split:
            ix=vertex(np.mean(P[list(f)],axis=0))
            for i,j in zip(border,border[1:]+border[:1]):
                new.append((ix,i,j));lab.append(tag)
        else:new.append(f);lab.append(tag)
    return np.array(V),new,lab
V,F,tags=clean_surfaces(surfaces)
E=collections.defaultdict(list)
for j,f in enumerate(F):
    for a,b in zip(f,f[1:]+f[:1]):
        E[tuple(sorted((a,b)))].append((a,b,j))
ea=[(e,v) for e,v in E.items() if len(v)!=2 or v[0][:2]!=v[-1][:2][::-1]]
print('Vertices/triangles/edges',len(V),len(F),collections.Counter(map(len,E.values())),'bad',len(ea))
for e,v in ea[:25]:
    print('bad',V[list(e)].tolist(),[tags[j] for _,_,j in v],len(v))
def export(V,F,path):
    path.write_text('# Derived 2014 CityGML Uris massing; only matched primary roof heights fitted to 2017.\n'+
      '# No geometry details in intentionally historic or unverified portions; z=0 is provisional NAVD88 46.46.\n'+
      'o Uris_Survey_Envelope\n'+''.join('v %.5f %.5f %.5f\n'%tuple(p) for p in V)+
      ''.join('f %d %d %d\n'%tuple(x+1 for x in p) for p in F))
a=V.copy()
for h,z in new_z.items():a[np.abs(V[:,2]-h)<.000015,2]=z
# Internal centroid z of splits must be mapped linearly within wall; regenerate with new vertex levels instead.
def recal(a): 
    b=a.copy()
    for h,z in new_z.items(): b[np.abs(a[:,2]-h)<.000015,2]=z
    return b
fitfaces=[(tag, *[recal(x) for x in vv]) for tag,*vv in surfaces]
fitV,fitF,fitTags=clean_surfaces(fitfaces)
# Shift to working local grade, keeping the original deep ground surface as a hidden envelope bottom.
fitV[:,2]-=z0; V[:,2]-=z0
export(V,F,dest/'city-reference-shell.obj')
export(fitV,fitF,dest/'calibrated-envelope.obj')
(dest/'measurements.json').write_text(json.dumps(receipt,indent=2)+'\n')

