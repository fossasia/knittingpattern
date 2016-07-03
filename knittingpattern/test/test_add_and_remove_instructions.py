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
    return pattern.rows[1]


@fixture
def row2(pattern):
    """The row with one instruction."""
    return pattern.rows[2]


@fixture
def instruction(row):
    """The instruction."""
    return row.instructions[0]


@fixture
def instruction2(row2):
    """The instruction."""
    return row2.instructions[0]


@fixture
def empty_row(row, instruction):
    """Now, there is no instruction any more."""
    assert instruction
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
    assert not instruction.is_in_row()


def test_inserting_a_new_instruction_loads_its_config(row):
    row.instructions.append({})
    instruction = row.instructions[-1]
    assert instruction.type == "knit"
    assert instruction.is_in_row()
    assert instruction.row == row
    assert instruction.index_in_row == 1


def test_insert_an_existing_instruction(row, instruction2, row2):
    row.instructions.insert(0, instruction2)
    assert instruction2.row == row
    assert instruction2.index_in_row == 0
    assert row2.instructions == []


def test_transfer_removed_instruction(row, row2):
    row2.instructions.append(row.instructions.pop())
    instruction = row2.instructions[-1]
    assert instruction.row == row2
