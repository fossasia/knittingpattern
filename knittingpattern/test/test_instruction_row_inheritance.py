"""Test that the color attribute is inherited properly."""
from test_knittingpattern import fixture
from knittingpattern import load_from_relative_file


@fixture
def coloring_pattern():
    """The pattern with one colored line and a uncolored line."""
    patterns = load_from_relative_file(__name__, "pattern/inheritance.json")
    return patterns.patterns["color test"]


@fixture
def colored_row(coloring_pattern):
    """The colored row."""
    return coloring_pattern.rows["colored"].instructions


@fixture
def uncolored_row(coloring_pattern):
    """The uncolored row."""
    return coloring_pattern.rows["uncolored"].instructions


def test_instruction_has_no_color(uncolored_row):
    """Neither row nor instruction have a color."""
    assert uncolored_row[0].color is None


def test_instruction_has_own_color(uncolored_row):
    """Instruction uses own color."""
    assert uncolored_row[1].color == "yellow"


def test_instruction_has_color_from_row(colored_row):
    """No color is given in the instruction, the row color is used."""
    assert colored_row[1].color == "blue"


def test_instruction_has_own_color_despite_row(colored_row):
    """Instruction uses own color before row's color."""
    assert colored_row[0].color == "green"
