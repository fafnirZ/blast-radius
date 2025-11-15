from pathlib import Path


def get_all_python_file_paths(root_path: Path) -> list[Path]:
    assert isinstance(root_path, Path)
    results = []
    for path in root_path.glob("**/*.py"):
        if path.is_file():
            results.append(path)
    return results 


def convert_path_to_import(path: Path) -> str:
    assert isinstance(path, Path)
    parts = path.parts

    # if starts with '/' ignore it
    if parts[0] == "/":
        parts = parts[1:]
    results = ".".join(parts)
    return results