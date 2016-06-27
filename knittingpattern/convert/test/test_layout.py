"""Test the layout of knitting patterns."""
from test_convert import fixture
import os
from knittingpattern.convert.Layout import GridLayout, InstructionInGrid
from knittingpattern import load_from_relative_file
from collections import namedtuple


def coordinates(layout):
    """The coordinates of the layout."""
    return list(layout.walk_instructions(lambda point: (point.x, point.y)))


def sizes(layout):
    """The sizes of the instructions of the layout."""
    return list(layout.walk_instructions(lambda p: (p.width, p.height)))


def instructions(layout):
    """The instructions of the layout."""
    return list(layout.walk_instructions(lambda point: point.instruction))


def row_ids(layout):
    """The ids of the rows of the layout."""
    return list(layout.walk_rows(lambda row: row.id))


def connections(layout):
    """The connections between the rows of the leyout."""
    return list(layout.walk_connections(lambda c: (c.start.xy, c.stop.xy)))


class BaseTest:

    """Base class for a set of tests on knitting patterns."""

    FILE = "block4x4.json"
    PATTERN = "knit"
    COORDINATES = [(x, y) for y in range(4) for x in range(4)]
    SIZES = [(1, 1)] * 16
    ROW_IDS = [1, 2, 3, 4]
    LARGER_CONNECTIONS = []
    BOUNDING_BOX = (0, 0, 4, 4)

    @fixture(scope="class")
    def pattern(self):
        """Teh pattern to test."""
        path = os.path.join("test_patterns", self.FILE)
        pattern_set = load_from_relative_file(__name__, path)
        return pattern_set.patterns[self.PATTERN]

    @fixture(scope="class")
    def grid(self, pattern):
        """The computed grid for the pattern."""
        return GridLayout(pattern)

    def test_coordinates(self, grid):
        """Test the coordinates of the layout."""
        coords = coordinates(grid)
        print("generated:", coords)
        print("expected: ", self.COORDINATES)
        assert coords == self.COORDINATES

    def test_size(self, grid):
        """Test teh sizes of the layout."""
        generated = sizes(grid)
        print("generated:", generated)
        print("expected: ", self.SIZES)
        assert generated == self.SIZES

    def test_instructions(self, grid, pattern):
        """Test that the instructions are returned row-wise."""
        instructions_ = []
        for row_id in self.ROW_IDS:
            for instruction in pattern.rows[row_id].instructions:
                instructions_.append(instruction)
        assert instructions(grid) == instructions_

    def test_row_ids(self, grid):
        """Test the order of rows."""
        assert row_ids(grid) == self.ROW_IDS

    def test_connections(self, grid):
        """test the connections betwen rows."""
        generated = connections(grid)
        print("generated:", generated)
        print("expected: ", self.LARGER_CONNECTIONS)
        assert generated == self.LARGER_CONNECTIONS

    def test_bounding_box(self, grid):
        """Test the bounding box of the layout."""
        assert grid.bounding_box == self.BOUNDING_BOX


class TestBlock4x4(BaseTest):
    """Execute the BaseTest."""


class TestHole(BaseTest):
    """Test if holes are layouted."""
    FILE = "with hole.json"
    SIZES = BaseTest.SIZES[:]
    SIZES[5] = (2, 1)
    SIZES[6] = (0, 1)
    COORDINATES = BaseTest.COORDINATES[:]
    COORDINATES[6] = COORDINATES[7]


class TestAddAndRemoveMeshes(BaseTest):
    """take away and add meshes at the right and left."""
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
    def i_1(self, pattern):
        return pattern.rows[1].instructions

    @fixture
    def i_2(self, pattern):
        return pattern.rows[2].instructions

    @fixture
    def i_3(self, pattern):
        return pattern.rows[3].instructions

    @fixture
    def i_4(self, pattern):
        return pattern.rows[4].instructions

    @fixture
    def instructions(self, i_1, i_2, i_3, i_4):
        return i_1 + i_2 + i_3 + i_4

    def test_all_consume_one_mesh(self, instructions):
        assert all(i.number_of_consumed_meshes == 1
                   for i in instructions)

    def test_all_produce_one_mesh(self, instructions):
        assert all(i.number_of_produced_meshes == 1
                   for i in instructions)

    # i_1 produced

    def test_i_1_0_is_not_produced(self, i_1):
        assert i_1[0].producing_instructions == [None]

    def test_i_1_1_is_not_produced(self, i_1):
        assert i_1[1].producing_instructions == [None]

    def test_i_1_2_is_not_produced(self, i_1):
        assert i_1[2].producing_instructions == [None]

    def test_i_1_3_is_not_produced(self, i_1):
        assert i_1[3].producing_instructions == [None]

    # i_1 consumed

    def test_i_1_0_consumed(self, i_1, i_2):
        assert i_1[0].consuming_instructions == [i_2[0]]

    def test_i_1_1_consumed(self, i_1, i_2):
        assert i_1[1].consuming_instructions == [i_2[1]]

    def test_i_1_2_consumed(self, i_1, i_2):
        assert i_1[2].consuming_instructions == [i_2[2]]

    def test_i_1_3_consumed(self, i_1, i_2):
        assert i_1[3].consuming_instructions == [i_2[3]]

    # i_2 produced

    def test_i_2_0_produced(self, i_1, i_2):
        assert i_2[0].producing_instructions == [i_1[0]]

    def test_i_2_1_produced(self, i_1, i_2):
        assert i_2[1].producing_instructions == [i_1[1]]

    def test_i_2_2_produced(self, i_1, i_2):
        assert i_2[2].producing_instructions == [i_1[2]]

    def test_i_2_3_produced(self, i_1, i_2):
        assert i_2[3].producing_instructions == [i_1[3]]

    def test_i_2_4_produced(self, i_2):
        assert i_2[4].producing_instructions == [None]

    # i_2 consumed

    def test_i_2_0_consumed(self, i_2, i_3):
        assert i_2[0].consuming_instructions == [i_3[0]]

    def test_i_2_1_consumed(self, i_2, i_3):
        assert i_2[1].consuming_instructions == [i_3[1]]

    def test_i_2_2_consumed(self, i_2, i_3):
        assert i_2[2].consuming_instructions == [i_3[2]]

    def test_i_2_3_not_consumed(self, i_2):
        assert i_2[3].consuming_instructions == [None]

    def test_i_2_4_not_consumed(self, i_2):
        assert i_2[4].consuming_instructions == [None]

    # i_3 produced

    def test_i_3_0_produced(self, i_2, i_3):
        assert i_3[0].producing_instructions == [i_2[0]]

    def test_i_3_1_produced(self, i_2, i_3):
        assert i_3[1].producing_instructions == [i_2[1]]

    def test_i_3_2_produced(self, i_2, i_3):
        assert i_3[2].producing_instructions == [i_2[2]]

    # i_3 consumed

    def test_i_3_0_consumed(self, i_3, i_4):
        assert i_3[0].consuming_instructions == [i_4[1]]

    def test_i_3_1_consumed(self, i_3, i_4):
        assert i_3[1].consuming_instructions == [i_4[2]]

    def test_i_3_2_consumed(self, i_3, i_4):
        assert i_3[2].consuming_instructions == [i_4[3]]

    # i_4 produced

    def test_i_4_0_not_produced(self, i_4):
        assert i_4[0].producing_instructions == [None]

    def test_i_4_1_produced(self, i_3, i_4):
        assert i_4[1].producing_instructions == [i_3[0]]

    def test_i_4_2_produced(self, i_3, i_4):
        assert i_4[2].producing_instructions == [i_3[1]]

    def test_i_4_3_produced(self, i_3, i_4):
        assert i_4[3].producing_instructions == [i_3[2]]

    def test_i_4_4_not_produced(self, i_4):
        assert i_4[4].producing_instructions == [None]

    # i_4 consumed

    def test_i_4_0_not_consumed(self, i_4):
        assert i_4[0].consuming_instructions == [None]

    def test_i_4_1_not_consumed(self, i_4):
        assert i_4[1].consuming_instructions == [None]

    def test_i_4_2_not_consumed(self, i_4):
        assert i_4[2].consuming_instructions == [None]

    def test_i_4_3_not_consumed(self, i_4):
        assert i_4[3].consuming_instructions == [None]

    def test_i_4_4_not_consumed(self, i_4):
        assert i_4[4].consuming_instructions == [None]


class TestParallelRows(BaseTest):
    """Test unconnected rows of different sizes."""
    FILE = "split_up_and_add_rows.json"
    SIZES = [(1, 1)] * 15
    SIZES[-2] = (2, 1)
    COORDINATES = [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
            (3, 1), (4, 1),
            (0, 2), (1, 2),  # could also be (0, 1), (1, 1)
            (3, 2), (4, 2),
            (0, 3), (1, 3), (2, 3), (4, 3)
        ]
    ROW_IDS = ["1.1", "2.2", "2.1", "3.2", "4.1"]
    # LARGER_CONNECTIONS = [((0, 1), (0, 3)), ((1, 1), (1, 3))]
    LARGER_CONNECTIONS = [((0, 0), (0, 2)), ((1, 0), (1, 2))]
    BOUNDING_BOX = (0, 0, 5, 4)

    @fixture
    def row_4(self, pattern):
        return pattern.rows["4.1"]

    @fixture
    def skp(self, row_4):
        return row_4.instructions[2]

    def test_skp_has_2_consumed_meshes(self, skp):
        """Test skp consumes two meshes."""
        assert skp.type == "skp"
        assert skp.number_of_consumed_meshes == 2

    def test_row_4_1_consumes_5_meshes(self, row_4):
        """Test: the yo in the last row adds to the skp so the width is 5."""
        assert row_4.number_of_consumed_meshes == 5
        assert len(row_4.consumed_meshes) == 5

Instruction = namedtuple("Instruction", ["color", "number_of_consumed_meshes"])


def test_get_color_from_instruction_in_grid():
    """Test the color attribute."""
    instruction = Instruction("black", 1)
    instruction_in_grid = InstructionInGrid(instruction, (0, 0))
    assert instruction_in_grid.color == "black"


class TestSmallCafe(BaseTest):
    """This test tests the negative expansion of rows.

    If you start expanding in the middle, this tests that all rows are
    included.
    """
    FILE = "small-cafe.json"
    PATTERN = "A.2"
    SIZES = \
        [(1, 1)] * 12 + \
        [(0, 1), (1, 1), (0, 1)] + [(1, 1)] * 11 + \
        [(1, 1)] * 14 + \
        [(1, 1)] * 3 + [(0, 1)] + [(1, 1)] * 11 + [(0, 1)] + \
        [(1, 1)] * 16
    COORDINATES = \
        [(i, -1) for i in range(12)] + \
        [(0, 0), (0, 0), (1, 0)] + [(i, 0) for i in range(1, 12)] + \
        [(i, 1) for i in range(-1, 13)] + \
        [(-1, 2), (0, 2), (1, 2), (2, 2)] + [(i, 2) for i in range(2, 13)] + \
        [(13, 2)] + \
        [(i, 3) for i in range(-2, 14)]
    ROW_IDS = ["B.first", "A.2.25", "A.2.26", "A.2.27", "A.2.28"]
    LARGER_CONNECTIONS = []
    BOUNDING_BOX = (-2, -1, 15, 4)


class TestCastOffAndBindOn(BaseTest):
    """Cast On and Bind off have no size but must be layouted differently."""
    FILE = "cast_on_and_bind_off.json"
    SIZES = [(1, 1)] * 12
    COORDINATES = [(x, y) for y in range(3) for x in range(4)]
    ROW_IDS = [1, 2, 3]
    LARGER_CONNECTIONS = []
    BOUNDING_BOX = (0, 0, 4, 3)

    @fixture
    def cast_on(self, co_row):
        return co_row.instructions[0]

    @fixture
    def co_row(self, pattern):
        return pattern.rows[1]

    @fixture
    def co_row_in_grid(self, grid, co_row):
        return grid.row_in_grid(co_row)

    def test_cast_on_has_layout_specific_width(self, cast_on):
        """Test that cast On has a custom width."""
        assert cast_on["grid-layout"]["width"] == 1

    def test_first_row_has_width_4(self, co_row_in_grid):
        """Test that the Cast On row has a width."""
        assert co_row_in_grid.width == 4


# TODO
#
# def test_use_row_with_lowest_number_of_incoming_connections_as_first_row():
#     fail()
#
#
# def test_if_row_with_lowest_number_of_connections_exist_use_smallest_id():
#     fail()
