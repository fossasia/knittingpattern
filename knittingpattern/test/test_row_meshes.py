from test_knittingpattern import fixture, raises
from knittingpattern import new_knitting_pattern

NO_CONSUMED_MESH = {"number of consumed meshes": 0}
NO_PRODUCED_MESH = {"number of produced meshes": 0}
DOUBLE_CONSUMED_MESH = {"number of consumed meshes": 2}
DOUBLE_PRODUCED_MESH = {"number of produced meshes": 2}


def assert_consumed_index(mesh, instruction_index, index_in_instruction=0):
    assert mesh.consuming_instruction.index_in_row == instruction_index
    assert mesh.index_in_consuming_instruction == index_in_instruction


def assert_produced_index(mesh, instruction_index, index_in_instruction=0):
    assert mesh.producing_instruction.index_in_row == instruction_index
    assert mesh.index_in_producing_instruction == index_in_instruction


def assert_row(row, first_consumed, last_consumed, first_produced,
               last_produced):
    assert_consumed_index(row.first_consumed_mesh, *first_consumed)
    assert_consumed_index(row.last_consumed_mesh, *last_consumed)
    assert_produced_index(row.first_produced_mesh, *first_produced)
    assert_produced_index(row.last_produced_mesh, *last_produced)


@fixture
def row():
    pattern = new_knitting_pattern("test")
    return pattern.add_row(1)


def test_no_meshes(row):
    with raises(IndexError):
        row.first_consumed_mesh
    with raises(IndexError):
        row.last_consumed_mesh
    with raises(IndexError):
        row.first_produced_mesh
    with raises(IndexError):
        row.last_produced_mesh


def test_knit_row(row):
    row.instructions.extend([{}, {}, {}, {}])
    assert_row(row, (0,), (3,), (0,), (3,))


def test_1_or_0(row):
    row.instructions.extend([NO_CONSUMED_MESH, {}, NO_PRODUCED_MESH])
    assert_row(row, (1,), (2,), (0,), (1,))


def test_2(row):
    row.instructions.extend([DOUBLE_CONSUMED_MESH, {}, DOUBLE_PRODUCED_MESH])
    assert_row(row, (0,), (2,), (0,), (2, 1))


def test_2_reversed(row):
    row.instructions.extend([DOUBLE_PRODUCED_MESH, {}, DOUBLE_CONSUMED_MESH])
    assert_row(row, (0,), (2, 1), (0,), (2,))
