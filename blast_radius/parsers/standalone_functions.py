

from typing import Any, Optional
from blast_radius.parsers.base import BaseNodeVisitor

class FunctionArgumentInfo:
    arg_name: str
    type_annotation: Optional[type]

class DefaultedFunctionArgumentInfo(FunctionArgumentInfo):
    default: Any

class ReturnTypeInfo:
    value: type

class StandaloneFunctionInfo:
    # ID should be a global reference to the symbol start
    name: str
    args: list[FunctionArgumentInfo]
    kwargs: list[FunctionArgumentInfo|DefaultedFunctionArgumentInfo]
    returns: ReturnTypeInfo
    
    start_lineno: int
    end_lineno: int

    # TODO: process body

class StandaloneFunctionGatherer(BaseNodeVisitor):
    pass