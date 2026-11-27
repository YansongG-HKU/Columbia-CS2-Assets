# Lewisohn, Philosophy and Fayerweather Halls — LOD2 hard-plane lighting

Four pinned candidates screened with seven geometric perspectives and four textured mid/far views. Avery Hall showed intentional thin-detail simplification rather than the large lighting defect and was not edited. In the other three, a smooth normal fan across masonry/roof/approach hard edges makes the surfaces appear rounded at distance. Corrected the affected face-corner normals, tangent frames and smoothing flags only.

| Asset | Corrected triangles / LOD2 | Source package SHA-256 | Candidate package SHA-256 | LOD2 FBX SHA-256 |
| --- | --- | --- | --- | --- |
| Lewisohn Hall | 92 / 92 | `a8ed6508002b217e56eb870d7709dc2f08edafc78e1efc3378b0cb675f10d162` | `bc599d4d5ae482b1b3a1f2a69df8fc3836aaf35b360dc6bab217303af2f2ab75` | `03e2077a8d5a218406466969b10b5f62c71ec568ce8bda05d516edf5aef5abbe` |
| Philosophy Hall | 80 / 408 | `a0e232d90061da9d66c64e79d480da354578282a8310925cbc89df842d34787c` | `d421d30a57346b07cc74e96aeafb47d0b8cb8bc0ddca9d22143f1e4561af2953` | `aa1803726713cf3927dd2559711e24707bb92561ac5ae5a09abf69cd583150cc` |
| Fayerweather Hall | 96 / 336 | `1b1649756f412403a4275e84a408b86c949917bb1e619bb3d6a1e78c8e96d743` | `4ac834ffd5ee580c7d46d65361558e69b9d7d6ee58f27d6280287a2146700fb0` | `07530884ae2c5c0d69e2c182bb760ac3da515466f64961346cf56795f8bdf6df` |

Geometry, topology, UV, placements and all texture bytes unmodified. Unaffected detail normals after import unchanged within 1e-6. Across each asset, matched three textured Workbench views show correction; three flat RGB and three emissive map samples each compare pixel-exact. No changes to Lewisohn access geometry, Philosophy main steps/double lights, Fayerweather oval-window pieces. Candidate archives each include a comparison and checksums. No Editor, collision, pedestrian, nighttime-in-game or save/reopen check, no .pmod, no release.
