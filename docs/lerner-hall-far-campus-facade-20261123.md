# Lerner Hall: retain campus ramp cues at far distance

Continues [the near/mid trial](lerner-campus-glass-and-ramps-trial-20261123.md). Far uses the original 72-face opaque mesh; projected the current mid glazed/ramp daytime appearance onto only the two campus rectangle faces at Y=-31.5m, into their existing rotated UV rectangle. Patched 14,798 pixels inside [109,106,209,254) on 1024px BaseColor, including two-pixel pad; no other rasterized triangle intersects this patch. Outside pixels and every other file in the folder are identical, including mesh/UV, all near/mid, control and emissive maps. Kept local texture resolution and no new render pass/geometric complexity. Not a real transparency claim at far.

Blender CPU matched campus-side daytime preview: inside predeclared central crop, mean absolute RGB-channel difference against medium drops 65.0→7.5 (8-bit). Three representative ramp bands remain visible. No angle-dependent game/reflection or night calibration; verify actual glass and LOD switching in Editor, including night because the old emissive/control textures are intentionally unchanged. Game import, LFS and release still pending.

Whole ZIP `哥大-Lerner-Hall-整栋及三档坡道-未游戏验收.zip`, 10,282,250 bytes, SHA-256 `32d0ca947c1d17badd856020b6efb7fa7c8b0d955c467bb860448d989cebcbab`; CRC and expected 7 FBX/10 PNG verified.
