# Retain original: legacy LOD2 roof normal field, Nov 21 2026

A valid stitched surface with exact native corner vectors on untouched faces is not proof of invariant smooth lighting. In this source family the FBX reader normalizes new interpolated corner normals before drawing; the original interpolation formed combinations of the original outer corners and then normalized. Normalization and interpolation do not commute. We sampled interpolated **world-independent directions across matching visible surface positions**, not only retained vertices. The fit is an offline comparison, not official in-game thresholds.

| Test-only roof variant | Blender max / P95 angle difference | Disposition |
|---|---:|---|
| Uris Hall at +44.1 m | 7.126° / 5.506° | Withhold candidate; retain original LOD2 |
| Pupin Hall at +52.7 m vs preceding +49.8 m geometry patch | 5.713° / 4.008° | Do not adopt prior cumulative ZIP as final |
| Pupin Hall at +49.8 m vs original | 7.178° / 5.504° | Do not adopt preceding test patch as final |
| Dodge Hall at +22.8 m | 1.011° / 0.804° | Geometry study, hold against conservative P95 ≤ 0.3° gate |
| John Jay Hall at +43.36 m | 0.124° / 0.109° | Passed this local comparison only; other acceptance remains open |

Uris ref trial input FBX `3dde42a760068a4dd3319103035f527b7adadcd5392ffa97b7e0b85f33ff72bd`, trial-only output `87703156e4490d4354b3f58ec26251a164aec2f0bff601a4a9f647fabb5392a2` not delivered. 72→80 triangles, 108→120 paired edges and full model opposed positive-area pairs 28→24, UV max difference 1.58e−7, external ray positional max 0.0251 mm, 120,613 close-roof and 625 cleared internal rays. Independent native corner field compare used 87,870 matched points, max 7.128°, P95 5.500°, approximately X −15.0699 / local native depth 15.4068 m. Adaptive densification while keeping outline edges encountered 1,010 roof triangles and sampled max still 2.262°; rejected as not a viable LOD2 alternative. Neither file nor original canonical assets altered in this PR. Near/mid Uris model not replaced. For later repairs, add a cross-surface normal-direction comparison, use exact seam with suitable surface provenance or re-bake as an intentionally redesigned look, not a silent fix, and do not treat offline proof as CS2 Editor acceptance.
