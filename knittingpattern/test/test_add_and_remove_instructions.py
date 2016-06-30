from test_knittingpattern import fixture, HERE, raises
from knittingpattern import load_from_relative_file
from knittingpattern.Instruction import InstructionNotFoundInRow


@fixture
def single_instruction_pattern_set():
    return load_from_relative_file(HERE, "pattern/single_instruction.json")


@fixture
def pattern(single_instruction_pattern_set):
    return single_instruction_pattern_set.patterns["A.1"]


@fixture
def row(pattern):
    return pattern.rows["1"]


@fixture
def instruction(row):
    return row.instructions[0]


def test_there_is_only_one_instruction(row):
    assert len(row.instructions) == 1


def test_removing_the_instruction_gives_an_error_when_accessing_its_index(
        row, instruction):
    row.instructions.pop()
    with raises(InstructionNotFoundInRow):
        instruction.index_in_row
