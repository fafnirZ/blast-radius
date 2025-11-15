from pathlib import Path


def get_all_python_files(root_path) -> list[Path]:
    results = []
    for path in root_path.glob("**/*.py"):
        if path.is_file():
            results.append(path)
    return results
    
