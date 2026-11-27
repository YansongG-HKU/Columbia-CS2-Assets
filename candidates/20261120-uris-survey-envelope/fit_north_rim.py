"""Evidence-clipped curved roof rim, 2017 survey, no walls or import."""
import sys, json, gzip, hashlib, collections
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from pyproj import Transformer
raw=Path(sys.argv[1]); city=Path(sys.argv[2]); out=Path(sys.argv[3]);out.mkdir(exist_ok=True)
with gzip.open(raw,'rt') as g:
    a=np.unique(np.loadtxt(g,delimiter=',',skiprows=1,usecols=range(6)),axis=0)
assert len(a)==292195
origin=np.array([587623.1421979353,4518097.006500896])
arc_center=np.array([587624.3011,4518100.1849])
p=a[:,:2]-arc_center; r=np.linalg.norm(p,axis=1); ang=np.arctan2(p[:,1],p[:,0]); deg=np.degrees(ang)
z=a[:,2]; hold=np.isin(a[:,4],[1135,1136]); roof=(a[:,3]==1)&(a[:,5]==1)
zone=(deg>=25)&(deg<=150)
high=roof&zone&(r>19.5)&(r<23.0)&(z>=55.77)&(z<=56.18)
used=high&~hold
def col(t):return np.c_[np.ones(len(t)),np.cos(t),np.sin(t),np.cos(t*2),np.sin(t*2)]
A=col(ang)
def robust(M,v,f):
    return least_squares(lambda q:M@q-v,np.linalg.lstsq(M,v,rcond=None)[0],loss='soft_l1',f_scale=f).x
R=robust(A[used],r[used],.19)
h0=float(np.median(z[used]))
err=r-A@R
hband=np.percentile(err[used],[3,97])
# Symmetric robust band enclosing most sampled roof-top points, not measured vertical edges.
half=float(max(abs(hband)))
assert .12<half<.50 and 55.95<h0<56.13
S=np.arange(30,146.01,4)
E=np.deg2rad(S);pred=col(E)@R
# Keep outer flat panel on consistently observed roof, not the municipal envelope.
low=roof&(z>=54.85)&(z<=55.25)&(r>=15)&(r<25)&~hold
edge=[]
for t,rc in zip(S,pred):
    selected=low&(abs(deg-t)<2.4)&(r>rc+half-.08)
    assert selected.sum()>10
    edge.append(float(np.quantile(r[selected],.95)-.10))
edge=np.array(edge)
assert (edge-pred-half>.2).all()
base=float(np.median(z[roof&zone&(r>11)&(r<18)&(z>54.85)&(z<55.25)&~hold]))
# 6 columns: inset low deck -> curb foot -> curb crown -> curb crown -> foot -> outer deck.
ring=np.c_[np.full(len(S),15.),pred-half,pred-half,pred+half,pred+half,edge]
H=[base,base,h0,h0,base,base]
V=[];F=[];tag=[]
for t,rs in zip(E,ring):
    for d,h in zip(rs,H):
        x,y=arc_center-origin+d*np.array([np.cos(t),np.sin(t)])
        V.append((x,y,h-46.46))
for j in range(len(E)-1):
    for i in range(5):
        p=j*6+i;q=p+1;u=p+6;v=q+6
        F.extend(((p,q,v),(p,v,u)));tag.extend((i,i))
V=np.round(np.array(V),6);el=collections.defaultdict(list)
for n,f in enumerate(F):
    p=V[list(f)]
    no=np.cross(p[1]-p[0],p[2]-p[0]);assert np.linalg.norm(no)>.001 and no[2]>-1e-6
    for i,j in zip(f,f[1:]+f[:1]):el[tuple(sorted((i,j)))].append((i,j))
bounds=[k for k,v in el.items() if len(v)==1]
assert all(len(v)==1 or (len(v)==2 and v[0]==v[1][::-1]) for v in el.values())
assert set(collections.Counter(x for j in bounds for x in j).values())=={2}
f=out/'Uris-north-roof-rim-study.obj'
f.write_text('# Uris arc roof: locally observed upper band and flat deck; inferred risers\n'+
             '# Metres in EPSG6347 local frame; z=0 uses provisional front grade 46.46 NAVD88.\n'+
             'o Uris_North_Arc_Roof_Study\n'+
             ''.join('v %.6f %.6f %.6f\n'%tuple(x) for x in V)+
             ''.join('f %d %d %d\n'%tuple(i+1 for i in f) for f in F))
(out/'facet-source-tags.json').write_text(json.dumps({'bands_by_face_in_export_order':tag},indent=2)+'\n')
geom=json.loads(city.read_text())['features'][0]['geometry']['coordinates'][0][0]
pts=np.array(Transformer.from_crs(4326,6347,always_xy=True).transform(*np.array(geom).T)).T
t=pts-arc_center; ts=np.degrees(np.arctan2(t[:,1],t[:,0])); rs=np.linalg.norm(t,axis=1)
k=(ts>=30)&(ts<=146)
# Interpolate common central sector only. Full site dimensions require local axis.
ii=np.argsort(ts[k]); Q=np.interp(S,ts[k][ii],rs[k][ii])
# Nearby paving versus independent higher linear band. Neither is a wall-foot survey.
control={}
for name,rc,tw,hmin,hmax in [('inner_paving',23.0,16,47.5,48.10),('higher_outer_band',24.7,20,48.35,48.90)]:
    ok=zone&(deg>=43)&(deg<=133)&(abs(r-rc)<1.0)&(z>=hmin)&(z<=hmax)&(a[:,5]==1)&np.isin(a[:,3],[1,2])
    control[name]=[{ 'n':int(sum(ok&m)), 'navd88_p10_p50_p90_m':np.quantile(z[ok&m],[.1,.5,.9]).tolist()}
                   for m in (~hold,hold)]
data={'source_csv_gz_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),
      'city_footprint_geojson_sha256':hashlib.sha256(city.read_bytes()).hexdigest(),
      'held_out_ids':[1135,1136],'centre_epsg6347_m':arc_center.tolist(),'origin_epsg6347_m':origin.tolist(),
      'z0_navd88_m':46.46,'angles_deg':S.tolist(),'radial_roof_edge_m':edge.tolist(),
      'centreline_radial_coeff_1_cos_sin_cos2_sin2':R.tolist(),
      'nominal_sampled_band_width_m':2*half, 'band_width_not_surveyed_wall_width':True,
      'deck_navd88_m':base, 'raised_band_navd88_m':h0,
      'median_height_difference_m':h0-base,
      'higher_band_train_n':int(used.sum()), 'higher_band_withheld_n':int((high&hold).sum()),
      'higher_band_withheld_centreline_distance_p50_p90_m':np.quantile(abs(err[high&hold]),[.50,.90]).tolist(),
      'nearby_ground_support':control,
      'city_outline_minus_flat_roof_edge_m_p05p50p95':np.quantile(Q-edge,[.05,.50,.95]).tolist(),
      'city_outline_not_used_as_roof_edge':True,
      'vertices':len(V),'faces':len(F),'open_cut_boundary_edges':len(bounds),
      'two_face_edges':len(el)-len(bounds),'raised_vertical_faces_are_inferred':True,
      'obj_sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
(out/'rim-study.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data,indent=1))

