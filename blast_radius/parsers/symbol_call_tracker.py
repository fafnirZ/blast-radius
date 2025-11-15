# if class or method has been `Called` i.e. initialised or called
# keep track of the variable which has called been assiged to the output of the call.


import ast
from dataclasses import dataclass
from pathlib import Path

from blast_radius.files import get_all_python_file_paths
from blast_radius.parsers.base import BaseNodeVisitor
from blast_radius.parsers.helpers import check_expression_contains_symbol
from blast_radius.symbol import ClassSymbol, Symbol


class SymbolCallGatherer(BaseNodeVisitor):

    def __init__(self, symbol: Symbol):
        assert isinstance(symbol, Symbol)
        self.symbol = symbol
        self.symbol_containers = []


    def visit_AugAssign(self, node: ast.AugAssign):
        if check_expression_contains_symbol(node.value, self.symbol.symbl):
            self.symbol_containers.append(node)
        self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if check_expression_contains_symbol(node.value, self.symbol.symbl):
            self.symbol_containers.append(node)
        self.generic_visit(node)
    
    def visit_Assign(self, node: ast.Assign):
        if check_expression_contains_symbol(node.value, self.symbol.symbl):
            self.symbol_containers.append(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # check if function definition contains args
        for arg in node.args.args:
            if isinstance(self.symbol, ClassSymbol):
                if arg.annotation == self.symbol.symbl:
                    self.symbol_containers.append(node)
                    break
        # check if return statement contains symbol
        if check_expression_contains_symbol(node.returns, self.symbol.symbl):
            self.symbol_containers.append(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        # bases (parent)
        if any([check_expression_contains_symbol(base, self.symbol.symbl)
                for base in node.bases]):
            self.symbol_containers.append(node)

        # class attribute annotations are handled in AnnAssign
        self.generic_visit(node)
    
    @property
    def attrs(self) -> list[str]:
        return ["symbol", "symbol_containers"]
    
@dataclass
class SymbolContainerAssociations:

    associations: dict[Path, SymbolCallGatherer]

    @classmethod
    def build(cls, root_path: Path, symbol: Symbol) -> SymbolCallGatherer:
        assert isinstance(root_path, Path)

        _associations = {}
        file_paths = get_all_python_file_paths(root_path)
        
        for file_path in file_paths:
            gatherer = SymbolCallGatherer.from_file_path(file_path, symbol=symbol)
            _associations[file_path] = gatherer
        
        return cls(associations=_associations)
    