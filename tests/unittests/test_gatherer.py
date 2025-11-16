
from io import StringIO
import json
from pprint import pprint
import pytest
from blast_radius.parsers.classes import ClassAttributeInfo, ClassBaseClassInfo, ClassMethodInfo, ClassSymbolGatherer
from blast_radius.parsers.standalone_functions import FunctionArgumentInfo, ReturnTypeInfo
import difflib

CASE_1_CODE = """
class ClassName(SomeOtherClass):
    attribute1: str
    attribute2: int

    def method_1(self) -> SomeOtherClass:
        pass

    @classmethod
    def method_2(cls, *, arg: str) -> None:
        pass
"""
CASE_1_EXPECTED_OBJS = {
    "bases": [ClassBaseClassInfo(base_class_name="SomeOtherClass")],
    "attributes": [
        ClassAttributeInfo(attr_name="attribute1", attr_type="str"),
        ClassAttributeInfo(attr_name="attribute2", attr_type="int"),
    ],
    "methods": [
        ClassMethodInfo(
            name="method_1",
            args=[FunctionArgumentInfo(arg_name="self", type_annotation=None)],
            method_type="instance",
            returns=ReturnTypeInfo(value="SomeOtherClass"),
            start_lineno=6,
            end_lineno=7
        ),
        ClassMethodInfo(
            name="method_2",
            args=[
                FunctionArgumentInfo(arg_name="cls", type_annotation=None),
                FunctionArgumentInfo(arg_name="arg", type_annotation="str"),
            ],
            method_type="class",
            returns=ReturnTypeInfo(value="SomeOtherClass"),
            start_lineno=10,
            end_lineno=11,
        )
    ]
}

@pytest.mark.parametrize(
    "content, expected",
    [
        (CASE_1_CODE, CASE_1_EXPECTED_OBJS)
    ]
)
def test_class_symbol_gatherer(content, expected):

    gatherer = ClassSymbolGatherer.from_source_code(content)
    gatherer_data_dict = {
        attr: getattr(gatherer, attr)
        for attr in gatherer.attrs
    }

    # raw print
    pprint(gatherer_data_dict)
    pprint(expected)

    # diff print

    # diff = difflib.unified_diff(json.dumps(gatherer_data_dict), json.dumps(expected))
    # for line in diff:
    #     print(line)

    
    assert gatherer_data_dict == expected