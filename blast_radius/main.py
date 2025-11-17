import ast
from pathlib import Path
from argparse import ArgumentParser
from pprint import pprint
from blast_radius.files import get_all_python_file_paths
from blast_radius.symbol_gatherers.imports import FileImportAssociation, ImportGatherer
from blast_radius.symbol_gatherers.symbol_call_tracker import SymbolContainerAssociations
from blast_radius.symbol import ClassSymbol, FunctionSymbol


def main(args):
    library_path = Path(args.library_path[0])
    import_associations = FileImportAssociation.build(library_path)
    
    if args.cls_symbol:
        symbol_assoc = SymbolContainerAssociations.build(library_path, ClassSymbol(args.cls_symbol).determine())
        pprint(symbol_assoc)
    if args.fn_symbol:
        symbol_assoc = SymbolContainerAssociations.build(library_path, FunctionSymbol(args.fn_symbol)) 
        pprint(symbol_assoc)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "library_path",
        nargs=1,
    )
    parser.add_argument(
        "--cls-symbol",
    )
    parser.add_argument(
        "--fn-symbol",
    )
    args = parser.parse_args()
    main(args)
    exit(0)