# St.

`NA_StPaulsChapel_4x6` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 4 x 6 cells (32 x 48 m) |
| Model bounds (incl. lot surface) | 32.0 x 48.0 x 35.35 m |
| Real reference | 43.3 x 24.9 m footprint, 35.3 m to lantern finial (OSM way 274995768); dome 91 ft / 27.7 m |
| LOD0 tris (Base / Win / Gls) | 22655 / 423 / 12 |
| LOD1 tris (Base / Win / Gls) | 15571 / 423 / 12 |
| LOD2 tris | 616 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_StPaulsChapel_4x6_Base | 22655 | 567 | 1603 | 1 | 0 | 0 | 0 |
| NA_StPaulsChapel_4x6_Win | 423 | 499 | 0 | 0 | 0 | 0 | 38 |
| NA_StPaulsChapel_4x6_Gls | 12 | 14 | 0 | 0 | 0 | 0 | 1 |
| NA_StPaulsChapel_4x6_LOD1_Base | 15571 | 567 | 1339 | 1 | 0 | 0 | 0 |
| NA_StPaulsChapel_4x6_LOD1_Win | 423 | 499 | 0 | 0 | 0 | 0 | 38 |
| NA_StPaulsChapel_4x6_LOD1_Gls | 12 | 14 | 0 | 0 | 0 | 0 | 1 |
| NA_StPaulsChapel_4x6_LOD2_Base | 616 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
