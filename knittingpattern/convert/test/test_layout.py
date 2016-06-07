from test import *
import os
from knittingpattern.convert.Layout import GridLayout
from knittingpattern import load_from_relative_file


def coordinates(layout):
    return layout.walk_instructions(lambda point: (point.x, point.y))


def sizes(layout):
    return layout.walk_instructions(lambda point: (point.width, point.height))


def instructions(layout):
    return layout.walk_instructions(lambda point: point.instruction)


def row_ids(layout):
    return layout.walk_rows(lambda row: row.id)


def connections(layout):
    return layout.walk_connections(lambda c: (c.start_point.xy,
                                              c.end_point.xy))


class BaseTest:

    FILE = "block4x4.json"
    PATTERN = "knit"
    COORDINATES = [(x, y) for y in range(4) for x in range(4)]
    SIZES = [(1, 1)] * 16
    ROW_IDS = [1, 2, 3, 4]
    LARGER_CONNECTIONS = []

    @fixture
    def pattern(self):
        pattern_set = load_from_relative_file(__name__, os.path.join("test_patterns", self.FILE))
        return pattern_set.patterns[self.PATTERN]

    @fixture
    def grid(self, pattern):
        return GridLayout(pattern)

    def test_coordinates(self, grid):
        coords = coordinates(grid)
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
    

class _TestSplitUpMeshes(BaseTest):
    FILE = "split_up_and_add_rows.json"
    SIZES = [(1, 1)] * 17
    SIZES[-2] = (2, 1)
    COORDINATES = [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
            (0, 1), (1, 1), 
            (3, 1), (4, 1),
            (3, 2), (4, 2),
            (0, 3), (1, 3), (2, 3), (4, 3)
        ]
    ROW_IDS = ["1.1", "2.1", "2.2", "3.2", "4.1"]
    LARGER_CONNECTIONS = [((0, 1), (0, 3)), ((1, 1), (1, 3)), ((2, 0), (2, 3))]




