# Kent Hall

`NA_KentHall_8x4` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 8 x 4 cells (64 x 32 m) |
| Model bounds (incl. lot surface) | 64.7 x 32.0 x 25.65 m |
| Real reference | 62.5 x 16.7 m + 15.6 x 3.8 m projection, 25.6 m (OSM) |
| LOD0 tris (Base / Win / Gls) | 34836 / 505 / 112 |
| LOD1 tris (Base / Win / Gls) | 21288 / 505 / 112 |
| LOD2 tris | 108 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_KentHall_8x4_Base | 34836 | 4 | 736 | 0 | 0 | 0 | 0 |
| NA_KentHall_8x4_Win | 505 | 999 | 0 | 0 | 0 | 0 | 247 |
| NA_KentHall_8x4_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_KentHall_8x4_LOD1_Base | 21288 | 4 | 620 | 0 | 0 | 0 | 0 |
| NA_KentHall_8x4_LOD1_Win | 505 | 999 | 0 | 0 | 0 | 0 | 247 |
| NA_KentHall_8x4_LOD1_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_KentHall_8x4_LOD2_Base | 108 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
