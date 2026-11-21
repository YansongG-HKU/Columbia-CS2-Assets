"""Build an offline survey shell, preserving CityGML geometry and only LiDAR-confirmed tiers."""
from prep import *
import ctypes as ct
from geos import *
from mesh import clean_surfaces
D_OUT=D/'deliver';D_OUT.mkdir(exist_ok=True)
points=D/'lerner-ground-roofs.csv.gz'
A=np.unique(np.loadtxt(points,delimiter=',',skiprows=1,usecols=range(6)),axis=0)
M=local(A[:,:2]); Z=A[:,2]; src=A[:,4].astype(int); first=(A[:,3]==1)&(A[:,5]==1)
def inside_d(p,xy):
 x,y=xy.T; b=np.zeros(len(x),bool); ds=np.full(len(x),1e6)
 for s,t in zip(p,np.roll(p,-1,axis=0)):
  v=t-s; dv=xy-s
  if abs(v[1])>1e-9:b^=((t[1]>y)!=(s[1]>y))&(x<(y-s[1])*v[0]/v[1]+s[0])
  d=dv-np.clip((dv@v)/(v@v),0,1)[:,None]*v
  ds=np.minimum(ds,np.einsum('ij,ij->i',d,d))
 return b,ds
def summary(inside):
 hist,edges=np.histogram(Z[inside],np.arange(36,81,.1)); ix=np.argsort(hist)[-18:][::-1]
 return [(round(float(edges[i]),2),int(hist[i])) for i in ix if hist[i]]
print('data',A.shape,collections.Counter(src))
ground_checks={}
X,Y=M.T
boxes={'west_broadway':(-39,-33,-17,18),'south_115th':(-27,29,-28,-24),'east_campus':(33,38,-19,18),'north':(-28,29,23,28)}
for key,(x0,x1,y0,y1) in boxes.items():
 sel=(X>=x0)&(X<=x1)&(Y>=y0)&(Y<=y1)&(A[:,3]==2)
 ar=Z[sel]
 if len(ar)>19:
  ground_checks[key]={'bbox_local_m':[x0,x1,y0,y1],'n':len(ar),'z_p10_50_90':np.quantile(ar,[.1,.5,.9]).tolist()}
print('ground checks',json.dumps(ground_checks))
for r in sorted(groups['RoofSurface'],key=lambda p:p[0,2]):
 sel0,dd=inside_d(r[:,:2],M); sel=sel0&(dd>1.)&first; print(r[0,2],sum(sel),dict(collections.Counter(src[sel])),summary(sel))
from shell_core import build_shell
held=np.isin(src,[1135,1136])
def fit(name,domain,band,previous=None,min_coverage=.93):
 lo,hi=band; cut=domain&(Z>=lo)&(Z<=hi)
 tr=cut&~held; te=cut&held; cf=sum(te)/sum(domain&held); train_cf=sum(tr)/sum(domain&~held)
 assert min(cf,train_cf)>min_coverage and min(sum(tr),sum(te))>100,(name,cf,train_cf,sum(tr),sum(te))
 h=round(float(np.median(Z[tr])),2)
 def error(ref):
  return [float(u) for u in np.quantile(np.abs(Z[te]-ref),[.5,.9,.95])]
 return h,dict(candidate_height_NAVD88_m=h,point_filter=['classification=1','return=1'],height_screen_m=band,
   train_in_band=int(sum(tr)),hold_in_band=int(sum(te)),hold_total=int(sum(domain&held)),train_in_band_fraction=train_cf,
   hold_in_band_fraction=cf,held_error_p50_p90_p95_m=error(h),
   historic_height_m=previous,historic_held_error_p50_p90_p95_m=error(previous) if previous is not None else None)
r0=next(r for r in groups['RoofSurface'] if abs(r[0,2]-60.13451)<.00005)
actual,edge_distance=inside_d(r0[:,:2],M)
n,e=fit('central east',actual&(edge_distance>1.)&first,[60.23,60.57],float(r0[0,2]))
historical={}
for r in sorted(groups['RoofSurface'],key=lambda p:p[0,2]):
 if r is r0:continue
 q,edge=inside_d(r[:,:2],M)
 dom=q&(edge>1.)&first
 mode=55.2 if r[0,2]<59 else 72.2
 reg=(Z>=mode-.14)&(Z<=mode+.16)
 historical[str(r[0,2])]={'action':'historical placeholder, not laser-calibrated as whole tier',
   'all_first_return_n':int(sum(dom)),'dominant_mode_band_m':[mode-.14,mode+.16],
   'fraction_dominant_mode':float(sum(dom&reg)/sum(dom))}
z0=round(ground_checks['west_broadway']['z_p10_50_90'][1],2)
obj=build_shell({float(r0[0,2]):n},z0,D_OUT/'Lerner-central-roof-measuring-shell.obj')
gdelta=np.asarray(gp.Centroid().GetPoint_2D())-np.asarray(fp.Centroid().GetPoint_2D())
receipt={'notice':'Offline 2014/2017 measuring shell; no CS2 Editor, no facade, ramps, windows, LOD, or publish acceptance. Historic tiers remain placeholders.',
 'source':{'nyc_2014_archive':'https://maps.nyc.gov/download/3dmodel/DA_WISE_GML.zip','footprint':'https://data.cityofnewyork.us/resource/5zhs-2jue.geojson?bin=1082166','lidar_catalog':'https://www.fisheries.noaa.gov/inport/item/64728/full-list',
 'lidar_ept':'https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9306','bin':'1082166','doitt_id':'397140',
 'historic_building':B.find('{*}name').text,'gml_sha256':hashlib.sha256((D/'lerner-nyc-2014.gml').read_bytes()).hexdigest(),
 'footprint_sha256':hashlib.sha256((D/'lerner-footprint.geojson').read_bytes()).hexdigest(),
 'cropped_points_csv_gz_sha256':hashlib.sha256(points.read_bytes()).hexdigest()},
 'metre_frame':{'horizontal_epsg':6347,'vertical_for_lidar':'EPSG 5703 NAVD88 GEOID18','origin_xy':O.tolist(),'axes_NE_rows':axis.tolist(),
 'z_zero_from_broadway_m':z0,'citygml_historic_bottom_not_ground_navd88_control':float(g[0,2]),'plan_span_oriented_m':np.ptp(P,axis=0).tolist(),
 'historic_minus_footprint_centroid_m':gdelta.tolist(),'raw_footprint_symmetric_difference_m2':gp.SymDifference(fp).GetArea(),
 'after_translation_plan_shape_symmetric_difference_m2':poly(P+gdelta).SymDifference(gp).GetArea()},
 'point_split':{'distinct_records':len(A),'hold_source_ids':[1135,1136],'crop_query':json.loads((D/'lerner-ground-roofs.json').read_text()),
 'ground_class_2_quadrants':ground_checks,
 'broadway_to_campus_box_median_delta_m':round(ground_checks['east_campus']['z_p10_50_90'][1]-z0,3)},
 'central_east_roof':e,'unadjusted_historic_roofs':historical,'shell':obj}
# Diagnostic windows lie inside selected regions; these are not roof boundaries.
zones={
 'Broadway flat inner deck':([-25.8,-17.8,-12.0,13.0],[72.05,72.37]),
 'east perimeter low deck':([29.0,30.8,1.0,16.5],[55.08,55.34]),
 'south adjacent lower return band, identity unresolved':([-9.2,14.3,-21.9,-19.7],[48.53,48.86]),
}
roi={}
for label,(box,band) in zones.items():
 x0,x1,y0,y1=box
 domain=first&(X>x0)&(X<x1)&(Y>y0)&(Y<y1)
 lo,hi=band
 ok=domain&(Z>=lo)&(Z<=hi)
 tr=ok&~held; te=ok&held
 assert sum(tr)>100 and sum(te)>70
 zz=round(float(np.median(Z[tr])),2)
 roi[label]={'local_xy_window_m':box,'searched_height_band_m':band,'z_train_NAVD88_m':zz,
 'n_train_in_band':int(sum(tr)),'n_hold_in_band':int(sum(te)),'n_hold_all_heights':int(sum(domain&held)),
 'hold_in_band_abs_error_p50_p90_p95_m':np.quantile(abs(Z[te]-zz),[.5,.9,.95]).tolist(),
 'action':'diagnostic only; not used to change the shell'}
receipt['diagnostic_windows']=roi
(D_OUT/'measurements.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'central':e,'unadjusted':historical,'shell':obj},indent=2))
