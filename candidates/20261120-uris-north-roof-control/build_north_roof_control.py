"""Detached Uris north 2017 LiDAR roof surface; no wall, thickness or CS2 import."""
import gzip
import hashlib
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from pyproj import Transformer
from scipy.spatial import ConvexHull

PIX_PER_TILE = 256
PX = 0.29858214173896974
WORLD = 20037508.342789244
TILE = np.array([154428, 196936]) * PIX_PER_TILE
HOLD = [1135, 1136]
ORIGIN_PX = [590., 218.]
UV = np.array([[.887, .462], [.462, -.887]])
Z_BAND = [54.90, 55.18]
STATIONS = {
    "curved_north_flat": [(566,155),(615,145),(649,171),(648,193),(622,208),(572,190)],
    "low_rectangular_front": [(452,367),(488,384),(476,414),(434,394)],
    "low_rectangular_east": [(641,378),(661,342),(662,368),(648,397),(632,412)],
    "low_rectangular_rear_mixed_edges": [(449,205),(491,226),(478,243),(442,230)],
    "east_step_mixed": [(518,407),(529,413),(523,426),(509,421)],
    "west_apparent_fan_mixed": [(465,279),(471,271),(484,278),(483,290),(473,294),(465,286)],
    "east_apparent_fan_mixed": [(586,351),(597,351),(605,358),(602,368),(591,369),(585,362)],
    "front_plaza_ground": [(444,453),(460,459),(458,468),(440,462)],
}
UTM = Transformer.from_crs(3857, 6347, always_xy=True)
MERC = Transformer.from_crs(6347, 3857, always_xy=True)


def quantiles(z):
    return [round(float(v), 3) for v in np.percentile(z, [10, 50, 90])] if len(z) else []


def length_to_chord(vertices, i):
    a, b, c = vertices[i - 1], vertices[i], vertices[(i + 1) % len(vertices)]
    t = np.clip(np.dot(b-a, c-a) / np.dot(c-a,c-a), 0, 1)
    return np.linalg.norm(b - (a+t*(c-a)))


def outline(xy):
    # Simplify only *inward*. Never invent the missing outer parapet/edge.
    v = xy[ConvexHull(xy).vertices]
    while len(v) > 6:
        costs = [length_to_chord(v, j) for j in range(len(v))]
        if min(costs) > 0.28:
            break
        v = np.delete(v, int(np.argmin(costs)), axis=0)
    return v


def in_ring(p, v, tol=0):
    e = np.roll(v, -1, axis=0)-v
    d = p[:, None, :] - v[None, :, :]
    return np.all((e[None,:,0]*d[:,:,1]-e[None,:,1]*d[:,:,0])
                  >= -tol*np.linalg.norm(e,axis=1),axis=1)


def main(path):
    source = open(path, "rb").read()
    with gzip.open(path, "rt") as f:
        a = np.loadtxt(f, delimiter=",", skiprows=1, usecols=(0,1,2,3,4,5))
    a = np.unique(a, axis=0)
    assert len(a)==292195 and a.shape[1] == 6
    x, y = MERC.transform(a[:,0],a[:,1])
    p = np.c_[(x+WORLD)/PX, (WORLD-y)/PX] - TILE
    uv = (p-ORIGIN_PX) @ UV.T
    held = np.isin(a[:,4],HOLD)
    primary = (a[:,5]==1)&np.isin(a[:,3],[1,2])
    station = {}
    pix = np.rint(p).astype(int)
    idx = np.flatnonzero(np.all((pix>=0)&(pix<768),axis=1))
    for name, polygon in STATIONS.items():
        raster = Image.new('1',(768,768))
        ImageDraw.Draw(raster).polygon(polygon,fill=1)
        selected = idx[np.asarray(raster)[pix[idx,1],pix[idx,0]]]; selected=selected[primary[selected]]
        station[name] = {"polygon_2024_ortho_pixels":polygon}
        for label,b in (("train",False),("hold",True)):
            z=a[selected[held[selected]==b],2]
            station[name][label]={"n":len(z),"p10_50_90_navd88_m":quantiles(z)}
    upper_utm={
       "upper_station_west_83m": [(587586.95,4518076.03),(587588.17,4518075.44),(587587.37,4518073.82),(587586.15,4518074.41)],
       "upper_station_mid_83m": [(587603.56,4518065.23),(587606.00,4518064.05),(587605.40,4518062.83),(587602.96,4518064.01)],
       "upper_east_cap_85m": [(587629.29,4518062.29),(587630.51,4518061.70),(587629.42,4518059.47),(587628.20,4518060.06)],
    }
    for name, polygon in upper_utm.items():
        poly=np.asarray(polygon)
        poly=poly[ConvexHull(poly).vertices]
        kk=np.flatnonzero(primary & (a[:,3]==1) & np.all(a[:,:2]>=poly.min(0),axis=1) &
                          np.all(a[:,:2]<=poly.max(0),axis=1))
        kk=kk[in_ring(a[kk,:2],poly)]
        station[name]={"polygon_epsg6347_m":polygon}
        for label,b in (("train",False),("hold",True)):
            z=a[kk[held[kk]==b],2]
            station[name][label]={"n":len(z),"p10_50_90_navd88_m":quantiles(z)}
    roi=(uv[:,0]>=-106)&(uv[:,0]<=107)&(uv[:,1]>=2.5)&(uv[:,1]<=120)
    zband=(a[:,2]>=Z_BAND[0])&(a[:,2]<=Z_BAND[1])
    root = roi&primary&(a[:,3]==1)
    train=a[root&zband&~held]; check=a[root&zband&held]
    origin=np.array(UTM.transform( (ORIGIN_PX[0]+TILE[0])*PX-WORLD,
                                 WORLD-(ORIGIN_PX[1]+TILE[1])*PX ))
    # Work in real UTM metres. Keep spatial cells seen in >=2 train swaths and >=3 observations.
    keys=np.floor((train[:,:2]-origin)/.56).astype(int)
    cell={}
    for k,r in zip(keys,train):
        cell.setdefault(tuple(k),[]).append(r)
    supported=np.array([np.mean(c,axis=0)[:2] for c in cell.values()
                         if len(c)>=3 and len(set(r[4] for r in c))>=2])
    v=outline(supported-origin)
    # Remove 0.6m radial margin at the uncertain roof/wall transition.
    c=v.mean(axis=0); vec=v-c; v=c+vec*(1-.60/np.linalg.norm(vec,axis=1))[:,None]
    center=v.mean(axis=0)
    zfit=float(np.median(train[:,2]))
    hz=check[:,2]-zfit
    broad=a[root&held]; broad_inside=in_ring(broad[:,:2]-origin,v)
    # Detect contamination from neighboring roofs separately from point selection.
    inside_z=broad[broad_inside,2]
    matches=np.abs(inside_z-zfit)<=.25
    area=float(np.sum(v[:,0]*np.roll(v[:,1],-1)-v[:,1]*np.roll(v[:,0],-1))/2)
    assert area>0 and .95 < np.mean(matches) and np.mean(in_ring(check[:,:2]-origin,v,.55))>.92
    report={"source_csv_gz_sha256":hashlib.sha256(source).hexdigest(),"heldout_ids":HOLD,
            "station":station,"north_patch":{"datum_horizontal":"EPSG:6347",
            "datum_vertical":"NAVD88 metres GEOID18", "origin_utm_m":origin.tolist(),
            "local_z0_navd88_m":46.46,"surface_navd88_m":zfit,
            "train_z_band_m":Z_BAND,"train_n_in_band":len(train),"hold_n_in_band":len(check),
            "train_spatial_cells_with_repeated_swaths":len(supported),
            "hull_held_coverage_with_55cm_tolerance":float(np.mean(in_ring(check[:,:2]-origin,v,.55))),
            "held_all_z_inside_hull_n":len(inside_z),"held_all_z_inside_hull_within_25cm":float(np.mean(matches)),
            "held_outside_25cm_z_p10_50_90_m":quantiles(inside_z[~matches]),
            "hold_abs_height_error_p50_p90_in_band_m":np.percentile(abs(hz),[50,90]).tolist(),
            "mesh_area_m2":area,"mesh_extents_local_utm_m":[v.min(axis=0).tolist(),v.max(axis=0).tolist()],
            "ring_vertices":len(v),"expected_open_edges":len(v)}}
    lines=['# Uris north curved roof interior survey control, NOT an import asset',
           '# x=east y=north z=up (meters); see evidence for georeference', 'o Uris_North_Roof_control']
    z=zfit-46.46
    lines.extend(f'v {x:.5f} {y:.5f} {z:.5f}' for x,y in np.vstack([center,v]))
    lines.extend(f'f 1 {j+2} {(j+1)%len(v)+2}' for j in range(len(v)))
    print(json.dumps({"evidence":report,"obj":"\n".join(lines)+"\n"}))


if __name__=="__main__":
    main(sys.argv[1])
