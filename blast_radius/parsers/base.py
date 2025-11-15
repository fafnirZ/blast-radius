

import ast
from pathlib import Path
from typing import Self


class BaseNodeVisitor(ast.NodeVisitor):

    @classmethod
    def from_file_path(cls, file_path: Path) -> Self:
        # read raw file info
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                source_code = file.read()
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return cls()
        return cls.from_source_code(source_code=source_code)

    @classmethod
    def from_source_code(cls, source_code: str) -> Self:
        inst = cls()
        tree = ast.parse(source_code) 
        # traverse AST
        gatherer = inst
        gatherer.visit(tree)
        return inst
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            "("
            +",".join([f"{attr}={repr(getattr(self, attr))}" for attr in self.attrs])
            +")"
        )
    