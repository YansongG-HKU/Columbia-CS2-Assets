# Havemeyer Hall

`NA_HavemeyerHall_8x8` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 8 x 8 cells (64 x 64 m) |
| Model bounds (incl. lot surface) | 65.1 x 64.0 x 38.95 m |
| Real reference | 48.8 x 62.9 m, 38.9 m (OSM way 274995734) |
| LOD0 tris (Base / Win / Gls) | 79410 / 935 / 112 |
| LOD1 tris (Base / Win / Gls) | 46650 / 935 / 112 |
| LOD2 tris | 160 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_HavemeyerHall_8x8_Base | 79410 | 0 | 1605 | 0 | 0 | 0 | 0 |
| NA_HavemeyerHall_8x8_Win | 935 | 1793 | 0 | 0 | 0 | 0 | 429 |
| NA_HavemeyerHall_8x8_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_HavemeyerHall_8x8_LOD1_Base | 46650 | 0 | 1277 | 0 | 0 | 0 | 0 |
| NA_HavemeyerHall_8x8_LOD1_Win | 935 | 1793 | 0 | 0 | 0 | 0 | 429 |
| NA_HavemeyerHall_8x8_LOD1_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_HavemeyerHall_8x8_LOD2_Base | 160 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
