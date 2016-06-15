from test import *
import os
from knittingpattern.convert.Layout import GridLayout, InstructionInGrid
from knittingpattern import load_from_relative_file
from collections import namedtuple


def coordinates(layout):
    return list(layout.walk_instructions(lambda point: (point.x, point.y)))


def sizes(layout):
    return list(layout.walk_instructions(lambda p: (p.width, p.height)))


def instructions(layout):
    return list(layout.walk_instructions(lambda point: point.instruction))


def row_ids(layout):
    return list(layout.walk_rows(lambda row: row.id))


def connections(layout):
    return list(layout.walk_connections(lambda c: (c.start.xy, c.stop.xy)))


class BaseTest:

    FILE = "block4x4.json"
    PATTERN = "knit"
    COORDINATES = [(x, y) for y in range(4) for x in range(4)]
    SIZES = [(1, 1)] * 16
    ROW_IDS = [1, 2, 3, 4]
    LARGER_CONNECTIONS = []
    BOUNDING_BOX = (0, 0, 4, 4)

    @fixture
    def pattern(self):
        path = os.path.join("test_patterns", self.FILE)
        pattern_set = load_from_relative_file(__name__, path)
        return pattern_set.patterns[self.PATTERN]

    @fixture
    def grid(self, pattern):
        return GridLayout(pattern)

    def test_coordinates(self, grid):
        coords = coordinates(grid)
        print("generated:", coords)
        print("expected: ", self.COORDINATES)
        assert coords == self.COORDINATES

    def test_size(self, grid):
        assert sizes(grid) == self.SIZES

    def test_instructions(self, grid, pattern):
        instructions_ = []
        for row_id in self.ROW_IDS:
            for instruction in pattern.rows[row_id].instructions:
                instructions_.append(instruction)
        assert instructions(grid) == instructions_

    def test_row_ids(self, grid):
        assert row_ids(grid) == self.ROW_IDS

    def test_connections(self, grid):
        assert connections(grid) == self.LARGER_CONNECTIONS

    def test_bounding_box(self, grid):
        assert grid.bounding_box == self.BOUNDING_BOX


class TestBlock4x4(BaseTest):
    pass


class TestHole(BaseTest):
    FILE = "with hole.json"
    SIZES = BaseTest.SIZES[:]
    SIZES[5] = (2, 1)
    SIZES[6] = (0, 1)
    COORDINATES = BaseTest.COORDINATES[:]
    COORDINATES[6] = COORDINATES[7]


class TestAddAndRemoveMeshes(BaseTest):
    FILE = "add and remove meshes.json"
    SIZES = [(1, 1)] * 17
    COORDINATES = [
            (0, 0), (1, 0), (2, 0), (3, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
            (0, 2), (1, 2), (2, 2),
            (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3)
        ]
    BOUNDING_BOX = (-1, 0, 5, 4)

    # test how instructions are connected

    @fixture
    def i1(self, pattern):
        return pattern.rows[1].instructions

    @fixture
    def i2(self, pattern):
        return pattern.rows[2].instructions

    @fixture
    def i3(self, pattern):
        return pattern.rows[3].instructions

    @fixture
    def i4(self, pattern):
        return pattern.rows[4].instructions

    @fixture
    def instructions(self, i1, i2, i3, i4):
        return i1 + i2 + i3 + i4

    def test_all_consume_one_mesh(self, instructions):
        assert all(i.number_of_consumed_meshes == 1
                   for i in instructions)

    def test_all_produce_one_mesh(self, instructions):
        assert all(i.number_of_produced_meshes == 1
                   for i in instructions)

    # i1 produced

    def test_i1_0_is_not_produced(self, i1):
        assert i1[0].producing_instructions == [None]

    def test_i1_1_is_not_produced(self, i1):
        assert i1[1].producing_instructions == [None]

    def test_i1_2_is_not_produced(self, i1):
        assert i1[2].producing_instructions == [None]

    def test_i1_3_is_not_produced(self, i1):
        assert i1[3].producing_instructions == [None]

    # i1 consumed

    def test_i1_0_consumed(self, i1, i2):
        assert i1[0].consuming_instructions == [i2[0]]

    def test_i1_1_consumed(self, i1, i2):
        assert i1[1].consuming_instructions == [i2[1]]

    def test_i1_2_consumed(self, i1, i2):
        assert i1[2].consuming_instructions == [i2[2]]

    def test_i1_3_consumed(self, i1, i2):
        assert i1[3].consuming_instructions == [i2[3]]

    # i2 produced

    def test_i2_0_produced(self, i1, i2):
        assert i2[0].producing_instructions == [i1[0]]

    def test_i2_1_produced(self, i1, i2):
        assert i2[1].producing_instructions == [i1[1]]

    def test_i2_2_produced(self, i1, i2):
        assert i2[2].producing_instructions == [i1[2]]

    def test_i2_3_produced(self, i1, i2):
        assert i2[3].producing_instructions == [i1[3]]

    def test_i2_4_produced(self, i2):
        assert i2[4].producing_instructions == [None]

    # i2 consumed

    def test_i2_0_consumed(self, i2, i3):
        assert i2[0].consuming_instructions == [i3[0]]

    def test_i2_1_consumed(self, i2, i3):
        assert i2[1].consuming_instructions == [i3[1]]

    def test_i2_2_consumed(self, i2, i3):
        assert i2[2].consuming_instructions == [i3[2]]

    def test_i2_3_not_consumed(self, i2):
        assert i2[3].consuming_instructions == [None]

    def test_i2_4_not_consumed(self, i2):
        assert i2[4].consuming_instructions == [None]

    # i3 produced

    def test_i3_0_produced(self, i2, i3):
        assert i3[0].producing_instructions == [i2[0]]

    def test_i3_1_produced(self, i2, i3):
        assert i3[1].producing_instructions == [i2[1]]

    def test_i3_2_produced(self, i2, i3):
        assert i3[2].producing_instructions == [i2[2]]

    # i3 consumed

    def test_i3_0_consumed(self, i3, i4):
        assert i3[0].consuming_instructions == [i4[1]]

    def test_i3_1_consumed(self, i3, i4):
        assert i3[1].consuming_instructions == [i4[2]]

    def test_i3_2_consumed(self, i3, i4):
        assert i3[2].consuming_instructions == [i4[3]]

    # i4 produced

    def test_i4_0_not_produced(self, i4):
        assert i4[0].producing_instructions == [None]

    def test_i4_1_produced(self, i3, i4):
        assert i4[1].producing_instructions == [i3[0]]

    def test_i4_2_produced(self, i3, i4):
        assert i4[2].producing_instructions == [i3[1]]

    def test_i4_3_produced(self, i3, i4):
        assert i4[3].producing_instructions == [i3[2]]

    def test_i4_4_not_produced(self, i4):
        assert i4[4].producing_instructions == [None]

    # i4 consumed

    def test_i4_0_not_consumed(self, i4):
        assert i4[0].consuming_instructions == [None]

    def test_i4_1_not_consumed(self, i4):
        assert i4[1].consuming_instructions == [None]

    def test_i4_2_not_consumed(self, i4):
        assert i4[2].consuming_instructions == [None]

    def test_i4_3_not_consumed(self, i4):
        assert i4[3].consuming_instructions == [None]

    def test_i4_4_not_consumed(self, i4):
        assert i4[4].consuming_instructions == [None]


class TestParallelRows(BaseTest):
    FILE = "split_up_and_add_rows.json"
    SIZES = [(1, 1)] * 15
    SIZES[-2] = (2, 1)
    COORDINATES = [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
            (0, 1), (1, 1),
            (3, 1), (4, 1),
            (3, 2), (4, 2),
            (0, 3), (1, 3), (2, 3), (4, 3)
        ]
    ROW_IDS = ["1.1", "2.1", "2.2", "3.2", "4.1"]
    LARGER_CONNECTIONS = [((0, 1), (0, 3)), ((1, 1), (1, 3))]
    BOUNDING_BOX = (0, 0, 5, 4)

    @fixture
    def r4(self, pattern):
        return pattern.rows["4.1"]

    @fixture
    def skp(self, r4):
        return r4.instructions[2]

    def test_skp_has_2_consumed_meshes(self, skp):
        assert skp.type == "skp"
        assert skp.number_of_consumed_meshes == 2

    def test_row_4_1_consumes_5_meshes(self, r4):
        assert r4.number_of_consumed_meshes == 5
        assert len(r4.consumed_meshes) == 5


def test_use_row_with_lowest_number_of_incoming_connections_as_first_row():
    fail()


def test_if_row_with_lowest_number_of_connections_exist_use_smallest_id():
    fail()


test_use_row_with_lowest_number_of_incoming_connections_as_first_row = "TODO"
test_if_row_with_lowest_number_of_connections_exist_use_smallest_id = "TODO"


def test_InstructionInGrid_get_color_from_instruction():
    Instruction = namedtuple("Instruction", ["color",
                                             "number_of_consumed_meshes"])
    instruction = Instruction("black", 1)
    instruction_in_grid = InstructionInGrid(instruction, 0, 0)
    assert instruction_in_grid.color == "black"
