
from pathlib import Path
import pytest

from blast_radius.symbol import ClassAttributeSymbol, ClassMethodSymbol, ClassSymbol

CONTENTS = (
"""
class ClassName:
    attribute1: str

    def method(self) -> None:
        pass

    @classmethod
    def classmethod(self) -> None:
        pass

    @property
    def property(self) -> str:
        return self.attribute1
"""
)

@pytest.mark.parametrize(
    "input, contents, expected_symbol_type",
    [
        ("path/to/file_a.py:ClassName", CONTENTS, ClassSymbol),
        ("path/to/file_a.py:ClassName.attribute1", CONTENTS, ClassAttributeSymbol),
        ("path/to/file_a.py:ClassName.method", CONTENTS, ClassMethodSymbol),
        ("path/to/file_a.py:ClassName.classmethod", CONTENTS, ClassMethodSymbol),
        ("path/to/file_a.py:ClassName.property", CONTENTS, ClassMethodSymbol),
    ]
)
def test_class_symbol(
    input, contents, expected_symbol_type,
    tmp_path
):
    
    input_path = tmp_path/input
    input_str = str(input_path)

    __input_path = Path(input_str.split(":")[0])
    __input_path.parent.mkdir(parents=True, exist_ok=True)
    __input_path.write_text(contents)
    
    inst = ClassSymbol(input_str).determine()
    assert isinstance(inst, expected_symbol_type)

