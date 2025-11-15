from pathlib import Path
import sys
from argparse import ArgumentParser
from blast_radius.files import get_all_python_files

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "library_path",
        nargs=1
    )
    args = parser.parse_args()
    library_path = args.library_path[0]
    files = get_all_python_files(Path(library_path))
    print(files)
