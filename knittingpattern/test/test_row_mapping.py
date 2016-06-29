"""Test that the rows of a pattern map the right way."""
from test_knittingpattern import fixture
from knittingpattern import load_from_object
from knittingpattern.Loader import JSONLoader as Loader

relative_path = "pattern/row_mapping_pattern.json"
row_mapping_pattern1 = Loader().relative_file(__name__, relative_path)


@fixture
def p1():
    return load_from_object(row_mapping_pattern1)


@fixture
def a1(p1):
    return p1.patterns["A.1"]


@fixture
def r11(a1):
    return a1.rows["1.1"]


@fixture
def r21(a1):
    return a1.rows["2.1"]


@fixture
def r22(a1):
    return a1.rows["2.2"]


@fixture
def r32(a1):
    return a1.rows["3.2"]


@fixture
def r41(a1):
    return a1.rows["4.1"]


# TODO: test _get_producing_row_and_index

def assert_rows_map(row1, index1, row2, index2):
    produced_mesh = row1.produced_meshes[index1]
    consumed_mesh = row2.consumed_meshes[index2]
    assert produced_mesh.is_connected_to(consumed_mesh)


def assert_is_not_connected(row, index):
    assert not row.produced_meshes[index].is_connected()


class TestRow11:

    def test_first_meshes_map_to_second_row(self, r11, r21):
        assert_rows_map(r11, 0, r21, 0)
        assert_rows_map(r11, 1, r21, 1)

    def test_middle_mesh_does_not_map_to_any_row(self, r11):
        assert_is_not_connected(r11, 2)

    def test_right_meshes_map_to_third_row(self, r11, r22):
        assert_rows_map(r11, 3, r22, 0)
        assert_rows_map(r11, 4, r22, 1)

    def test_number_of_meshes(self, r11):
        assert r11.number_of_produced_meshes == 5
        assert r11.number_of_consumed_meshes == 4


class TestRow21:

    def test_all_meshes_map_to_last_row(self, r21, r41):
        assert_rows_map(r21, 0, r41, 0)
        assert_rows_map(r21, 1, r41, 1)

    def test_number_of_meshes(self, r21):
        assert r21.number_of_produced_meshes == 2
        assert r21.number_of_consumed_meshes == 2


class TestRow22:

    def test_all_meshes_map_to_row_3(self, r22, r32):
        assert_rows_map(r22, 0, r32, 0)
        assert_rows_map(r22, 1, r32, 1)


class TestRow32:

    def test_all_meshes_map_to_last_row(self, r32, r41):
        assert_rows_map(r32, 0, r41, 3)
        assert_rows_map(r32, 1, r41, 4)


class TestRow41:

    def test_row_maps_to_nowhere(self, r41):
        for i in range(4):
            assert_is_not_connected(r41, i)

    def test_number_of_meshes(self, r41):
        assert r41.number_of_produced_meshes == 4
        assert r41.number_of_consumed_meshes == 5
