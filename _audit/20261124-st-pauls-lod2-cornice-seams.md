# St. Paul's Chapel LOD2: two cornice seams (offline)

Retain the 4×6 base, west portico and 35.3 m finial trial. Both overlapping cornice spans, on the +Y-facing returns near y−16.18 and −16.17, had 20 mm and 30 mm of duplicate same-facing surface over about 18.92 and 18.74 m respectively. Before trimming, their UVs sampled different existing atlas colors. Close the gap in the asset's intended layered profile by raising the lower plane of each narrower box exactly to its supporting box's top, with no change to supports or intended exterior envelope. Preserve all quads, edge indices, normal and material arrays; UV on the shortened side faces is linearly clipped, not re-baked. No geometry from other tiers altered.

- Removed exactly 0.940595 m² of same-facing overdraw. Two closed boxes remain, underside contact is backed by the supporting box. 1,396 triangles as before. 1,006 untouched polygons. Only eight vertex positions and sixteen UV corners changed.
- Eight view directions, 112,000 rays per model, 27,643 paired first hits; same hit or miss per sample with max 0.023 mm delta. Both repaired strips 11,046 local 2→1 directed reproductions. Full package Blender reload of seven FBX; ten PNG maps preserved byte for byte. Near/mid keep old issue list; no gratuitous geometry/UV changes.
- Input ZIP SHA-256 0e9d36591e3315d9ceb69e083c5e47804a4f67432636e2244adb133bba9bbd2c.
- Repaired far FBX SHA-256 2b01193687aa79c8c1f2a4260ac31abb5e56e3da79bfca41a2853fd0396253a0.
- Verified whole offline ZIP: 哥大-圣保罗礼拜堂-两条远景檐线去重整栋-未游戏验收.zip, 22,842,346 bytes, SHA-256 577ca74d63cbe320287de784e4e893304e78c44b94acf72529e8ad237ecf10b2. This is the same candidate count. Notes/readback only in this draft, no binary pushes.
- No functional CS2 Editor in this cloud check. GPU flicker or mip behavior, import, placement, visibility by tier and publish all remain unverified.
