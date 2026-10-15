# Alfred Lerner Hall

`NA_LernerHall_9x9` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 9 x 9 cells (72 x 72 m) |
| Model bounds (incl. lot surface) | 72.0 x 72.0 x 37.45 m |
| Real reference | 63.6 x 45.8 m + Broadway wing, 33.8 m (OSM way 274995718); Tschumi 1999 |
| LOD0 tris (Base / Win / Gls) | 30084 / 958 / 0 |
| LOD1 tris (Base / Win / Gls) | 23520 / 958 / 0 |
| LOD2 tris | 72 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_LernerHall_9x9_Base | 30084 | 226 | 1892 | 0 | 0 | 0 | 0 |
| NA_LernerHall_9x9_Win | 958 | 1916 | 0 | 0 | 0 | 0 | 465 |
| NA_LernerHall_9x9_LOD1_Base | 23520 | 226 | 1892 | 0 | 0 | 0 | 0 |
| NA_LernerHall_9x9_LOD1_Win | 958 | 1916 | 0 | 0 | 0 | 0 | 465 |
| NA_LernerHall_9x9_LOD2_Base | 72 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
