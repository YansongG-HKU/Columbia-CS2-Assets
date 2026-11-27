"""Check next shared near/mid shoulder radius and freeze a monotonic base-surface plan."""
import json,sys
from pathlib import Path
import numpy as np
survey,plan=map(Path,sys.argv[1:])
a=np.unique(np.loadtxt(survey/'low-points.csv.gz',delimiter=',',skiprows=1),axis=0)
j=json.loads((survey/'deliver/fit.json').read_text()); w=a[:,:2]-j['fit_center']; r=np.linalg.norm(w,axis=1)
az=(np.arctan2(w[:,1],w[:,0])+np.pi)%(2*np.pi)//(np.pi/4); qc=(a[:,3]==1)&(a[:,5]==1)&(abs(r-11.8322)<.08)
t=qc&np.isin(a[:,4],[1063,1064,1065,1134]); h=qc&np.isin(a[:,4],[1135,1136])
z=a[:,2]; ref=float(np.median(z[t])); hv=float(np.median(z[h])); medb=[float(np.median(z[t&(az==i)])) for i in range(8)]
assert sum(t)>=160 and sum(h)>=95 and np.ptp(medb)<.39 and abs(ref-hv)<.12 and all(min(sum(m&(az==i)) for i in range(8))>=8 for m in (t,h))
p=json.loads(plan.read_text())
p['alignment']=p['alignment'].replace('r=3.594 and r=11.832','r=3.594 and r=12.606')
p['supported_near_outer_station']={'rad_center_m':11.8322,'train_count':int(sum(t)),'held_count':int(sum(h)),'train_NAVD88_m':ref,'held_NAVD88_m':hv,'sector_medians_m':medb}
p['monotonic_taper_note']='Keep measured fit unless it would reverse the radial slope against the retained inner substrate and lantern. Set conservative rises at 4.7674 and 5.9125 m without changing lantern or its base.'
for u in p['rings']:
 if u['radius_m']==4.7674:u['rise_m']=.26;u['blend_weight']=round(.26/.696874,6)
 if u['radius_m']==5.9125:u['rise_m']=.63;u['blend_weight']=round(.63/.698875,6)
p['rings'].append(dict(radius_m=11.8322,old_height_m=36.7789,blend_weight=1,rise_m=round(ref-45-36.7789,6)))
height=[41.6698]+[x['old_height_m']+x['rise_m'] for x in p['rings']]+[35.8406]
assert all(a>b for a,b in zip(height,height[1:])),height
plan.write_text(json.dumps(p,indent=2)+'\n')
print(height,p['supported_near_outer_station'])
