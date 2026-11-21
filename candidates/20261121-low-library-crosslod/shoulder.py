"""Derive the far shoulder station from the same source dataset but a new annular subset."""
import json,sys
from pathlib import Path
import numpy as np
p,d=map(Path,sys.argv[1:])
a=np.unique(np.loadtxt(p/'low-points.csv.gz',delimiter=',',skiprows=1),axis=0)
j=json.loads((p/'deliver/fit.json').read_text())
w=a[:,:2]-j['fit_center'];r=np.linalg.norm(w,axis=1)
az=(np.arctan2(w[:,1],w[:,0])+np.pi)%(2*np.pi)//(np.pi/4)
q=(a[:,3]==1)&(a[:,5]==1)&(abs(r-11.72)<.08); t=q&np.isin(a[:,4],[1063,1064,1065,1134]); h=q&np.isin(a[:,4],[1135,1136])
z=a[:,2]; t_ref=float(np.median(z[t])); vals=[float(np.median(z[t&(az==i)])) for i in range(8)]
hold_med=float(np.median(z[h]))
assert sum(t)>150 and sum(h)>100 and np.ptp(vals)<.38 and abs(t_ref-hold_med)<.12 and all(min(sum(q0&(az==i)) for i in range(8))>=8 for q0 in (t,h))
capt={'base_reference':'Farthest already patched LOD2 FBX; maintain the same 45.0 m NAVD88 crown-only offset.',
 'raw_anchor_radius_m':11.7232,'sample_annulus_center_and_half_width_m':[11.72,.08],
 'elevation_baseline_lod2':36.9,'rise_11_72':round(t_ref-45-36.9,6),'training_points':int(sum(t)),'paired_continuous_eight_sectors_training_medians_m':vals,
 'train_median_z_NAVD88':t_ref,'held_points':int(sum(h)),'held_median_z_NAVD88':hold_med,
 'held_residual_p50_p90_p95_against_training_median_m':np.quantile(abs(z[h]-t_ref),[.5,.9,.95]).tolist()}
(d/'shoulder-plan.json').write_text(json.dumps(capt,indent=2)+'\n')
np.savetxt(d/'shoulder-held-local.csv',np.c_[w[h],z[h]-82],delimiter=',',fmt='%.6f')
print(capt)
