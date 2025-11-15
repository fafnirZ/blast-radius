import pytest
from pathlib import Path

from blast_radius.files import convert_path_to_import

@pytest.mark.parametrize(
    "input, expected",
    [
        (Path("some/path/to"), "some.path.to"),
        (Path("/another/path/to"), "another.path.to"),
    ]
)
def test_convert_path_to_import(
    input, expected
):
    result = convert_path_to_import(input) 
    assert result == expected