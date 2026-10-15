# Uris Hall

`NA_UrisHall_6x9` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 48 × 72 m |
| Model bounds (incl. lot surface) | 48.0 x 72.0 x 47.25 m |
| Real reference | 47.2 × 68.6 m footprint, 12 storeys |
| LOD0 tris (Base / Win / Gls) | 8958 / 128 / 72 |
| LOD1 tris (Base / Win / Gls) | 5886 / 128 / 72 |
| LOD2 tris | 72 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_UrisHall_6x9_Base | 8958 | 0 | 187 | 0 | 0 | 0 | 0 |
| NA_UrisHall_6x9_Win | 128 | 256 | 0 | 0 | 0 | 0 | 53 |
| NA_UrisHall_6x9_Gls | 72 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_UrisHall_6x9_LOD1_Base | 5886 | 0 | 187 | 0 | 0 | 0 | 0 |
| NA_UrisHall_6x9_LOD1_Win | 128 | 256 | 0 | 0 | 0 | 0 | 53 |
| NA_UrisHall_6x9_LOD1_Gls | 72 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_UrisHall_6x9_LOD2_Base | 72 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
