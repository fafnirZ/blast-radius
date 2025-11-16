from __future__ import annotations
import ast
from dataclasses import dataclass
from typing import Literal
from blast_radius.parsers.base import BaseNodeVisitor
from blast_radius.parsers.standalone_functions import FunctionArgumentInfo, ReturnTypeInfo, StandaloneFunctionInfo

@dataclass
class ClassAttributeInfo:
    attr_name: str
    attr_type: str

@dataclass
class ClassBaseClassInfo:
    base_class_name: str

@dataclass
class ClassMethodInfo(StandaloneFunctionInfo):
    method_type: Literal["instance", "class", "static", "property"]
    

class ClassSymbolGatherer(BaseNodeVisitor):
    bases: list[ClassBaseClassInfo]
    attributes: list[ClassAttributeInfo]
    methods: list[ClassMethodInfo]

    def __init__(self):
        self.bases = []
        self.attributes = []
        self.methods = []

    def visit_ClassDef(self, node: ast.ClassDef):
        # get base info
        for name_node in node.bases:
            self.bases.append(ClassBaseClassInfo(
                base_class_name=name_node.id
            ))
        
        self.generic_visit(node)
        
                
    def visit_FunctionDef(self, node: ast.FunctionDef):
        ########
        # args #
        ########
        __args = []
        __method_type = "instance"
        arguments: ast.arguments = node.args
        for arg in [
            *arguments.args,
            # TODO kwargs?
        ]:
            __args.append(FunctionArgumentInfo(
                arg_name=arg.arg,
                type_annotation=arg.annotation.id if arg.annotation else None,
            ))
            
        ##############
        # decorators #
        ##############
        
        for decorator in node.decorator_list:
            if decorator.id == "classmethod":
                __method_type = "class"
            elif decorator.id == "staticmethod":
                __method_type = "static"
            elif decorator.id == "property":
                __method_type = "property"
        

            

        ###############
        # return type #
        ###############

        match node.returns:
            case ast.Name():
                __return_type = ReturnTypeInfo(value=node.returns.id)
            case ast.Constant():
                __return_type = ReturnTypeInfo(value=node.returns.value)
            case _:
                __return_type = ReturnTypeInfo(value=None)

        self.methods.append(ClassMethodInfo(
            name=node.name,
            args=__args,
            method_type=__method_type,
            returns=__return_type,
            start_lineno=node.lineno,
            end_lineno=node.end_lineno,
        ))
        # do not traverse further, just store high level symbol info.

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.attributes.append(ClassAttributeInfo(
            attr_name=node.target.id,
            attr_type=node.annotation.id
        )) 
        # do not traverse further.
            
    
    @property
    def attrs(self) -> list[str]:
        return ["bases", "attributes", "methods"]
            
