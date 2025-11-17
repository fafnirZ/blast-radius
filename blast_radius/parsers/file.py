from __future__ import annotations
import ast
from dataclasses import dataclass
from pathlib import Path
from blast_radius.parsers.base import BaseNodeVisitor
from blast_radius.parsers.classes import ClassSymbolGatherer
from blast_radius.parsers.imports import ImportGatherer
from blast_radius.parsers.standalone_functions import StandaloneFunctionGatherer

@dataclass
class EntireFileSymbolGatherer(BaseNodeVisitor):

    imports: ImportGatherer # TODO rename ImportSymbolGatherer
    classes: list[ClassSymbolGatherer]
    standalone_functions: list[StandaloneFunctionGatherer]

    def visit_ClassDef(self, node: ast.ClassDef):
        inst = ClassSymbolGatherer()
        inst.visit(node)
        self.classes.append(inst)
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        inst = StandaloneFunctionGatherer()
        inst.visit(node)
        self.standalone_functions.append(inst)
    
    def visit(self, node: ast.Module):
        self.imports = ImportGatherer()
        self.imports.visit(node)
        
        # continue
        self.generic_visit()
