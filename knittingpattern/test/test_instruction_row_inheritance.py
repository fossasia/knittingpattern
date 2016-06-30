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
    return coloring_pattern.rows["colored"].instructions


@fixture
def uncolored_row(coloring_pattern):
    return coloring_pattern.rows["uncolored"].instructions


def test_instruction_has_no_color(uncolored_row):
    assert uncolored_row[0].color is None


def test_instruction_has_own_color(uncolored_row):
    assert uncolored_row[1].color == "yellow"


def test_instruction_has_color_from_row(colored_row):
    assert colored_row[1].color == "blue"


def test_instruction_has_own_color_despite_row(colored_row):
    assert colored_row[0].color == "green"
