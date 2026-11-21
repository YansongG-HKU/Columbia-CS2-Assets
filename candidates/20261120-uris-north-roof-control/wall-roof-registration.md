# Uris Hall: wall-to-roof orientation, dated observations

**Orientation is resolved.** In [Blaer & Allen (2009), Figs. 14–17](https://www.cs.columbia.edu/~allen/PAPERS/blaer_jfr2009.pdf#page=16), the elevated photo and final scan show the curved north frontage, with the thin tower behind it. Fig. 14's diagram is inverted relative to conventional north-up for this block: its curved end is at the bottom, the NBV 1 marker is at the opposite straight end. Fig. 16's *head-on straight entrance* and paired frontal windows are from that opposite side. The [GLUCK+ site plan and 1986 addition](https://gluckplus.com/project/columbia-university-business-school-addition/) show the curved component at the far side, and place the limestone entrance mask opposite the Low Library rotunda. Its ground and second floor drawings document the straight mask and are not construction drawings for the rear arc. The 2024 NYC ortho and independent 2017 NOAA 9306 roof points both show the arc on the north/up side of the map. This rules out transferring an arch to the addition's south windows.

**What the data constrain.** A circle fitted in EPSG:6347 to the outer 97th-percentile envelope of the flat roof-band samples in 45 columns gives radius 22.39 m and center **587624.3011 E, 4518100.1849 N**. Vertices are a *roof-return envelope*, not wall faces: held scan IDs 1135/1136 gave absolute radial error median 0.343 m, p90 0.879 m, max 1.111 m over the same 45 transverse columns. An ellipse reduced training spread slightly but no clear gain on held scans; the center/radius are coarse layout controls only. No other façade coordinates were inferred from the undimensioned paper. Do not round this into the outer wall radius, quantize the mullion spacing, or force a curve through the shoulders; fit the two wall ends separately when evidenced.

**North-side ground controls.** The 13×13-pixel class-2 samples in the already-pinned 2024 ortho transform are:

| Station pixel (x,y) | 2017 NAVD88 m, training / held scan median | train / held count |
| --- | --- | --- |
| Northwest stair vicinity (465,144) | 47.335 / 47.335 (mixed steps) | 14 / 6 |
| NW flank (505,111) | 47.010 / 47.005 | 36 / 20 |
| North apex exterior (580,83) | 47.210 / 47.190 | 22 / 11 |
| NNE paving (644,100) | 47.190 / 47.170 | 30 / 18 |
| East outside (695,148) | 47.850 / 47.845 (sparse) | 5 / 4 |
| ESE (709,225) | no class-2 observations | 0 / 0 |
| South plaza reference (450,459) | 46.460 / 46.430 | 29 / 29 |

The well-covered north controls imply roughly 7.84–8.05 m from adjacent paving to the fitted 55.05-m roof, versus about 8.6 m at the remote south comparator. These are station distances, not a surveyed wall base, floor or doorway. The source article says parts of the roof were missed by its ground scans; no raw Uris scan download was established. The published diagrams support visual correspondence, not transplanting their image pixels as measured dimensions. This does not change the asset files.

Local reference PDF SHA256: `306865353835fda352ec1905d17062963cf438018e73eedece3a87e325ea9994`. Reproducible optional fit print: `python3 sample_roof_arc.py uris-cropped-ept.npz`.
