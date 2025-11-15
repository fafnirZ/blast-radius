import ast
from pathlib import Path
from argparse import ArgumentParser
from pprint import pprint
from blast_radius.files import get_all_python_file_paths
from blast_radius.parsers.imports import FileImportAssociation, ImportGatherer

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "library_path",
        nargs=1
    )

    parser.add_argument(
        "symbol",
        nargs=1
    )
    args = parser.parse_args()
    library_path = Path(args.library_path[0])
    symbol = args.symbol[0]
    import_associations = FileImportAssociation.build(library_path)
    pprint(import_associations)
    
    # file_paths = get_all_python_file_paths(library_path)
    # for file_path in file_paths:
    #     try:
    #         with open(file_path, "r", encoding="utf-8") as file:
    #             source_code = file.read()
    #     except FileNotFoundError:
    #         print(f"Error: File not found at {file_path}")
    #     tree = ast.parse(source_code) 

    #     if file_path.name == "file.py":
    #         print([a for a in ast.walk(tree)])
    #     # contains_symbol = any([isinstance(node, ast.Call) and node.func == symbol for node in ast.walk(tree)])
    #     for node in ast.walk(tree):
    #         if isinstance(node, ast.Call):
    #             node.generic_visit()

        # print(file_path, contains_symbol)