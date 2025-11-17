from __future__ import annotations
import ast
from dataclasses import dataclass
from pathlib import Path
from blast_radius.symbol_gatherers.base import BaseNodeVisitor
from blast_radius.symbol_gatherers.classes import ClassSymbolGatherer
from blast_radius.symbol_gatherers.imports import ImportGatherer
from blast_radius.symbol_gatherers.standalone_functions import StandaloneFunctionGatherer

class EntireFileSymbolGatherer(BaseNodeVisitor):

    imports: ImportGatherer # TODO rename ImportSymbolGatherer
    classes: list[ClassSymbolGatherer]
    standalone_functions: list[StandaloneFunctionGatherer]

    def __init__(self):
        self.imports = None
        self.classes = []
        self.standalone_functions = []
    
    def visit(self, node: ast.Module):
        self.imports = ImportGatherer()
        self.imports.visit(node)

        for node in node.body:
            if isinstance(node, ast.ClassDef):
                inst = ClassSymbolGatherer()
                inst.visit(node)
                self.classes.append(inst)
            elif isinstance(node, ast.FunctionDef):
                inst = StandaloneFunctionGatherer()
                inst.visit(node)
                self.standalone_functions.append(inst)

    
    @property
    def attrs(self) -> list[str]:
        return ["imports", "classes", "standalone_functions"]
