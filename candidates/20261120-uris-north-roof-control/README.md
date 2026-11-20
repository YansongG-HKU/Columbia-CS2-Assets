# Uris Hall: roof survey controls and detached curved roof prototype

This folder does not replace an FBX and is not fit for batch import. It contains a georeferenced **roof-interior-only** 12-triangle surface, a plan drawing, reproducible construction, and measurements tied to the exact independently read back near/mid/far trial. It does not assert that the northern annex is in CS2 canon; the original package covers a simplified footprint.

## Data and separate holdout

- 2017 [NOAA NYC LiDAR EPT, collection 9306](https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9306/ept.json) in EPSG:6347 metres / NAVD88 GEOID18. The QGIS crop has 292,253 raw rows, 292,195 distinct observations across the six analysis columns. The exact gzip CSV digest and all 49 compressed source-node digests are supplied. The north ROI uses first returns with original class 1, not an asserted NOAA building class. The horizontal mask and interval define the flat roof interior, not a cadastral edge.
- [2024 NYC orthophoto service](https://tiles.arcgis.com/tiles/yG5s3afENB5iO9fj/arcgis/rest/services/NYC_Orthos_2024/MapServer) locates visible station footprints; it is not evidence for identical roof construction in both years. The raw lat/lon-to-pixel mapping is in the replay script. The GLUCK+ architectural image checks the shape/relationship, not dimensional elevations.
- Entire scan source IDs 1135/1136 are omitted from the fit. 3,613 interval-selected observations from withheld scans were checked; median absolute vertical deviation is 0.04 m and p90 is 0.08 m. The height-band check is conditional and not total survey accuracy. With no Z band applied, 3,447 held-out first-return points inside the modeled control patch include 95.6% within 0.25 m of the deck and 4.4% higher features (signed residuals appear from small raised objects/edges; not classified as roof members). 97.5% of withheld band points are within the reduced outline plus 0.55 m. The scan split is genuine; the small inset was chosen after examining preliminary boundary contamination. Do not cite the 0.55 m coverage as a blind perimeter accuracy score.
- The geometry point-count is 13 vertices, 12 upward triangles, 12 intended exterior boundary edges, 12 two-face edges, no three-face edge. Data read back in Blender with validated geometry and matching ~873.51 m². Deliberately open surface; not a manifold building. Parapet, drains, thickness, walls, seam and materials excluded. The trial does not yet implement the annex as a verified shape.

## Which model changes these measurements support

| 2017 observed feature | Median elevations in metres NAVD88 | Existing FBX local elevations in metres |
| --- | --- | --- |
| North curved flat roof interior | 55.06 trial sample / 55.03 scan hold; fitted control 55.05 | 8.10–8.15 m shallow rear **rectangle**, not an established match |
| Broad low deck, two clean separate stations | both 60.74 on fit scans / 60.70 on held scans | 11.70–11.75 m broad modeled deck; precise alignment not yet proven |
| Two tier stations near tower plant perimeter | 83.14/83.17 fit, 83.10/83.13 hold | 43.20, 44.10 and 44.15 m trial planes; roof/parapet correspondence not yet established |
| Separate thin east cap | 85.55 fit / 85.52 hold | No individual match verified |
| Localized visibly higher plant (mixed returns) | east patch median 92.91 fit / 92.85 hold | 47.20 m single rectangular box does not capture these separate features |
| Front-plaza ground patch | 46.48 fit / 46.44 hold | Not a door, survey benchmark, or proved FBX origin |

The clean lower-to-upper survey-plane difference is roughly 22.4 m. The trial upper inner plane to the broad low deck is 32.4 m. This is a correspondence warning rather than a 10 m edit. The NYC OTI BIN 1084473 height (~40.35 m above its defined ground reference) is a different metric; the upper equipment returns are not grounds to apply or reject a single global scale. No heights were conflated or changed in the game candidate. Next: register architect/ortho plan and FBX with three physical plan correspondences plus a held XY corner. Confirm legal asset scope of curved northern element and independently constrain its walls, seam and floor references. Then make and compare near, mid and far candidates, bake and verify if changed, and run the CS2 Editor tests where compatible.

## Replay

`python3 build_north_roof_control.py uris-noaa-2017-sample.csv.gz` prints the exact OBJ and evidence as JSON (numpy, Pillow, pyproj, scipy). See the receipts for extraction source and expected hashes. No texture, placement, Editor, or release acceptance.
