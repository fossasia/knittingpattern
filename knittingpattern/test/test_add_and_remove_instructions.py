"""Test the maniipulation of the rows by adding instructions."""
from test_knittingpattern import fixture, HERE, raises
from knittingpattern import load_from_relative_file
from knittingpattern.Instruction import InstructionNotFoundInRow


@fixture
def single_instruction_pattern_set():
    """Load the pattern set with only one instruction."""
    return load_from_relative_file(HERE, "pattern/single_instruction.json")


@fixture
def pattern(single_instruction_pattern_set):
    """The pattern which has only one instruction."""
    return single_instruction_pattern_set.patterns["A.1"]


@fixture
def row(pattern):
    """The row with one instruction."""
    return pattern.rows["1"]


@fixture
def instruction(row):
    """The instruction."""
    return row.instructions[0]


@fixture
def empty_row(row):
    """Now, there is no instruction any more."""
    row.instructions.pop()
    return row


def test_there_is_only_one_instruction(row):
    """There should be only one instruction, as claimed many times.

    If people write that there is only one instruction, we should make that
    sure!"""
    assert len(row.instructions) == 1


def test_removing_the_instruction_gives_an_error_when_accessing_its_index(
        empty_row, instruction):
    """Obviously a removed instruction is not in its row any more and thus has
    no index."""
    with raises(InstructionNotFoundInRow):
        instruction.index_in_row
