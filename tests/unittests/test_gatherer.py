
from blast_radius.parsers.classes import ClassSymbolGatherer


CONTENT = """
class ClassName(SomeOtherClass):
    attribute1: str
    attribute2: int

    def method_1(self) -> SomeOtherClass:
        pass

    @classmethod
    def method_2(cls, *, arg: str) -> None:
        pass
"""

def test_class_symbol_gatherer():

    gatherer = ClassSymbolGatherer.from_source_code(CONTENT)
    print(gatherer)

    assert 1==0