"""Map ``(x, y)`` coordinates to instructions

"""
from itertools import chain


class InstructionInGrid(object):
    """Holder of an instruction in the GridLayout."""

    def __init__(self, instruction, x, y):
        """
        :param instruction: an :class:`instruction
          <knittingpattern.Instruction.InstructionInRow>`
        :param float x: the x position of the :paramref:`instruction`
        :param float y: the y position of the :paramref:`instruction`

        """
        self._instruction = instruction
        self._x = x
        self._y = y
        self._width = instruction.number_of_consumed_meshes
        self._height = 1

    @property
    def x(self):
        """:return: x coordinate in the grid
        :rtype: float
        """
        return self._x

    @property
    def y(self):
        """:return: y coordinate in the grid
        :rtype: float
        """
        return self._y

    @property
    def xy(self):
        """:return: ``(x, y)`` coordinate in the grid
        :rtype: float
        """
        return self._x, self._y

    @property
    def width(self):
        """:return: width of the instruction on the grid
        :rtype: float
        """
        return self._width

    @property
    def height(self):
        """:return: height of the instruction on the grid
        :rtype: float
        """
        return self._height

    @property
    def instruction(self):
        """:return: instruction that is placed on the grid
        :rtype: knittingpattern.Instruction.InstructionInRow
        """
        return self._instruction

    @property
    def color(self):
        """:return: the color of the :attr:`instruction`"""
        return self._instruction.color


def identity(object):
    """:return: the argument"""
    return object


class _RecursiveWalk(object):
    """This class starts walking the knitting pattern and maps instructions to
    positions in the grid that is created."""

    def __init__(self, first_instruction):
        """Start walking the knitting pattern starting from first_instruction.
        """
        self._first_instruction = first_instruction
        self._instructions_in_grid = {}
        self._todo = []
        self._expand(first_instruction, 0, 0, 0, 0)
        self._walk()

    def _expand(self, *args, **kw):
        """Add the arguments `(args, kw)` to `_walk` to the todo list."""
        self._todo.append((args, kw))

    def _step(self, instruction, cx, cy, px, py,
              subtract_width=False, passed=[], rows=0):
        """Walk through the knitting pattern by expading an instruction."""
        if instruction is None:
            return
        if instruction in passed:
            return
        if subtract_width:
            cx -= instruction.number_of_consumed_meshes
            px -= instruction.number_of_produced_meshes
        if instruction in self._instructions_in_grid:
            i2 = self._instructions_in_grid[instruction]
            if i2.y >= cy:
                return
        # print("{}{} at ({},{})({},{}) {}".format(
        #          "  " * rows, instruction,
        #          cx, cy, px, py, subtract_width
        #      ))
        new_passed = [instruction] + passed
        in_grid = InstructionInGrid(instruction, cx, cy)
        self._instructions_in_grid[instruction] = in_grid
        self._expand(instruction.previous_instruction_in_row,
                     cx, cy, px, py, subtract_width=True, passed=new_passed,
                     rows=rows)
        self._expand(instruction.next_instruction_in_row,
                     cx + instruction.number_of_consumed_meshes, cy,
                     px + instruction.number_of_produced_meshes, py,
                     passed=new_passed, rows=rows)
        for i, mesh in enumerate(instruction.produced_meshes):
            if not mesh.is_consumed():
                continue
            x = px + i - mesh.mesh_index_in_consuming_instruction
            y = py + in_grid.height
            self._expand(mesh.consuming_instruction, x, y, x, y,
                         passed=new_passed, rows=rows + 1)

    def _walk(self):
        """Loop through all the instructions that are `_todo`."""
        while self._todo:
            args, kw = self._todo.pop(0)
            self._step(*args, **kw)

    def in_grid(self, instruction):
        """Returns an `InstructionInGrid` object for the `instruction`"""
        return self._instructions_in_grid[instruction]


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
        self._rows = list(sorted(self._pattern.rows))
        self._walk = _RecursiveWalk(self._rows[0].instructions[0])

    def walk_instructions(self, mapping=identity):
        """
        :return: an iterator over :class:`instructions in grid
          <InstructionInGrid>`
        :param mapping: funcion to map the result

        .. code:: python

            for pos, c in layout.walk_instructions(lambda i: (i.xy, i.color)):
                print("color {} at {}".format(c, pos))

        """
        instructions = chain(*self.walk_rows(lambda row: row.instructions))
        grid = map(self._walk.in_grid, instructions)
        return map(mapping, grid)

    def walk_rows(self, mapping=identity):
        """
        :return: an iterator over :class:`rows <knittingpattern.Row.Row>`
        :param mapping: funcion to map the result, see
          :meth:`walk_instructions` for an example usage
        """
        return map(mapping, self._rows)

    def walk_connections(self, mapping=identity):
        """
        :return: an iterator over :class:`connections <Connection>` between
          :class:`instructions in grid <InstructionInGrid>`
        :param mapping: funcion to map the result, see
          :meth:`walk_instructions` for an example usage
        """
        for start in self.walk_instructions():
            for stop_instruction in start.instruction.consuming_instructions:
                if stop_instruction is None:
                    continue
                stop = self._walk.in_grid(stop_instruction)
                connection = Connection(start, stop)
                if connection.is_visible():
                    # print("connection:",
                    #      connection.start.instruction,
                    #      connection.stop.instruction)
                    yield mapping(connection)

    @property
    def bounding_box(self):
        """
        :return: ``(min_x, min_y, max_x + 1, max_y + 1)`` the bounding box
          of this layout
        :rtype: tuple
        """
        x, y = zip(*self.walk_instructions(
                lambda instruction: (instruction.x, instruction.y)
            ))
        return min(x), min(y), max(x) + 1, max(y) + 1

__all__ = ["GridLayout", "InstructionInGrid", "Connection", "identity"]
