# if class or method has been `Called` i.e. initialised or called
# keep track of the variable which has called been assiged to the output of the call.


import ast
from dataclasses import dataclass
from pathlib import Path

from blast_radius.files import get_all_python_file_paths
from blast_radius.parsers.base import BaseNodeVisitor
from blast_radius.parsers.helpers import check_expression_contains_symbol
from blast_radius.symbol import ClassAttributeSymbol, ClassMethodSymbol, ClassSymbol, FunctionSymbol, Symbol


class SymbolCallGatherer(BaseNodeVisitor):
    """
    Used to profile Files which call a particular symbol.
    It is NOT used to profile the File which DEFINES tghe symbol. so DONT use it there.
    """
    def __init__(self, symbol: Symbol):
        assert isinstance(symbol, Symbol)
        self.symbol = symbol
        self.symbol_containers = []

    def get_symbol(self) -> str:
        if isinstance(self.symbol, ClassSymbol):
            if isinstance(self.symbol, (ClassMethodSymbol, ClassAttributeSymbol)):
                return self.symbol.bound_callable_name
            else:
                return self.symbol.class_name 
        elif isinstance(self.symbol, FunctionSymbol):
            return self.symbol.symbl
        else:
            RuntimeError

    def visit_AugAssign(self, node: ast.AugAssign):
        if node is None:
            return
        if check_expression_contains_symbol(node, self.get_symbol()):
            self.symbol_containers.append(node)
        if node:
            self.generic_visit(node)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        if node is None:
            return
        if check_expression_contains_symbol(node, self.get_symbol()):
            self.symbol_containers.append(node)
        if node:
            self.generic_visit(node)
    
    def visit_Assign(self, node: ast.Assign):
        if node is None:
            return
        if check_expression_contains_symbol(node, self.get_symbol()):
            self.symbol_containers.append(node)
        if node:
            self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node is None:
            return
        # check if function definition contains args
        for arg in node.args.args:
            if isinstance(self.symbol, ClassSymbol):
                if arg.annotation == self.get_symbol():
                    self.symbol_containers.append(node)
                    break
        # check if return statement contains symbol
        if check_expression_contains_symbol(node.returns, self.get_symbol()):
            self.symbol_containers.append(node)
        if node:
            self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        if node is None:
            return
        # bases (parent classes)
        if any([check_expression_contains_symbol(base, self.get_symbol())
                for base in node.bases]):
            self.symbol_containers.append(node)

        # check body
        if any([check_expression_contains_symbol(base, self.get_symbol())
                for base in node.body]):
            self.symbol_containers.append(node)
        
        # continue
        if node:
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
    