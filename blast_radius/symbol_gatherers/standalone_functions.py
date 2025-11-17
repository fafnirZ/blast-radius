

from dataclasses import dataclass
from typing import Any, Optional
from blast_radius.symbol_gatherers.base import BaseNodeVisitor

################################
# Function Summary Information
################################
@dataclass
class FunctionArgumentInfo:
    arg_name: str
    type_annotation: Optional[str]

@dataclass
class ReturnTypeInfo:
    value: str

@dataclass
class StandaloneFunctionSummaryInfo:
    # ID should be a global reference to the symbol start
    name: str
    args: list[FunctionArgumentInfo]
    returns: ReturnTypeInfo
    
    start_lineno: int
    end_lineno: int

################################
# Function Content Information #
################################

@dataclass
class StandaloneFunctionContentInfo:
    pass

class StandaloneFunctionGatherer(BaseNodeVisitor):
    pass