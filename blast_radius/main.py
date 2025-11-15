from pathlib import Path
from argparse import ArgumentParser
from blast_radius.files import get_all_python_file_paths

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "library_path",
        nargs=1
    )
    args = parser.parse_args()
    library_path = args.library_path[0]
    files = get_all_python_file_paths(Path(library_path))
    print(files)
