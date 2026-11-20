"""Check the city envelope against nominal lot cells without any scaling."""
from pathlib import Path
import numpy as np,xml.etree.ElementTree as E, json,sys
from pyproj import Transformer
gml,src=map(Path,sys.argv[1:])
T=Transformer.from_crs(2263,6347,always_xy=True)
for o in E.parse(gml).findall('.//{*}RoofSurface'):
 a=np.fromstring(o.find('.//{*}posList').text,sep=' ').reshape(-1,3)
 if abs(a[0,2]*1200/3937-82.71374)>.002:continue
 d=np.diff(np.array(T.transform(*a[:,:2].T)).T,axis=0)
 u=d[np.argmax(np.linalg.norm(d,axis=1))];u/=np.linalg.norm(u);u*=np.sign(u[0]);break
assert 'u' in globals()
R=np.column_stack([u,[-u[1],u[0]]]); assert np.linalg.det(R)>.999
vv=np.array([[float(i) for i in x.split()[1:]] for x in src.read_text().splitlines() if x.startswith('v ')])
new=vv[:,:2]@R; lo,hi=new.min(0),new.max(0)
a,b=lo+(hi-lo)/2,hi-lo
assert np.all(b>[48,72]) and np.allclose(np.ceil(b/8),[9,11])
report=dict(width_depth_m=b.tolist(),local_east_north_rotation=R.tolist(),asset_axis_central_offset_m=a.tolist(),
    current_6x9_dimensions_m=[48,72],min_integer_8m_cells_math_only=np.ceil(b/8).astype(int).tolist(),
    no_scaling_or_reflection=True,
    placement_note='Mathematical bbox only. No existing plop settings, building origin, lot meaning, roads or usable frontage were changed; reserve margins and verify in CS2.')
print(json.dumps(report,indent=2))
