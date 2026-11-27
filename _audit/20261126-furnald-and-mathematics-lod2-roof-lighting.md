# Furnald and Mathematics Hall: hard-edge LOD2 lighting

Offline only; keep existing footprint, alignment and prior hidden-plane seam corrections. Import each asset separately, do not mix old/new packages. ZIP checksums, CRC, shared map paths, and exact Blender geometry, index and UV hashes checked.

- Furnald: `FurnaldTrial/`, 8×5, ZIP SHA-256 `7ee56e68bd882119af1fb54dfb805eb7ee736e5237ad0d450bfe9a1f5c8b25fb` (8,389,377 bytes), replaces `a465cb6721f7242ffbcdd4d9e574a88fce79d73df132f2b934d74a8f4d97c454`.
- Mathematics: `MathematicsTrial/`, 7×5, ZIP SHA-256 `6c7169ad00097b6e31ee037e2ecdca2df14516b5e2860c1ed31e7d6faba12a2e` (10,661,687 bytes), replaces `46eb7adb56b953a244145ef936bda8ba1c6d1a03c18d9d1312e466548ea90d04`.

Each LOD2 still has 36 triangles. Split corner normals and tangent frames for planar façades and pitched roof facets replace the smoothed vertex normals which produced curved bright bands. Each asset's 17 other import files, maps, geometry and UV untouched. Four textured Blender lighting pairs per asset visible and four unlit/four emission pairs per asset pixel-identical. This is not the old ring topology experiment or a new roof shape. Inspect at true switching distance in Editor, especially roof/eaves, dormer simplification, material by day/night, collision and save/reopen. No model binaries in PR, no Editor run, no pmod or publication.
