import tempfile
import unittest
from pathlib import Path

from portable_asset_layout import find_inputs


class LayoutTests(unittest.TestCase):
    def test_preflight_cases(self):
        for case in ("valid", "no_blend", "two_blends", "no_png", "no_fbx",
                     "missing_settings", "zero_bytes", "duplicate_name",
                     "out_of_tree", "unsafe_name"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                parent = Path(tmp)
                repo = parent / "repo"
                building = repo / "Asset"
                fbx = building / "cs2_import_candidates"
                png = building / "textures"
                fbx.mkdir(parents=True)
                png.mkdir()
                (building/"asset.blend").write_bytes(b"one")
                (building/"settings.json").write_text("{}")
                (fbx/"b.fbx").write_bytes(b"b")
                (fbx/"a.fbx").write_bytes(b"a")
                (png/"base.png").write_bytes(b"png")
                names = ["Asset"]
                if case == "no_blend":
                    (building/"asset.blend").unlink()
                if case == "two_blends":
                    (building/"other.blend").write_bytes(b"two")
                if case == "no_png":
                    (png/"base.png").unlink()
                if case == "no_fbx":
                    for f in fbx.iterdir():
                        f.unlink()
                if case == "missing_settings":
                    (building/"settings.json").unlink()
                if case == "zero_bytes":
                    (fbx/"a.fbx").write_bytes(b"")
                if case == "duplicate_name":
                    names *= 2
                if case == "unsafe_name":
                    names = ["../Asset"]
                if case == "out_of_tree":
                    external = parent/"elsewhere.fbx"
                    external.write_bytes(b"not a local staging input")
                    (fbx/"b.fbx").unlink()
                    (fbx/"b.fbx").symlink_to(external)
                if case == "valid":
                    self.assertEqual([p.name for p in find_inputs(repo,names)["Asset"][2]], ["a.fbx","b.fbx"])
                else:
                    with self.assertRaises(ValueError):
                        find_inputs(repo,names)

if __name__ == "__main__":
    unittest.main()
