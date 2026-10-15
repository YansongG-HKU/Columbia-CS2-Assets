# Furnald Hall

`NA_FurnaldHall_8x5` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 8 x 5 cells (64 x 40 m) |
| Model bounds (incl. lot surface) | 64.0 x 40.0 x 32.65 m |
| Real reference | 49.6 x 19.4 m, 32.6 m, 10 levels (OSM way 274995731) |
| LOD0 tris (Base / Win / Gls) | 45646 / 589 / 112 |
| LOD1 tris (Base / Win / Gls) | 26002 / 589 / 112 |
| LOD2 tris | 32 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_FurnaldHall_8x5_Base | 45646 | 0 | 802 | 0 | 0 | 0 | 0 |
| NA_FurnaldHall_8x5_Win | 589 | 1167 | 0 | 0 | 0 | 0 | 289 |
| NA_FurnaldHall_8x5_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_FurnaldHall_8x5_LOD1_Base | 26002 | 0 | 638 | 0 | 0 | 0 | 0 |
| NA_FurnaldHall_8x5_LOD1_Win | 589 | 1167 | 0 | 0 | 0 | 0 | 289 |
| NA_FurnaldHall_8x5_LOD1_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_FurnaldHall_8x5_LOD2_Base | 32 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
