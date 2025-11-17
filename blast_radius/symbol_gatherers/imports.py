from __future__ import annotations
import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from blast_radius.files import get_all_python_file_paths
from blast_radius.symbol_gatherers.base import BaseNodeVisitor

# Define a custom type to hold import information for clarity

class ImportInfo:
    pass

@dataclass
class FromImportInfo(ImportInfo):
    import_path: str
    subject: str
    alias: Optional[str]

@dataclass
class NormalImportInfo(ImportInfo):
    import_path: str
    alias: Optional[str]

class ImportGatherer(BaseNodeVisitor):
    imports: list[ImportInfo]

    def __init__(self):
        # Stores information about all imports found
        self.imports: list[ImportInfo] = []


    def visit_Import(self, node: ast.Import):
        for obj in node.names:
            self.imports.append(NormalImportInfo(import_path=obj.name, alias=obj.asname))
        
        # # 'module' is None for a standard 'import' statement

    def visit_ImportFrom(self, node: ast.ImportFrom):
        module_name = node.module # The module name (e.g., 'os', 'mypackage.submodule')
        for obj in node.names:
            self.imports.append(FromImportInfo(
                import_path=module_name,
                subject=obj.name,
                alias=obj.asname
            ))

    @property
    def attrs(self) -> list[str]:
        return ["imports"]

@dataclass
class FileImportAssociation:
    """
    This means the `file` contains the following `import` statements.
    """
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
    