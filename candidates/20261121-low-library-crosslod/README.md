# Low Memorial Library | Combined LOD0, LOD1 and LOD2 crown trial
Cloud batch at 02:30 UTC, 2026-11-21. This trial supersedes the previous 02:00 single-LOD2 candidate for cross-LOD comparisons, without replacing production files.

## What was repaired
- LOD0 and LOD1: the same eight measured-profile dome rings were raised 0.260–0.701 m; 768 vertices and 5,184 transported corner frames per tier. The inner taper is monotonic across unchanged boundaries; the raised shoulder at radius 11.832 m uses a separate measured annulus (199 fit points and 104 held checks). Their 108,415 and 50,407 triangular faces, original XY/height bounds, material assignment, and UV corners are unchanged. A trial that also moved the innermost substrate ring added 60 intersections with the lantern; it was rejected. The accepted candidate leaves that ring, lantern and trim untouched.
- LOD2: from the already-seam-repaired and 02:00 reshaped version, the existing 24-vertex shoulder ring near radius 11.72 m was raised 0.690 m. It stays at 736 triangles, with the toe, seam, lower drum and peak unchanged. From the 02:00 baseline versus the pre-survey closed annulus, three rings were moved in total. Target elev. 82.59 m NAVD88 from 185 training returns in eight populated sectors; 114 independent returns at the new radius have median 82.545 m. Scope is this matched shoulder ring, not the outer toe/platform.

## What passed offline
All six FBXs were loaded one by one with automatic image search off; all imported texture nodes decoded, and all five exact-file PNGs per texture set were also checked. No new non-adjacent triangle intersection candidates in the dome-region scan and none touching moved faces; other pre-existing dome-component contacts and historical architectural detail are not qualified by this test. No mesh topology edits.
3929 independent point measurements reused (NOAA 2017 EPT 9306, separate flight passes 1135 and 1136). Near and mid rays agree exactly at these positions. Each tier is evaluated against a shared crown-fitted offset; no independent scaling or shifting of tiers or claim about grade.
- LOD0/LOD1 error p50/p90/p95: 0.648/0.791/0.836 → 0.117/0.475/0.639 m.
- LOD2 error p50/p90/p95, closed but uncalibrated annulus predecessor → current: 0.771/0.953/1.003 → 0.102/0.268/0.319 m.
- Gap between near/mid and far in unshifted game coordinates, 02:00 snapshot → this batch: 0.489/0.654/0.669 → 0.161/0.486/0.622 m; the pre-survey pair (both using older approximations) was 0.162/0.228/0.296 m.
- Outer 10.50–11.42 m near/mid versus far: with near/mid alone 0.583/0.644/0.671 m, then with the LOD2 shoulder correction 0.104/0.166/0.184 m. The near/mid lantern still distinguishes it from LOD2; this is not a full game-switch pass.

## Trial parts and limits
Extract both ZIPs into the same new folder. The two packages use the same `Low-Library-LOD-Trial/` root. FBXs and their PNG files must be side by side in `LOD-assets/`. The shared near and mid texture bank is supplied separately from the geometry and the five far textures. Validate each SHA256SUMS file after extraction. Original source files remain intact. 
Lighting and color frames use Blender with BaseColor and Normals; material channel wiring in CS2 Editor, import, effective switch screens, grade/entrance, interior, full geometry and texture spec are still not certified. No PDX release, Git LFS upload, main modification, or Windows testing. Figures are local shape checks, not a whole-building survey.
