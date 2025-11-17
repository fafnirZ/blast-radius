

from dataclasses import dataclass
from typing import Any, Optional
from blast_radius.symbol_gatherers.base import BaseNodeVisitor

@dataclass
class FunctionArgumentInfo:
    arg_name: str
    type_annotation: Optional[str]

@dataclass
class ReturnTypeInfo:
    value: str

@dataclass
class StandaloneFunctionInfo:
    # ID should be a global reference to the symbol start
    name: str
    args: list[FunctionArgumentInfo]
    returns: ReturnTypeInfo
    
    start_lineno: int
    end_lineno: int

    # TODO: process body

class StandaloneFunctionGatherer(BaseNodeVisitor):
    pass