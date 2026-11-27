# St. Paul’s Chapel: far-LOD wall and foundation lighting (offline only)

Replace single source archive `577ca74d63cbe320287de784e4e893304e78c44b94acf72529e8ad237ecf10b2` with new mandatory A+B pair. A `232858766b8e7dd9a2aad770173ecdd7f3a291df1ed320a70c48d4212b73d99d` (5,650,434 bytes); B `c2b5ba7db9f35b23c57efa4dfd47146c8b389d435dc99da3f14f0680b528430f` (17,275,153 bytes). Import both from one isolated folder `StPaulsChapelTrial/`, 4×6. B contains the original five near/middle texture files unchanged; no binaries are in this draft.

Only FAR vertex-corner normals on 48 broad, rectilinear raw polys (144 corners) changed. They now match the wall/foundation faces, maximum deviation on target corners ~57.31° → 0.020°. Raw curve and upper assembly normals, previous two eave overlap corrections, 35.3 m apex, polygon order and UV unchanged. Unedited Blender corner change below 0.00009 vector units. Still 1,396 imported triangles, seven FBX, ten PNG, five shared texture links, other 17 runtime items exact. Four major light comparisons visibly changed; all four unlit and four emission pairs pixel-identical. Archive CRC and checksums verified.

Editor checks still open: low-angle lighting, eaves, near-far transitions, night, orientation and placement, and save/reopen. Geometry below grade was not trimmed in this batch. No real import, pmod or release.
