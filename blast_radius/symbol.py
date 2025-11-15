from abc import ABC, abstractmethod
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
        assert self.value.split(":") == 2
        path_to_file, _ = self.value.split(":")
        assert Path(path_to_file).is_file()
        self.symbol_validation()

    @abstractmethod 
    def symbol_validation(self):
        raise NotImplementedError
    
    @cached_property
    def file_path(self):
        fp,_ = self.value.split(":")
        return fp

    @cached_property
    def symbl(self):
        _,sym = self.value.split(":")
        return sym


class ClassSymbol(Symbol):
    def symbol_validation(self):
        _, symbol = self.value.split(":")
        assert len(symbol.split(".")) == 1


class MethodSymbol(Symbol):
    def symbol_validation(self):
        _, symbol = self.value.split(":")
        assert len(symbol.split(".")) == 2

class FunctionSymbol(Symbol):
    def symbol_validation(self):
        _, symbol = self.value.split(":")
        assert len(symbol.split(".")) == 1