from dataclasses import dataclass


@dataclass
class Symbol:
    value: str

class ClassSymbol(Symbol):
    def __post_init__(self):
        assert len(self.value.split(".")) == 1

class MethodSymbol(Symbol):
    def __post_init__(self):
        assert len(self.value.split(".")) == 2

class FunctionSymbol(Symbol):
    def __post_init__(self):
        assert len(self.value.split(".")) == 1