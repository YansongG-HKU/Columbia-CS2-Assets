# Columbia CS2 Assets

Cities: Skylines II building assets of Columbia University's Morningside Heights campus, modelled procedurally in Blender
to a common standard: real dimensions (1 unit = 1 m), detailed facades, full PBR texture set (`_BaseColor`, `_Normal`,
`_MaskMap`, `_ControlMask`, `_Emissive`), LOD0/LOD1/LOD2, Base/Win/Gls sub-meshes, CS2 window UV grid, `settings.json`,
FBX (Forward -Z, Up Y), lots sized in 8 m cells, names `NA_<Name>_<WxD>`.

| Building | Folder | Asset | Lot |
|---|---|---|---|
| Low Memorial Library | [LowMemorialLibrary](LowMemorialLibrary) | NA_ColumbiaLowLibrary_13x10 | 13x10 |
| Butler Library | [ButlerLibrary](ButlerLibrary) | NA_ButlerLibrary_11x7 | 11x7 |
| St. Paul's Chapel | [StPaulsChapel](StPaulsChapel) | NA_StPaulsChapel_4x6 | 4x6 |
| Philosophy Hall | [PhilosophyHall](PhilosophyHall) | NA_PhilosophyHall_6x4 | 6x4 |
| Kent Hall | [KentHall](KentHall) | NA_KentHall_8x4 | 8x4 |
| Avery Hall | [AveryHall](AveryHall) | NA_AveryHall_6x4 | 6x4 |
| Hamilton Hall | [HamiltonHall](HamiltonHall) | NA_HamiltonHall_8x4 | 8x4 |
| John Jay Hall | [JohnJayHall](JohnJayHall) | NA_JohnJayHall_8x4 | 8x4 |

Each folder: `fbx/` (combined LOD FBX + `split/` per sub-mesh), `textures/`, `settings.json`, `<asset>.blend`,
`renders/` (day, aerial, close-up, night, LOD comparisons), `SOURCES.txt`, README with specs and mesh checks.

## Credits
- Low Memorial Library includes the "Alma Mater" 3D scan by **mkturkcan**, licensed under
  [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/) -
  https://sketchfab.com/3d-models/alma-mater-cdf8f9aef6354ee49c7cf801176d8a44 (modified: cleaned, re-oriented, scaled,
  decimated, re-textured as procedural bronze). Original sculpture by Daniel Chester French (1903).
- Footprints/heights: (c) OpenStreetMap contributors (ODbL). Other references listed per building.
- All other geometry and textures are procedurally generated for this project.
