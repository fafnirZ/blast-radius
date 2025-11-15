from __future__ import annotations
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from blast_radius.files import get_all_python_file_paths

# Define a custom type to hold import information for clarity

@dataclass
class ImportInfo:
    name: str
    aliases: Optional[list[AliasInfo]]
    def __repr__(self) -> str:
        return f"ImportInfo(name='{self.name}',aliases={self.aliases})"

@dataclass
class AliasInfo:
    name: str
    asname: str | None

    def __repr__(self) -> str:
        return f"AliasInfo(name='{self.name}', asname='{self.asname}')"

class ImportGatherer(ast.NodeVisitor):
    imports: list[ImportInfo]

    def __init__(self):
        # Stores information about all imports found
        self.imports: list[ImportInfo] = []

    def visit_Import(self, node: ast.Import):
        # Handles statements like: 'import module1', 'import module2 as alias'
        names = []
        for alias in node.names:
            names.append(AliasInfo(name=alias.name, asname=alias.asname))
        
        # 'module' is None for a standard 'import' statement
        self.imports.append(ImportInfo(name=None, aliases=names))
        self.generic_visit(node) # Continue traversing any nested nodes, though unlikely here

    def visit_ImportFrom(self, node: ast.ImportFrom):
        # Handles statements like: 'from module import name1', 'from . import name2 as alias'
        module_name = node.module # The module name (e.g., 'os', 'mypackage.submodule')
        names: list[AliasInfo] = []
        for alias in node.names:
            names.append(AliasInfo(name=alias.name, asname=alias.asname))
        
        self.imports.append(ImportInfo(name=module_name, aliases=names))
        self.generic_visit(node) # Continue traversing
    


    @classmethod
    def from_file_path(cls, file_path: Path) -> ImportGatherer:
        inst = cls()

        # read raw file info
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                source_code = file.read()
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return inst
        tree = ast.parse(source_code) 

        # traverse AST
        gatherer = inst
        gatherer.visit(tree)

        return inst
    
    def __repr__(self) -> str:
        return f"ImportGatherer(imports={self.imports})"
    

@dataclass
class FileImportAssociation:
    associations: dict[Path, ImportGatherer]

    @classmethod
    def build(cls, root_path: Path) -> FileImportAssociation:
        assert isinstance(root_path, Path)

        _associations = {}
        file_paths = get_all_python_file_paths(root_path)
        
        for file_path in file_paths:
            gatherer = ImportGatherer.from_file_path(file_path)
            _associations[file_path] = gatherer
        
        return cls(associations=_associations)
    