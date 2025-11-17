"""TODO renamed as GlobalIdentifiers"""
from __future__ import annotations
from abc import ABC, abstractmethod
import ast
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path


class GlobalIdentifier(ABC):
    """Global Identifer to a atomic line/symbol.
    
    Given a global identifier, one must always be able 
    to pinpoint exactly the symbol/line at question.
    """
    value: str

    @abstractmethod
    def validate_structure(self):
        raise NotImplementedError
    
    def validate_existance(self):
        raise NotImplementedError("not sure when I want to implement this, but we should validate that this symbol actually exists.")

@dataclass
class LineReference(GlobalIdentifier):
    """/path/to/file.py:{line_number}"""
    def validate_structure(self):
       assert len(self.value.split(":")) == 2

@dataclass
class Symbol(GlobalIdentifier):
    """/path/to/file.py:{symbol}"""
    def validate_structure(self):
        assert len(self.value.split(":")) == 2

class ClassSymbol(Symbol):
    """/path/to/file.py:ClassName""" 
    def validate_structure(self):
        super().validate_structure()
        _,symbol_section = self.value.split(":")
        assert len(symbol_section.split(".")) == 1

class ClassMethodSymbol(Symbol):
    """/path/to/file.py:ClassName.method_name"""
    def validate_structure(self):
        super().validate_structure()
        _,symbol_section = self.value.split(":")
        assert len(symbol_section.split(".")) == 2

class ClassMethodVariableSymbol(Symbol):
    """/path/to/file.py:ClassName.method_name.variable"""
    def validate_structure(self):
        super().validate_structure()
        _,symbol_section = self.value.split(":")
        assert len(symbol_section.split(".")) == 3

class ClassAttributeSymbol(ClassSymbol):
    """/path/to/file.py:ClassName.attribute_name"""
    def validate_structure(self):
        super().validate_structure()
        _,symbol_section = self.value.split(":")
        assert len(symbol_section.split(".")) == 2

class FunctionSymbol(Symbol):
    """/path/to/file.py:FunctionName"""
    def validate_structure(self):
        super().validate_structure()
        _,symbol_section = self.value.split(":")
        assert len(symbol_section.split(".")) == 1

class FunctionVariableSymbol(Symbol):
    """/path/to/file.py:Function.variable"""
    def validate_structure(self):
        super().validate_structure()
        _,symbol_section = self.value.split(":")
        assert len(symbol_section.split(".")) == 2
