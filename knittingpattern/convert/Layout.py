"""Map `(x, y)` coordinates to instructions.

"""
from itertools import chain


class InstructionInGrid(object):
    """Holder of an instruction in the GridLayout."""

    def __init__(self, instruction, x, y):
        self._instruction = instruction
        self._x = x
        self._y = y
        self._width = instruction.number_of_consumed_meshes
        self._height = 1

    @property
    def x(self):
        """x coordinate in the grid"""
        return self._x

    @property
    def y(self):
        """y coordinate in the grid"""
        return self._y

    @property
    def xy(self):
        return self._x, self._y

    @property
    def width(self):
        """width of the instruction on the grid"""
        return self._width

    @property
    def height(self):
        """height of the instruction on the grid"""
        return self._height

    @property
    def instruction(self):
        """instruction that is placed on the grid"""
        return self._instruction

    @property
    def color(self):
        """returns the color of the instruction"""
        return self._instruction.color


def identity(object):
    """returns the argument"""
    return object


class RecursiveWalk(object):
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
    """A connection between two `InstructionInGrid` objects."""

    def __init__(self, start, stop):
        self._start = start
        self._stop = stop

    @property
    def start(self):
        """start of the connection

        This is a `InstructionInGrid` object."""
        return self._start

    @property
    def stop(self):
        """stop of the connection

        This is a `InstructionInGrid` object."""
        return self._stop

    def is_visible(self):
        if self._start.y + 1 < self._stop.y:
            return True
        return False


class GridLayout(object):

    def __init__(self, pattern):
        self._pattern = pattern
        self._rows = list(sorted(self._pattern.rows))
        self._walk = RecursiveWalk(self._rows[0].instructions[0])

    def walk_instructions(self, mapping=identity):
        instructions = chain(*self.walk_rows(lambda row: row.instructions))
        grid = map(self._walk.in_grid, instructions)
        return map(mapping, grid)

    def walk_rows(self, mapping=identity):
        return map(mapping, self._rows)

    def walk_connections(self, mapping=identity):
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
        """Returns (min_x, min_y, max_x + 1, max_y + 1)"""
        x, y = zip(*self.walk_instructions(
                lambda instruction: (instruction.x, instruction.y)
            ))
        return min(x), min(y), max(x) + 1, max(y) + 1

__all__ = ["GridLayout"]
