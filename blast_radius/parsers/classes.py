from __future__ import annotations
from blast_radius.parsers.base import BaseNodeVisitor
from blast_radius.parsers.standalone_functions import DefaultedFunctionArgumentInfo, FunctionArgumentInfo, ReturnTypeInfo, StandaloneFunctionInfo

class ClassAttributeInfo:
    attr_name: str
    attr_type: type



class ClassMethodInfo(StandaloneFunctionInfo):
    is_instancemethod: bool
    is_classmethod: bool
    is_staticmethod: bool
    

class ClassSymbolGatherer(BaseNodeVisitor):
    attributes: list[ClassAttributeInfo]
    methods: list[ClassMethodInfo]