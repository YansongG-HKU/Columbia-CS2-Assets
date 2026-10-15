# Lewisohn Hall

`NA_LewisohnHall_6x4` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | x |
| Model bounds (incl. lot surface) | 48.0 x 32.0 x 25.85 m |
| Real reference | x |
| LOD0 tris (Base / Win / Gls) | 28946 / 431 / 112 |
| LOD1 tris (Base / Win / Gls) | 18470 / 431 / 112 |
| LOD2 tris | 96 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_LewisohnHall_6x4_Base | 28946 | 4 | 666 | 0 | 0 | 0 | 0 |
| NA_LewisohnHall_6x4_Win | 431 | 851 | 0 | 0 | 0 | 0 | 210 |
| NA_LewisohnHall_6x4_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_LewisohnHall_6x4_LOD1_Base | 18470 | 4 | 566 | 0 | 0 | 0 | 0 |
| NA_LewisohnHall_6x4_LOD1_Win | 431 | 851 | 0 | 0 | 0 | 0 | 210 |
| NA_LewisohnHall_6x4_LOD1_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_LewisohnHall_6x4_LOD2_Base | 96 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
