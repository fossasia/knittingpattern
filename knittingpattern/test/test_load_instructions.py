from test_knittingpattern import fixture, os
from knittingpattern.InstructionLibrary import InstructionLibrary


@fixture
def lib():
    return InstructionLibrary()


def test_load_from_relative_file(lib):
    relative_path = "test_instructions/test_instruction_1.json"
    lib.load.relative_file(__file__, relative_path)
    assert lib.as_instruction({"type": "test1"})["value"] == 1
    assert "value" not in lib.as_instruction({"type": "test2"})


def test_load_from_relative_folder(lib):
    lib.load.relative_folder(__file__, "test_instructions")
    assert lib.as_instruction({"type": "test1"})["value"] == 1
    assert lib.as_instruction({"type": "test2"})["value"] == 2


def test_load_from_folder(lib):
    folder = os.path.join(os.path.dirname(__file__), "test_instructions")
    lib.load.folder(folder)
    assert lib.as_instruction({"type": "test2"})["value"] == 2
    assert lib.as_instruction({"type": "test1"})["value"] == 1


def test_loading_from_folder_recursively(lib):
    lib.load.relative_folder(__file__, "test_instructions")
    assert lib.as_instruction({"type": "test3"})["value"] == 3
