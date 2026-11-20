# Uris Hall: closed massing shell and roof calibration

This draft replaces neither the published content nor the existing CS2 import trial. It reconstructs the closed building envelope with a **true curved north wing** from CityGML and six compatible roof tiers from airborne survey. This is a geometry foundation for an improved asset, not that finished asset.

## Provenance

- [NYC OTI 3D Building Model, 2014 collection](https://github.com/CityOfNewYork/nyc-geo-metadata/blob/main/Metadata/Metadata_3DBuildingModel.md). Exact public byte range 130249474–174447202 of the CityGML archive returned the compressed DA13 entry (44,197,729 bytes including local header). The 64 KiB directory suffix and DeliveryArea vector independently establish geographic coverage. Decompressing in streams verified the entry CRC 0x13a23f43 against the ZIP. Extract exactly the registered BIN **1084473**, DOITT_ID 186607, Bldg_13210013985, raw extracted GML SHA256 7a99f794e1f62d74eeef1886969598631d80e9b4298db05e67ab826bd7e55389. Historic CityGML outer perimeter and 77 exterior wall facets associated with the curved-wing roof level are preserved in plan; the data are not a recent wall survey.
- [NYC OTI 2D footprints](https://data.cityofnewyork.us/City-Government/BUILDING/5zhs-2jue/about_data), photogrammetric feature BIN 1084473 edited August 2017, exact query receipt in the rim record. It confirms the curved origin and lies about 0.8 m outside the inset 2017 flat roof edge in this section; not a substitute for tracing the actual roof curb or wall foundation. Its generic year attribute is not the established building year.
- [NOAA 9306 EPT](https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9306/ept.json); 292,195 observables in EPSG:6347, height NAVD88 GEOID18 metres. Only matching stable roof terraces calibrated. Do not apply one overall height correction (not all differences share direction), or align the old point-cloud/historical highest equipment and published city nominal height as if they are the same point. No terrain/base, slope, doors, windows or material measured from a roof point collection.
- [Blaer & Allen figure 14](https://www.cs.columbia.edu/~allen/PAPERS/blaer_jfr2009.pdf#page=16) and [GLUCK+ architectural reference](https://gluckplus.com/project/columbia-university-business-school-addition/) independently orient the straight rotunda-facing side opposite the curved north frontage. [NYC 2024 ortho](https://tiles.arcgis.com/tiles/yG5s3afENB5iO9fj/arcgis/rest/services/NYC_Orthos_2024/MapServer) cross-checks extents. No image was used as proof of surveyed wall thickness or matching rooftop equipment today.

## Geometry and limits

| Component | 2014 height after units conversion | 2017 fitted NAVD88 m |
| --- | ---: | ---: |
| Curved roof deck | 54.765 m | 55.04 m |
| Narrow straight intermediate terrace | 56.711 m | 57.63 m |
| Broad podium | 60.302 m | 60.76 m |
| Small protrusion 1 | 62.988 m | 62.81 m |
| Small protrusion 2 | 63.002 m | 62.80 m |
| Main lower tower roof strip | 82.714 m | 83.14 m |
| Two upper plant masses | 85.283 / 88.179 m | historical placeholder, no one-to-one fit |

18,167 band-selected held-out first returns from whole IDs 1135/1136: tier median absolute height error 0.03–0.05 m, p90 0.07–0.09 m. This excludes other surfaces in the same plan area and is not an all-roof residual. See measurements.json for counts. Do not confuse narrow north rim (~56.06 m) with wide rectangular intermediate terrace (57.63 m).
The enclosed candidate contains 284 vertices, 564 triangles, 846 oriented two-face edges, no open perimeter or nonadjacent triangle overlaps in independent Blender reimport. CityGML originally encodes three negative roof rings separately: subtract these holes before constrained planar triangulation so no faces overlap the higher tiers. Noded existing junctions and retained agreed plan. The original 37.996-m underground CityGML base is a **hidden cap**, not a floor or game level. View displays a provisional reference plane 46.46 m NAVD88 to mask that cap. Nearby paving and retainers are not bulk rebuilt.

### Lot and roof detail are separate

- The registered dimensions, in the building's own oriented axes, are **68.61×80.99 m**; canonical trial lot is **48×72 m (6×9 cells)**. At 8 m cells, 9×11 is only an arithmetic enclosure, not a recommendation to change prefab settings without required margins, grade, path and Editor tests. No global shrink, origin or lot edit used.
- The separate reconstructed rim layer has 290 triangles and an accepted 1.02 m rise across the supported central arc. 64/68 height-selected withheld rim returns intersect the new measured-top faces; 1057/1158 on lower faces. Their conditional median errors are 0.04 and 0.03 m, p90 0.09 / 0.06 m. Intentional cut boundary and inferred risers; this piece has not been merged blindly into the roof shell or applied to a prefab. Adjacent observed 47.82–47.85 m paving and nearby +0.79–0.80 m distinct outside band are not facade floor elevations.
- Window bays, limestone front mask, true graded contacts, modern fans, roof trim and matching three LOD meshes/textures still need construction and an import test. The two brown upper shapes in the preview are historical. Use the shell as a measured limit, not importing it unchanged as the game asset.

Replay: extract DA13 via extract_da13_uris.py; load the exact crop NPZ (`a` matrix as in rim source); run city_shell.py CITY_GML CROP_NPZ OUTPUT with numpy, pyproj, GDAL/OGR and GEOS 3.10+; run axis_extent_check.py CITY_GML calibrated-envelope.obj; see fit_north_rim.py and validate_rim.py for the independent study. verify_render_city_shell.py is the separate Blender check. None of these constitutes a CS2 Editor pass.
