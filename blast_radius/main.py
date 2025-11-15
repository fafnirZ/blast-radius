from pathlib import Path
from argparse import ArgumentParser
from pprint import pprint
from blast_radius.files import get_all_python_file_paths
from blast_radius.imports import FileImportAssociation, ImportGatherer

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "library_path",
        nargs=1
    )
    args = parser.parse_args()
    library_path = args.library_path[0]
    import_associations = FileImportAssociation.build(Path(library_path))
    pprint(import_associations)