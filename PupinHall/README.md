# Pupin Hall

`NA_PupinHall_8x3` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 8 x 3 cells (64 x 24 m) |
| Model bounds (incl. lot surface) | 64.0 x 24.0 x 56.7 m |
| Real reference | 55.4 x 16.2 m slab + 2 end pavilions (OSM way 738973812); 15 storeys (CU); height ~50 m estimated |
| LOD0 tris (Base / Win / Gls) | 54436 / 1164 / 112 |
| LOD1 tris (Base / Win / Gls) | 45448 / 1164 / 112 |
| LOD2 tris | 84 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_PupinHall_8x3_Base | 54436 | 0 | 1180 | 0 | 0 | 0 | 0 |
| NA_PupinHall_8x3_Win | 1164 | 2328 | 0 | 0 | 0 | 0 | 582 |
| NA_PupinHall_8x3_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_PupinHall_8x3_LOD1_Base | 45448 | 0 | 1180 | 0 | 0 | 0 | 0 |
| NA_PupinHall_8x3_LOD1_Win | 1164 | 2328 | 0 | 0 | 0 | 0 | 582 |
| NA_PupinHall_8x3_LOD1_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_PupinHall_8x3_LOD2_Base | 84 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
