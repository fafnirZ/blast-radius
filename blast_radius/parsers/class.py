from __future__ import annotations
import ast



class ClassGatherer(ast.NodeVisitor):
    classes: list[ClassInfo]