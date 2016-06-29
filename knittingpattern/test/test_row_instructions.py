"""These tests access the instructions in rows."""
from test_knittingpattern import fixture, raises
from test_examples import charlotte as _charlotte
from knittingpattern.Instruction import InstructionNotFoundInRow


@fixture
def a1():
    """:return: the pattern ``"A.1"`` in charlotte"""
    return _charlotte().patterns["A.1"]


@fixture
def row0(a1):
    return a1.rows.at(0)


@fixture
def row1(a1):
    return a1.rows.at(1)


@fixture
def row2(a1):
    return a1.rows.at(2)


@fixture
def mesh0(row0):
    mesh = row0.produced_meshes[0]
    return mesh


@fixture
def instruction0(row0):
    return row0.instructions[0]


@fixture
def instruction1(row1):
    return row1.instructions[0]


@fixture
def removed_instruction(row0):
    return row0.instructions.pop(1)


def test_row0_consumes_empty_meshes(row0):
    assert len(row0.consumed_meshes) == 5
    assert not any(mesh.is_produced() for mesh in row0.consumed_meshes)


def test_consumed_meshes_have_index(row0):
    for i in range(5):
        mesh = row0.consumed_meshes[i]
        assert mesh.index_in_consuming_row == i
        assert mesh.consuming_row == row0


def test_row0_produces_5_meshes(row0):
    assert len(row0.produced_meshes) == 5
    assert all(mesh.is_knit() for mesh in row0.produced_meshes)


def test_row0_meshes_point_also_to_row1(mesh0, row0, row1):
    assert mesh0.producing_row == row0
    assert mesh0.consuming_row == row1


def test_row0_instruction_produces_mesh_0(mesh0, instruction0):
    assert instruction0 == mesh0.producing_instruction
    assert instruction0.produced_meshes == [mesh0]
    assert instruction0.number_of_produced_meshes == 1


def test_instruction0_is_knit(instruction0):
    assert instruction0.does_knit()


def test_instruction_position_in_row(row0, instruction0):
    assert instruction0.row == row0
    assert instruction0.index_in_row == 0
    assert row0.instructions[0] == instruction0


def test_mesh0_is_consumed_by_instruction1(mesh0, instruction1):
    assert mesh0.consuming_instruction == instruction1
    assert instruction1.consumed_meshes[0].as_produced_mesh() == mesh0


def test_instruction1_is_knit(instruction1):
    assert instruction1.does_knit()


def test_instruction1_position_in_row(instruction1):
    assert instruction1.index_in_row == 0


def test_mesh0_is_produced(mesh0):
    assert mesh0.is_produced()
    assert mesh0.is_consumed()


def test_instruction0_builds_on_unproduced_meshes(instruction0):
    assert not instruction0.consumed_meshes[0].is_produced()


@fixture
def skp(row2):
    return row2.instructions[0]


@fixture
def yo(row2):
    return row2.instructions[1]


def test_yarn_over(yo):
    assert yo.number_of_consumed_meshes == 0
    assert yo.number_of_produced_meshes == 1


def test_skp(skp):
    assert skp.number_of_consumed_meshes == 2
    assert skp.number_of_produced_meshes == 1


def test_position_in_row2(skp, yo, row2):
    assert skp.row == row2
    assert yo.row == row2
    assert skp.index_in_row == 0
    assert yo.index_in_row == 1


def test_skp_consumed_meshes_from_row1(skp, row1, row2):
    assert len(skp.produced_meshes) == 1
    assert len(skp.consumed_meshes) == 2
    m1, m2 = skp.consumed_meshes
    assert m1.consuming_instruction == skp
    assert m1.consuming_row == row2
    assert m1.producing_row == row1
    assert m1.index_in_producing_row == 0
    assert m1.is_produced()
    assert m1.is_consumed()
    assert m2.consuming_instruction == skp
    assert m2.consuming_row == row2
    assert m2.producing_row == row1
    assert m2.index_in_producing_row == 1
    assert m2.index_in_consuming_row == 1


def test_skp_produces_one_mesh(skp):
    assert len(skp.produced_meshes) == 1


def test_skp_produced_meshes(skp, row2):
    m = skp.produced_meshes[0]
    assert m.producing_instruction == skp
    assert m.is_produced()
    assert not m.is_consumed()
    assert m.index_in_producing_row == 0
    assert m.producing_row == row2


def test_yarn_over_consumes_no_meshes(yo):
    assert yo.consumed_meshes == []


def test_yarn_over_produces_a_mesh(yo):
    assert len(yo.produced_meshes) == 1
    m = yo.produced_meshes[0]
    assert m.producing_instruction == yo
    assert m.producing_row == yo.row
    assert m.index_in_producing_row == 1


def test_previous_instruction(row0, instruction0):
    assert row0.instructions[1].previous_instruction_in_row == instruction0


def test_next_instruction(row0, instruction0):
    assert instruction0.next_instruction_in_row == row0.instructions[1]


def test_previous_instruction_is_None_at_border(instruction0):
    assert instruction0.previous_instruction_in_row is None


def test_next_instruction_is_None_at_border(row0):
    assert row0.instructions[-1].next_instruction_in_row is None


def test_index_of_instruction_does_not_change(instruction0):
    index1 = instruction0.index_in_row
    index2 = instruction0.index_in_row
    assert index1 == index2


def test_repr(instruction0):
    string = repr(instruction0)
    assert string.startswith("<" + instruction0.__class__.__name__)
    assert str(instruction0.index_in_row) in string
    assert repr(instruction0.row) in string


def test_instruction_consumes_no_mesh_but_has_mesh_index(yo):
    assert yo.index_of_first_consumed_mesh_in_row == 2
    assert yo.index_of_last_consumed_mesh_in_row == 1


def test_index_of_last_produced_mesh_is_same_as_first(yo):
    first = yo.index_of_first_produced_mesh_in_row
    last = yo.index_of_last_produced_mesh_in_row
    assert first == last


def test_removed_instruction_raises_exception(removed_instruction):
    with raises(InstructionNotFoundInRow):
        removed_instruction.index_of_first_produced_mesh_in_row
    with raises(InstructionNotFoundInRow):
        removed_instruction.index_of_last_produced_mesh_in_row
    with raises(InstructionNotFoundInRow):
        removed_instruction.index_of_first_consumed_mesh_in_row
    with raises(InstructionNotFoundInRow):
        removed_instruction.index_of_last_consumed_mesh_in_row


def test_instruction_is_in_row(instruction0):
    assert instruction0.is_in_row()


def test_instruction_is_not_in_row(removed_instruction):
    assert not removed_instruction.is_in_row()


def test_repr_removed_instruction(removed_instruction):
    assert removed_instruction.__class__.__name__ in repr(removed_instruction)


def test_repr_meshes(instruction0, row2):
    assert "Mesh" in repr(instruction0.produced_meshes[0])
    assert "Mesh" in repr(instruction0.consumed_meshes[0])
    assert "Mesh" in repr(row2.produced_meshes[0])
