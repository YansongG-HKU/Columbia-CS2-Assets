# St Paul's Chapel: three-LOD offline comparison candidate

Recovered and SHA-256/size checked the split near/mid bodies and window/glass submeshes plus texture maps from main `98587eeddab6ddf83a0c562efbf449207d633582`. Used the previously delivered west-portico/green-tile/copper-apse variant as LOD2, with neutral MaskMap, ControlMask and Emissive rather than mismatched UV maps. New distinct intake name; seven FBX Blender rereads retained the input coordinates, triangle indices and UVs and resolved referenced images in-folder. Body triangle counts 22,655 / 15,571 / 1,340; each existing near/mid body still has two near-zero-area triangles at threshold 1e-12 used in this run.

The base footprint is 32 × 48 m in all three; near/mid top is 35.30 m while both old and updated far top is 33.00 m. This 2.30 m discrepancy is pre-existing, and the far wall/lantern transitions and game materials have not passed. Offline medium/far projection IoU at 0/45/90°: 95.73% / 94.69% / 93.53%; not an in-game test. Fix the recognizable finial rather than scaling the whole mesh.

Whole ZIP `哥大-圣保罗礼拜堂-三档整栋对照候选-未游戏验收.zip`, SHA-256 `53bdd846317e60fe1c9af2315361c3171faacf2e31bd247d8a0b96f359279a8b`, 22,847,201 bytes; CRC and archive entries checked. No upload of binary files to the PR, no merge or publication, no Editor run.
