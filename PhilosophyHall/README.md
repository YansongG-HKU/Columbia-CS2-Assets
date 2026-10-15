# Philosophy Hall

`NA_PhilosophyHall_6x4` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 6 x 4 cells (48 x 32 m) |
| Model bounds (incl. lot surface) | 48.0 x 32.0 x 29.05 m |
| Real reference | 44.9 x 18.5 m, 29.0 m (OSM); NRHP 145 x 65 ft, 8 storeys |
| LOD0 tris (Base / Win / Gls) | 43254 / 527 / 112 |
| LOD1 tris (Base / Win / Gls) | 24282 / 527 / 112 |
| LOD2 tris | 96 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_PhilosophyHall_6x4_Base | 43254 | 20 | 924 | 0 | 0 | 0 | 0 |
| NA_PhilosophyHall_6x4_Win | 527 | 999 | 0 | 0 | 0 | 0 | 236 |
| NA_PhilosophyHall_6x4_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_PhilosophyHall_6x4_LOD1_Base | 24282 | 20 | 804 | 0 | 0 | 0 | 0 |
| NA_PhilosophyHall_6x4_LOD1_Win | 527 | 999 | 0 | 0 | 0 | 0 | 236 |
| NA_PhilosophyHall_6x4_LOD1_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_PhilosophyHall_6x4_LOD2_Base | 96 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
