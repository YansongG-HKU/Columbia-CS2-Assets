# Mathematics Hall

`NA_MathematicsHall_7x5` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 7 x 5 cells (56 x 40 m) |
| Model bounds (incl. lot surface) | 56.0 x 40.0 x 26.25 m |
| Real reference | 45.4 x 17.1 m, 26.2 m (OSM way 274995760); entrance inscribed MATHEMATICS |
| LOD0 tris (Base / Win / Gls) | 33680 / 361 / 112 |
| LOD1 tris (Base / Win / Gls) | 19498 / 361 / 112 |
| LOD2 tris | 32 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_MathematicsHall_7x5_Base | 33680 | 136 | 538 | 4 | 0 | 0 | 0 |
| NA_MathematicsHall_7x5_Win | 361 | 711 | 0 | 0 | 0 | 0 | 175 |
| NA_MathematicsHall_7x5_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_MathematicsHall_7x5_LOD1_Base | 19498 | 0 | 410 | 0 | 0 | 0 | 0 |
| NA_MathematicsHall_7x5_LOD1_Win | 361 | 711 | 0 | 0 | 0 | 0 | 175 |
| NA_MathematicsHall_7x5_LOD1_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_MathematicsHall_7x5_LOD2_Base | 32 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
