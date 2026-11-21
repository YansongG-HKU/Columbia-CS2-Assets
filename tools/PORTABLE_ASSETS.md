# Conservative portable delivery helper

Run with Blender Python (tested Blender 4.3.2), not ordinary Python:

```sh
blender -b --factory-startup --python-exit-code 1 --python prepare_portable_assets.py -- \
  --repository ./repository --output ./portable --clean ./readback \
  --buildings AveryHall,LewisohnHall
```

Both output directories must be new and outside the source repository. Supply a comma-separated building list. Each input building must contain one `.blend`, `textures/*.png`, `cs2_import_candidates/*.fbx`, and `settings.json`.

This script copies only the selected split exports, original PNGs, settings, editable blend and available source notes. It does not delete or modify repository inputs. It neither downsamples nor merges texture atlases, and it does not optimize or repair geometry. Main/LOD1 sharing already encoded in settings stays unchanged.

Source blend image paths become relative references to the corresponding import-assets directory. In the copied FBXs, only FileName/Filename/RelativeFilename properties become same-directory texture basenames. Binary FBXs are decoded and reserialized at their original version; every decoded node and typed property, including version, must match the expected tree after the explicit path changes. No Autodesk profile or CS2 importer certification is implied.

Outputs include geometry/UV hashes and triangle counts (`verification.json`), per-FBX intended path edits and decoded-tree digests (`fbx_path_changes.json`), clean-directory no-search FBX and source-image loading checks (`clean_path_verification.json`), source-vs-import triangle count discrepancies (`source_to_fbx_count_differences.json`), and SHA256 payload manifest (`manifest.json`). Do not confuse a successful portable readback with geometry correctness. An explicit discrepancy report remains a blocker requiring review.

Smoke test: AveryHall + LewisohnHall, 14 FBXs and both source blends loaded from fresh directories; payload manifest has 42 files. LewisohnHall LOD1 still records source 16,788 versus imported 16,780 triangles. The existing eight collapsed/reversed groups were not fixed. Six earlier before/after Blender render pairs had exact RGBA equality; this helper does not rerender by default.

This is a file-layout/portability tool, not a texture-memory optimization. Identical selected payloads can be slightly larger after path serialization. Do not advertise omission of historical exports, preview renders or editable sources as lossless texture savings.
