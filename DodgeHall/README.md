# Dodge Hall

`NA_DodgeHall_9x5` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 9 x 5 cells (72 x 40 m) |
| Model bounds (incl. lot surface) | 72.0 x 40.0 x 25.65 m |
| Real reference | 62.9 x 18.6 m, 25.6 m (OSM way 274995789) |
| LOD0 tris (Base / Win / Gls) | 37120 / 488 / 276 |
| LOD1 tris (Base / Win / Gls) | 22240 / 488 / 276 |
| LOD2 tris | 56 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_DodgeHall_9x5_Base | 37120 | 4 | 744 | 0 | 0 | 0 | 0 |
| NA_DodgeHall_9x5_Win | 488 | 954 | 0 | 0 | 0 | 0 | 233 |
| NA_DodgeHall_9x5_Gls | 276 | 0 | 0 | 0 | 0 | 0 | 5 |
| NA_DodgeHall_9x5_LOD1_Base | 22240 | 4 | 648 | 0 | 0 | 0 | 0 |
| NA_DodgeHall_9x5_LOD1_Win | 488 | 954 | 0 | 0 | 0 | 0 | 233 |
| NA_DodgeHall_9x5_LOD1_Gls | 276 | 0 | 0 | 0 | 0 | 0 | 5 |
| NA_DodgeHall_9x5_LOD2_Base | 56 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
