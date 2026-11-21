"""Low Memorial Library survey crown indexed to CityGML. Builds an isolated closed crown study."""
from pathlib import Path
import numpy as np,gzip,xml.etree.ElementTree as X,collections,json,sys,math,hashlib
from scipy.interpolate import PchipInterpolator
from scipy.optimize import least_squares
from pyproj import Transformer
D=Path(sys.argv[1]); OUT=Path(sys.argv[2]); OUT.mkdir(exist_ok=True)
T=Transformer.from_crs(2263,6347,always_xy=True); origin_ft=np.array([994815,233735])
B=X.parse(D/'low-2014.gml').find('.//{*}Building')
assert B.find('{*}name').text=='Bldg_13210011337'
assert {t[0].text for t in B if t.attrib.get('name')=='BIN'}=={'1084472'}
ring=collections.defaultdict(set); ground=[]; crown_od=[]
for o in B.findall('{*}boundedBy'):
 typ=o[0].tag.split('}')[-1]
 if typ not in ('GroundSurface','RoofSurface'):continue
 for p in o[0].findall('.//{*}Polygon'):
  a=np.fromstring(p.find('.//{*}posList').text,sep=' ').reshape(-1,3)
  if typ=='GroundSurface':
   ground.extend(np.c_[np.transpose(T.transform(*a[:-1,:2].T)),a[:-1,2]*1200/3937]); continue
  for q in a[:-1]:
   x,y=(q[:2]-origin_ft)*1200/3937; z=q[2]*1200/3937
   if z>77:ring[round(z,4)].add((x,y))
a=np.asarray(sorted(ring[87.6869]));x,y=a.T
c0=np.linalg.lstsq(np.c_[2*x,2*y,np.ones(len(x))],x*x+y*y,rcond=None)[0][:2]
C=np.asarray(T.transform(*(c0*3937/1200+origin_ft)))
A=np.unique(np.loadtxt(D/'low-points.csv.gz',delimiter=',',skiprows=1),axis=0)
W=A[:,:2]-C; Z=A[:,2]; R=np.linalg.norm(W,axis=1)
qual=(A[:,3]==1)&(A[:,5]==1); train=qual&np.isin(A[:,4],[1063,1064,1065,1134]); held=qual&np.isin(A[:,4],[1135,1136])
# Optimize center on upper curved surface, without holdout or near-toe returns.
base=train&(R>1.4)&(R<10.5)&(Z>82.7)&(Z<88.2)
w=W[base]; z=Z[base]
def res(p):
 t=np.sum((w-p[:2])**2,axis=1)
 return p[2]+p[3]*t+p[4]*t*t+p[5]*t*t*t-z
p=least_squares(res,[0,0,87.99,-.035,0,0],loss='soft_l1',f_scale=.10,bounds=([-0.8,-0.8,87.7,-.08,-.01,-.01],[.8,.8,88.3,-.005,.01,.01])).x
S=C+p[:2]; R=np.linalg.norm(A[:,:2]-S,axis=1)
# Hard support ends before tier ambiguity, at 11.50 m radius. No inferred outer toe/drum.
bins=np.r_[0.,.5,np.arange(1.,12.,.5)]
fit=[]
for r in bins:
 m=train&(abs(R-r)<.25)&(Z>=82.2)&(Z<=88.3)
 assert sum(m)>=(4 if r==0 else 15),(r,sum(m))
 fit.append(float(np.median(Z[m])))
assert np.all(np.diff(fit)<0)
curve=PchipInterpolator(bins,fit)
# Create deliberate synthetic lower cap, not architectural geometry. Reference origin is CityGML Z transformed numerically, not ground/sill.
zref=82.
theta=np.arange(96)*2*np.pi/96
V=[(0.,0.,fit[0]-zref)]; F=[]
for r in np.arange(.25,11.51,.25):
 for t in theta:V.append((r*np.cos(t),r*np.sin(t),float(curve(r))-zref))
def k(r,t):return 1+r*96+t%96
for t in range(96):F.append((0,k(0,t),k(0,t+1)))
for j in range(45):
 for t in range(96):F.extend([(k(j,t),k(j+1,t),k(j+1,t+1)),(k(j,t),k(j+1,t+1),k(j,t+1))])
bot=len(V)
V.extend((11.50*np.cos(t),11.50*np.sin(t),0.) for t in theta); V.append((0.,0.,0.))
for t in range(96):
 i,j=k(45,t),k(45,t+1);u,v=bot+t,bot+(t+1)%96
 F.extend([(i,u,v),(i,v,j),(len(V)-1,v,u)])
path=OUT/'Low-Library-lidar-crown-study.obj'
path.write_text('# Isolated crown only. Synthetic lower closure at NAVD88 82.0; not a building replacement.\no Low_Library_Crown\n'
 +''.join('v %.7f %.7f %.7f\n'%v for v in V)+''.join('f %d %d %d\n'%tuple(x+1 for x in f) for f in F))
# Export full, unfiltered along measured crown across withheld passes. Highest near-edge cluster does not authorize toe.
within=held&(R<11.42); q=within&(Z>=82.2)&(Z<=88.3)
def quant(v):return np.quantile(v,[.5,.9,.95]).tolist()
old=json.loads((D/'old-lod2.json').read_text()); oldv=np.asarray(old['vertices'])
P=np.asarray(fit); xyz=A[within,:3]; np.savetxt(OUT/'held-roof-local.csv',np.c_[xyz[:,:2]-S,xyz[:,2]-zref],delimiter=',',fmt='%.6f')
g0=np.asarray(ground); seg=np.diff(np.r_[g0,g0[:1]],axis=0); norms=np.linalg.norm(seg[:,:2],axis=1); j=np.argmax(norms); ux=seg[j,:2]/norms[j]; uy=np.array([-ux[1],ux[0]])
cap={'schema':1,'building_BIN':1084472,'DOITT_ID':551695,'cloud_only':True,'LiDAR_NOAA_2017_subset_distinct':len(A),'CRS':'EPSG:6347 and NAVD88 GEOID18 z in meters','citygml_center':C.tolist(),'fit_center':S.tolist(),'fit_shift_m':p[:2].tolist(),'city_nominal_crown_h_m_USft_numeric':87.6869,'fitted_center_elevation_m':fit[0],'local_OBJ_z_0_NAVD88_m':zref,'crown_support_radius_m':11.50,'old_closed_LOD2_apex_local_z_and_radius_m':[float(oldv[:,2].max()),.55],
'city_ground_shell_span_along_building_edges_m':np.ptp((g0[:,:2]-C)@np.array([ux,uy]).T,axis=0).tolist(),
'city_ground_shell_z_numeric_m_not_walkable_grade':float(g0[0,2]),'train_pass_ids':[1063,1064,1065,1134],'validation_pass_ids':[1135,1136],
'held_all_n':int(within.sum()),'held_above_broad_z_qc_82_2_88_3_n':int(q.sum()),'curve_hold_all_z_abs_p50_p90_p95_m':quant(abs(Z[within]-curve(R[within]))),'curve_hold_quality_band_abs_p50_p90_p95_m':quant(abs(Z[q]-curve(R[q]))),
'profile_r_z':list(zip(bins.tolist(),fit)), 'obj_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(OUT/'fit.json').write_text(json.dumps(cap,indent=2)+'\n')
print(json.dumps({k:v for k,v in cap.items() if k!='profile_r_z'},indent=2))
