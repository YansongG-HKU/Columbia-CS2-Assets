# Low Memorial Library

`NA_ColumbiaLowLibrary_13x10` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 13 x 10 cells (104 x 80 m) |
| Model bounds (incl. lot surface) | 104.0 x 80.0 x 43.57 m |
| Real reference | building ~60 x 60 m (OSM 60.8 x 59.5), dome top ~41 m above terrace |
| LOD0 tris (Base / Win / Gls) | 108415 / 210 / 16 |
| LOD1 tris (Base / Win / Gls) | 50407 / 210 / 16 |
| LOD2 tris | 726 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_ColumbiaLowLibrary_13x10_Base | 108415 | 1661 | 700 | 4 | 0 | 0 | 0 |
| NA_ColumbiaLowLibrary_13x10_Win | 210 | 348 | 0 | 0 | 0 | 0 | 69 |
| NA_ColumbiaLowLibrary_13x10_Gls | 16 | 20 | 0 | 0 | 0 | 0 | 1 |
| NA_ColumbiaLowLibrary_13x10_LOD1_Base | 50407 | 1377 | 700 | 0 | 0 | 0 | 0 |
| NA_ColumbiaLowLibrary_13x10_LOD1_Win | 210 | 348 | 0 | 0 | 0 | 0 | 69 |
| NA_ColumbiaLowLibrary_13x10_LOD1_Gls | 16 | 20 | 0 | 0 | 0 | 0 | 1 |
| NA_ColumbiaLowLibrary_13x10_LOD2_Base | 726 | 8 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
