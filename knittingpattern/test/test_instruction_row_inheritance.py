"""Test that the color attribute is inherited properly."""
from test_knittingpattern import fixture, pytest
from knittingpattern import load_from_relative_file


@fixture(scope="module")
def coloring_pattern():
    """The pattern with one colored line and a uncolored line."""
    patterns = load_from_relative_file(__name__, "pattern/inheritance.json")
    return patterns.patterns["color test"]

INSTRUCTION_INHERITANCE = [
    ("uncolored", 0, None),      # Neither row nor instruction have a color.
    ("uncolored", 1, "yellow"),  # Instruction uses own color.
    ("colored", 0, "green"),      # Row color is used, instruction has none.
    ("colored", 1, "blue"),     # Instruction prefers own color before row's.
    ("inherited uncolored", 0, None),
    ("inherited uncolored", 1, "yellow"),
    ("inherited colored", 0, "green"),
    ("inherited colored", 1, "blue"),
    ("inherited uncolored +instructions", 0, None),
    ("inherited uncolored +instructions", 1, "brown"),
    ("inherited colored +instructions", 0, "blue"),
    ("inherited colored +instructions", 1, "red")]


@pytest.mark.parametrize("row_id,instuction_index,color",
                         INSTRUCTION_INHERITANCE)
def test_instruction_has_color(coloring_pattern, row_id,
                               instuction_index, color):
    """Test that the instructions correclty inherit from their row."""
    row = coloring_pattern.rows[row_id]
    instruction = row.instructions[instuction_index]
    assert instruction.color == color

ROW_INHERITANCE = [
    ("colored", "blue"),
    ("uncolored", None),
    ("inherited colored", "blue"),
    ("inherited uncolored", None),
    ("inherited colored +instructions", "blue"),
    ("inherited uncolored +instructions", None)]


@pytest.mark.parametrize("row_id,color", ROW_INHERITANCE)
def test_rows_have_color(coloring_pattern, row_id, color):
    """Test that the rows correcly inherit or define their color."""
    row = coloring_pattern.rows[row_id]
    assert row.color == color
