from knittingpattern import load_from_relative_file
from pytest import fixture, raises

@fixture
def p1():
    return load_from_relative_file(__name__, "pattern/row_mapping_pattern.json")


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

class TestRow11:

    def test_first_meshes_map_to_second_row(self, r11, r21):
        assert r11.map_mesh_index_to_row(0) == (r21, 0)
        assert r11.map_mesh_index_to_row(1) == (r21, 1)

    def test_middle_mesh_does_not_map_to_any_row(self, r11):
        assert r11.map_mesh_index_to_row(2) == None
        
    def test_right_meshes_map_to_third_row(self, r11, r22):
        assert r11.map_mesh_index_to_row(3) == (r22, 0)
        assert r11.map_mesh_index_to_row(4) == (r22, 1)
        
    def test_number_of_meshes(self, r11):
        assert r11.number_of_produced_meshes == 5
        assert r11.number_of_consumed_meshes == 4
        
        
class TestMappingErrors:

    def test_lower_indices_create_error(self, r11):
        with raises(IndexError):
            r11.map_mesh_index_to_row(-1)
    
    def test_higher_indices_create_error(self, r11):
        with raises(IndexError):
            r11.map_mesh_index_to_row(5)
            

class TestRow21:

    def test_all_meshes_map_to_last_row(self, r21, r41):
        assert r21.map_mesh_index_to_row(0) == (r41, 0)
        assert r21.map_mesh_index_to_row(1) == (r41, 1)
        
    def test_number_of_meshes(self, r21):
        assert r21.number_of_produced_meshes == 2
        assert r21.number_of_consumed_meshes == 2
        

class TestRow22:

    def test_all_meshes_map_to_row_3(self, r22, r32):
        assert r22.map_mesh_index_to_row(0) == (r32, 0)
        assert r22.map_mesh_index_to_row(1) == (r32, 1)
        
        
class TestRow32:

    def test_all_meshes_map_to_last_row(self, r32, r41):
        assert r32.map_mesh_index_to_row(0) == (r41, 3)
        assert r32.map_mesh_index_to_row(1) == (r41, 4)

        
class TestRow41:

    def test_row_maps_to_nowhere(self, r41):
        for i in range(4):
            assert r41.map_mesh_index_to_row(i) == None

    def test_number_of_meshes(self, r41):
        assert r41.number_of_produced_meshes == 4
        assert r41.number_of_consumed_meshes == 5
        



        