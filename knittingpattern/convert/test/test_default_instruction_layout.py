"""Test rendering propetries of the default instructions."""
from test_convert import fixture
from knittingpattern.InstructionLibrary import default_instructions


@fixture
def default():
    return default_instructions()


def test_knit_has_no_z_index(default):
    assert default["knit"].render_z == 0


def test_yo_has_z_index(default):
    assert default["yo"].render_z == 1
    assert default["yo twisted"].render_z == 1
