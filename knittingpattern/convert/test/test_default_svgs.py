from test_convert import fixture, os, pytest, HERE
from knittingpattern.convert.InstructionToSVG import \
    default_instructions_to_svg
from collections import namedtuple

Instruction = namedtuple("Instruction", ["type"])
default_files = os.listdir(os.path.join(HERE, "..", "..", "instructions"))
default_types = [os.path.splitext(file)[0] for file in default_files]


@fixture(scope="module")
def default():
    return default_instructions_to_svg()


def test_default_instruction_is_not_the_same(default):
    """This allows loading different svgs based on the default set."""
    assert default_instructions_to_svg() != default


@pytest.mark.parametrize('instruction', list(map(Instruction, default_types)))
def test_instructions_have_svg(default, instruction):
    assert default.has_svg_for_instruction(instruction)


def test_default_does_not_have_all_instructions(default):
    assert not default.has_svg_for_instruction(Instruction("asjdkalks"))
