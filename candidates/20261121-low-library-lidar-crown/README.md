# Low Memorial Library | Survey-supported LOD2 crown correction
2026-11-21 02:00 UTC cloud batch. Non-destructive, LOD2 only. Not an Editor-verified or full building release.

## Change
Raised existing 24-vertex rings at nominal radii 4.60 m and 8.82 m by 0.699 m and 0.676 m; the apex, drum, previously repaired annular seam, and all other parts are unchanged. Triangles remain 736. Used 2014 NYC OTI CityGML (BIN 1084472, DOITT ID 551695) for plan center and NOAA 2017 3DEP LiDAR (NOAA EPT ID 9306, GEOID18) for shape. Fit source IDs 1063, 1064, 1065, 1134; check IDs 1135 and 1136 were never used to fit. Crown centers and apex heights are paired for comparisons, not whole-building vertical registration. Standalone 23 m diameter study and its 82.00 m NAVD88 synthetic lower cap are not part of the game model. Point cloud evidence does not constrain the outer crown toe or drum, nor the entry, grade, building volume, interior, stairs or 2026 plaza work.

## Independent verification
3929 held first-return measurements inside 11.42 m. Vertical absolute p50/p90/p95 of the **FBX**: 0.771/0.952/1.002 m to 0.153/0.658/0.763 m following patch. Standalone isolated survey mesh: 0.073/0.188/0.226 m, but it does not meet the LOD2 triangle budget. Both game FBXs have 428 vertices, 736 triangles, 1104 oriented paired edges, identical bounds and 2208 exact UV corners; five 1024 px texture files read back byte-for-byte unchanged. All 432 touched tangent frames were locally transported and orthonormalized with handedness unchanged. No new non-adjacent triangle pairs or affected crown intersections; 307 pre-existing broadphase+triangle pairs in the unchanged rest of the game asset remain investigation items, not classified as 307 proven physical penetrations. Same-camera renders use BaseColor plus tangent normal.

## Trial as delivered
The six FBX/PNG files in `LOD2-trial/` must stay together. Do not rename or replace any production game asset based on this test by itself. Pairing with LOD0/LOD1, silhouette switch tests, photomatch at the actual site, full PBR/CS2 material wiring, interactions and Paradox CS2 Editor import still require verification; Blender reads FBX version 7400 and cannot certify any Editor target version. 
The scripts fit the crown, reproduce the modified FBX using Blender 4.3 and the previously closed-annulus FBX pinned by checksum, and independently reimport both to verify. The held calibration sample is included in the trial ZIP. Source for replay is the previously repaired/texture-atlas asset, not main or the original open annulus. For the full fit, follow NOAA extraction scripts and receipt crop then `old.py` for the Blender-transformed prior geometry; `fit.py` requires the three named inputs and produces the held rays.

Primary sources:
- https://operations.cufo.columbia.edu/content/low-library
- https://maps.nyc.gov/download/3dmodel/DA_WISE_GML.zip
- https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9306/ept.json
