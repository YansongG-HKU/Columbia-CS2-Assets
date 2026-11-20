"""Validate staging inputs without importing Blender or creating outputs."""
from pathlib import Path

def find_inputs(repository, names):
    repository = Path(repository).resolve(strict=True)
    if not repository.is_dir():
        raise ValueError(f"Not an asset repository directory: {repository}")
    if not names or len(set(names)) != len(names):
        raise ValueError("Choose a nonempty list of unique building names")
    inputs = {}
    for name in names:
        if not name or name in ('.', '..') or '/' in name or '\\' in name:
            raise ValueError(f"Invalid building name: {name!r}")
        root = repository / name
        if not root.is_dir() or not root.resolve().is_relative_to(repository):
            raise ValueError(f"{name}: missing building directory or outside repository")
        paths = (
            sorted(root.glob("*.blend")),
            sorted((root / "textures").glob("*.png")),
            sorted((root / "cs2_import_candidates").glob("*.fbx")),
            [root / "settings.json"],
        )
        blend, png, fbx, settings = paths
        if len(blend) != 1:
            raise ValueError(f"{name}: expected exactly one .blend, found {len(blend)}")
        if not png or not fbx:
            raise ValueError(f"{name}: expected nonempty textures/*.png and cs2_import_candidates/*.fbx")
        for group in paths:
            for path in group:
                if not path.is_file() or not path.resolve().is_relative_to(root.resolve()) or path.stat().st_size == 0:
                    raise ValueError(f"{name}: missing, empty or external input {path}")
        inputs[name] = (blend[0], png, fbx, settings[0])
    return inputs
