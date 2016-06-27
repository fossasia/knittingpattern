"""Map ``(x, y)`` coordinates to instructions

"""
from itertools import chain
from collections import namedtuple


INSTRUCTION_HEIGHT = 1  #: the default height of an instruction in the grid

#: This is the key to the "grid-layout"
#:
#: Values for the layout can be specified in each instruction.
#:
#: "grid-layout" : {
#:     "width" : 1
#: }
#:
#: .. seealso:: :data:`width`
GRID_LAYOUT = "grid-layout"

#: the width of the instruction in the grid layout, if specified.
#: .. seealso:: :data:`GRID_LAYOUT`
WIDTH = "width"
Point = namedtuple("Point", ["x", "y"])


class InGrid(object):

    """Base class for things in a grid"""

    def __init__(self, position):
        """Create a new InGrid object."""
        self._position = position

    @property
    def x(self):
        """:return: x coordinate in the grid
        :rtype: float
        """
        return self._position.x

    @property
    def y(self):
        """:return: y coordinate in the grid
        :rtype: float
        """
        return self._position.y

    @property
    def xy(self):
        """:return: ``(x, y)`` coordinate in the grid
        :rtype: tuple
        """
        return self._position

    @property
    def yx(self):
        """:return: ``(y, x)`` coordinate in the grid
        :rtype: tuple
        """
        return self._position.y, self._position.x

    @property
    def width(self):
        """:return: width of the object on the grid
        :rtype: float
        """

        return self._width

    @property
    def height(self):
        """:return: height of the object on the grid
        :rtype: float
        """
        return INSTRUCTION_HEIGHT

    @property
    def row(self):
        """:return: row of the object on the grid
        :rtype: knittingpattern.Row.Row
        """
        return self._row

    @property
    def bounding_box(self):
        """The bounding box of this object.

        :return: (min x, min y, max x, max y)
        :rtype: tuple
        """
        return self._bounding_box

    @property
    def id(self):
        """The id of this object."""
        return self._id


class InstructionInGrid(InGrid):

    """Holder of an instruction in the GridLayout."""

    def __init__(self, instruction, position):
        """
        :param instruction: an :class:`instruction
          <knittingpattern.Instruction.InstructionInRow>`
        :param Point position: the position of the :paramref:`instruction`

        """
        self._instruction = instruction
        super().__init__(position)

    @property
    def _width(self):
        """For ``self.width``."""
        layout = self._instruction.get(GRID_LAYOUT)
        if layout is not None:
            width = layout.get(WIDTH)
            if width is not None:
                return width
        return self._instruction.number_of_consumed_meshes

    @property
    def instruction(self):
        """The instruction.

        :return: instruction that is placed on the grid
        :rtype: knittingpattern.Instruction.InstructionInRow
        """
        return self._instruction

    @property
    def color(self):
        """The color of the instruction.

        :return: the color of the :attr:`instruction`
        """
        return self._instruction.color

    def _row(self):
        """For ``self.row``."""
        return self._instruction.row


class RowInGrid(InGrid):
    """Assign x and y coordinates to rows."""

    def __init__(self, row, position):
        """Create a new row in the grid."""
        super().__init__(position)
        self._row = row

    @property
    def _width(self):
        """:return: the number of consumed meshes"""
        return sum(map(lambda i: i.width, self.instructions))

    @property
    def instructions(self):
        """The instructions in a grid.

        :return: the :class:`instructions in a grid <InstructionInGrid>` of
          this row
        :rtype: list
        """
        x = self.x
        y = self.y
        result = []
        for instruction in self._row.instructions:
            instruction_in_grid = InstructionInGrid(instruction, Point(x, y))
            x += instruction_in_grid.width
            result.append(instruction_in_grid)
        return result

    @property
    def _bounding_box(self):
        min_x = self.x
        min_y = self.y
        max_x = min_x + max(self._row.number_of_consumed_meshes,
                            self._row.number_of_produced_meshes)
        max_y = min_y + self.height
        return min_x, min_y, max_x, max_y

    @property
    def _id(self):
        return self._row.id


def identity(object_):
    """:return: the argument"""
    return object_


class _RecursiveWalk(object):
    """This class starts walking the knitting pattern and maps instructions to
    positions in the grid that is created."""

    def __init__(self, first_instruction):
        """Start walking the knitting pattern starting from first_instruction.
        """
        self._rows_in_grid = {}
        self._todo = []
        self._expand(first_instruction.row, Point(0, 0), [])
        self._walk()

    def _expand(self, row, consumed_position, passed):
        """Add the arguments `(args, kw)` to `_walk` to the todo list."""
        self._todo.append((row, consumed_position, passed))

    def _step(self, row, position, passed):
        """Walk through the knitting pattern by expanding an row."""
        if row in passed or not self._row_should_be_placed(row, position):
            return
        self._place_row(row, position)
        passed = [row] + passed
        # print("{}{} at\t{} {}".format("  " * len(passed), row, position,
        #                               passed))
        for i, produced_mesh in enumerate(row.produced_meshes):
            self._expand_produced_mesh(produced_mesh, i, position, passed)
        for i, consumed_mesh in enumerate(row.consumed_meshes):
            self._expand_consumed_mesh(consumed_mesh, i, position, passed)

    def _expand_consumed_mesh(self, mesh, mesh_index, row_position, passed):
        """expand the consumed meshes"""
        if not mesh.is_produced():
            return
        row = mesh.producing_row
        position = Point(
                row_position.x + mesh.index_in_producing_row - mesh_index,
                row_position.y - INSTRUCTION_HEIGHT
            )
        self._expand(row, position, passed)

    def _expand_produced_mesh(self, mesh, mesh_index, row_position, passed):
        """expand the produced meshes"""
        if not mesh.is_consumed():
            return
        row = mesh.consuming_row
        position = Point(
                row_position.x - mesh.index_in_consuming_row + mesh_index,
                row_position.y + INSTRUCTION_HEIGHT
            )
        self._expand(row, position, passed)

    def _row_should_be_placed(self, row, position):
        """:return: whether to place this instruction"""
        placed_row = self._rows_in_grid.get(row)
        return placed_row is None or placed_row.y < position.y

    def _place_row(self, row, position):
        """place the instruction on a grid"""
        self._rows_in_grid[row] = RowInGrid(row, position)

    def _walk(self):
        """Loop through all the instructions that are `_todo`."""
        while self._todo:
            args = self._todo.pop(0)
            self._step(*args)

    def instruction_in_grid(self, instruction):
        """Returns an `InstructionInGrid` object for the `instruction`"""
        row_position = self._rows_in_grid[instruction.row].xy
        x = instruction.index_of_first_consumed_mesh_in_row
        position = Point(row_position.x + x, row_position.y)
        return InstructionInGrid(instruction, position)

    def row_in_grid(self, row):
        """Returns an `RowInGrid` object for the `row`"""
        return self._rows_in_grid[row]


class Connection(object):
    """a connection between two :class:`InstructionInGrid` objects"""

    def __init__(self, start, stop):
        """
        :param InstructionInGrid start: the start of the connection
        :param InstructionInGrid stop: the end of the connection
        """
        self._start = start
        self._stop = stop

    @property
    def start(self):
        """:return: the start of the connection
        :rtype: InstructionInGrid
        """
        return self._start

    @property
    def stop(self):
        """:return: the end of the connection
        :rtype: InstructionInGrid
        """
        return self._stop

    def is_visible(self):
        """:return: is this connection is visible
        :rtype: bool

        A connection is visible if it is longer that 0."""
        if self._start.y + 1 < self._stop.y:
            return True
        return False


class GridLayout(object):
    """This class places the instructions at ``(x, y)`` positions."""

    def __init__(self, pattern):
        """
        :param knittingpattern.KnittingPattern.KnittingPattern pattern: the
          pattern to layout

        """
        self._pattern = pattern
        self._rows = list(pattern.rows)
        self._walk = _RecursiveWalk(self._rows[0].instructions[0])
        self._rows.sort(key=lambda row: self._walk.row_in_grid(row).yx)

    def walk_instructions(self, mapping=identity):
        """Iterate over instructions.

        :return: an iterator over :class:`instructions in grid
          <InstructionInGrid>`
        :param mapping: funcion to map the result

        .. code:: python

            for pos, c in layout.walk_instructions(lambda i: (i.xy, i.color)):
                print("color {} at {}".format(c, pos))

        """
        instructions = chain(*self.walk_rows(lambda row: row.instructions))
        return map(mapping, instructions)

    def walk_rows(self, mapping=identity):
        """Iterate over rows.

        :return: an iterator over :class:`rows <RowsInGrid>`
        :param mapping: funcion to map the result, see
          :meth:`walk_instructions` for an example usage
        """
        row_in_grid = self._walk.row_in_grid
        return map(lambda row: mapping(row_in_grid(row)), self._rows)

    def walk_connections(self, mapping=identity):
        """Iterate over connections between instructions.

        :return: an iterator over :class:`connections <Connection>` between
          :class:`instructions in grid <InstructionInGrid>`
        :param mapping: funcion to map the result, see
          :meth:`walk_instructions` for an example usage
        """
        for start in self.walk_instructions():
            for stop_instruction in start.instruction.consuming_instructions:
                if stop_instruction is None:
                    continue
                stop = self._walk.instruction_in_grid(stop_instruction)
                connection = Connection(start, stop)
                if connection.is_visible():
                    # print("connection:",
                    #      connection.start.instruction,
                    #      connection.stop.instruction)
                    yield mapping(connection)

    @property
    def bounding_box(self):
        """The minimum and maximum bounds of this layout.

        :return: ``(min_x, min_y, max_x, max_y)`` the bounding box
          of this layout
        :rtype: tuple
        """
        min_x, min_y, max_x, max_y = zip(*list(self.walk_rows(
            lambda row: row.bounding_box)))
        return min(min_x), min(min_y), max(max_x), max(max_y)

    def row_in_grid(self, row):
        """The a RowInGrid for the row with position information.

        :return: a row in the grid
        :rtype: RowInGrid
        """
        return self._walk.row_in_grid(row)


__all__ = ["GridLayout", "InstructionInGrid", "Connection", "identity",
           "Point", "INSTRUCTION_HEIGHT", "InGrid", "RowInGrid"]
