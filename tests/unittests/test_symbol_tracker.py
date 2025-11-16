
import ast
from dataclasses import dataclass
from pathlib import Path
import pytest

from blast_radius.parsers.symbol_call_tracker import SymbolCallGatherer
from blast_radius.symbol import ClassSymbol

@dataclass
class FileObj:
    relative_path: str # allows us to prepend a origin folder
    contents: str

    def write_contents(self, origin_path: Path):
        assert isinstance(origin_path, Path)
        input_path = origin_path/self.relative_path
        input_str = str(input_path)
        __input_path = Path(input_str.split(":")[0])
        __input_path.parent.mkdir(parents=True, exist_ok=True)
        print(__input_path.is_file())
        __input_path.write_text(self.contents)

@dataclass
class Bucket:
    files: list[FileObj]

    def init(self, origin_path: Path):
        for file in self.files:
            file.write_contents(origin_path=origin_path)


FILE_A = FileObj(
    relative_path="path/to/file_a.py",
    contents=("""
class FirstClass:
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
)
FILE_B = FileObj(
    relative_path="path/to/file_b.py",
    contents=("""
from path.to.file_b import FirstClass
class AnotherClass:
    attribute1: FirstClass
"""
    )
)

BUCKET = Bucket(
    files=[FILE_A, FILE_B]
)

@pytest.mark.parametrize(
    "user_input, bucket, file_to_profile, expected_matches",
    [
        ("path/to/file_a.py:FirstClass", BUCKET, FILE_A, []), # expected matches = 0 because nothing is a container of a ClassDefinition
        ("path/to/file_a.py:FirstClass.attribute1", BUCKET, FILE_A, [ast.ClassDef, ast.AnnAssign]), 
        ("path/to/file_a.py:FirstClass.method", BUCKET, FILE_A, [ast.ClassDef, ast.FunctionDef]),
    ]
)
def test_class_symbol(
    user_input, bucket, file_to_profile, expected_matches,
    tmp_path
):
    bucket.init(origin_path=tmp_path)
    absolute_user_input = str(tmp_path / user_input)
    symbol = ClassSymbol(absolute_user_input).determine()
    gatherer = SymbolCallGatherer.from_source_code(
        source_code=file_to_profile.contents, 
        symbol=symbol,
    )
    print(gatherer.symbol_containers)
    assert [type(sym) for sym in gatherer.symbol_containers] == expected_matches