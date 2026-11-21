"""Sample the 2017 ground-only NYC DEM using landmarks selected on 2024 ortho."""
from osgeo import gdal
from pyproj import Transformer
import argparse,json,numpy as np,hashlib
from pathlib import Path

arg=argparse.ArgumentParser(description=__doc__)
arg.add_argument('dem',type=Path)
arg.add_argument('ortho_reference',type=Path)
arg.add_argument('report',type=Path)
a=arg.parse_args()
gdal.UseExceptions()
pix={'front-west':(390,425),'front-central':(450,457),'front-east':(516,488),'western-side':(322,263),
     'eastern-side':(658,443),'north-plaza':(463,50)}
r=json.loads(a.ortho_reference.read_text());scale=r['resolution_web_mercator']; W=20037508.342789244
assert (r['zoom'],r['tile_min_x'],r['tile_min_y'],r['tile_size'])==(19,154428,196936,256)
to2263=Transformer.from_crs(3857,2263,always_xy=True)
to4326=Transformer.from_crs(2263,4326,always_xy=True)
d=gdal.Open(str(a.dem));g=d.GetGeoTransform()
assert g==(994600.0,1.0,0.0,234375.0,0.0,-1.0)
b=d.GetRasterBand(1)
assert b.GetNoDataValue() is not None
foot_m=1200/3937
s={}
for k,(x,y) in pix.items():
    e,n=to2263.transform(-W+(r['tile_min_x']*256+x+.5)*scale,W-(r['tile_min_y']*256+y+.5)*scale)
    col,row=int(e-g[0]),int(g[3]-n)
    p=b.ReadAsArray(col-4,row-4,9,9)
    valid=p[np.isfinite(p)&(p!=b.GetNoDataValue())]
    if len(valid)!=81:raise ValueError('Incomplete site patch '+k)
    q=np.percentile(valid,[0,10,50,90,100])
    s[k]={'ortho_center_px':[x,y],'state_plane_ft':[e,n],'lonlat':to4326.transform(e,n),
          'samples':len(valid),'nine_ft_square_grid':True,'percentiles_ft':q.tolist(),
          'percentiles_m':(q*foot_m).tolist()}
out={'crop_sha256':hashlib.sha256(a.dem.read_bytes()).hexdigest(),'height_ref':'NAVD88 Geoid12B US survey feet',
     'dem_bounds_EPSG2263_ft':[994600,233660,995300,234375],
     'ground_only':True,'station_labels':'Approximate visually selected flat pavement; not surveyed doorway sill or property low point',
     'patches':s}
a.report.write_text(json.dumps(out,indent=2)+'\n')
for k,v in s.items():print(k,round(v['percentiles_m'][2],3))
