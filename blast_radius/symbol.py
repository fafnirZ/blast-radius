from __future__ import annotations
from abc import ABC, abstractmethod
import ast
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path


@dataclass
class Symbol(ABC):
    """A symbol must be globally unique so must include a path to the file.
    
    /path/to/file.py:ClassName
    """
    value: str

    def __post_init__(self):
        assert len(self.value.split(":")) == 2
        path_to_file, _ = self.value.split(":")
        assert Path(path_to_file).is_file()
        self.symbol_validation()

    @abstractmethod 
    def symbol_validation(self):
        raise NotImplementedError
    
    @cached_property
    def file_path(self) -> str:
        fp,_ = self.value.split(":")
        return fp

    @cached_property
    def symbl(self) -> str:
        _,sym = self.value.split(":")
        return sym


class ClassSymbol(Symbol):
    def symbol_validation(self):
        assert 1 <= len(self.symbl.split(".")) <= 2

    def determine(self) -> ClassMethodSymbol | ClassAttributeSymbol:
        """Raises Exceptions."""
        split_len = len(self.symbl.split("."))
        if split_len == 1:
            return self
        elif split_len == 2:
            fp = Path(self.file_path)
            assert fp.is_file()
            source_code = fp.read_text()
            tree = ast.parse(source_code)

            class_name, bound_obj_name = self.symbl.split(".")
            # get all ClassDefn Nodes matching class_name
            matching_class_nodes = [
                node
                for node in ast.walk(tree)
                if isinstance(node, ast.ClassDef) and node.name == class_name
            ]
            assert len(matching_class_nodes) == 1
            class_node = matching_class_nodes[0]
            print(class_node)

        else:
            raise RuntimeError



class ClassMethodSymbol(ClassSymbol):
    """ClassName.method_name"""
    def symbol_validation(self):
        assert len(self.symbl.split(".")) == 2

class ClassAttributeSymbol(ClassSymbol):
    """ClassName.attribute_name"""
    def symbol_validation(self):
        assert len(self.symbl.split(".")) == 2

class FunctionSymbol(Symbol):
    """FunctionName"""
    def symbol_validation(self):
        assert len(self.symbl.split(".")) == 1