from itertools import chain


class InstructionInGrid(object):

    def __init__(self, instruction, x, y):
        self.instruction = instruction
        self.x = x
        self.y = y
        self.width = instruction.number_of_consumed_meshes
        self.height = 1

    @property
    def xy(self):
        return self.x, self.y


def identity(object):
    return object

class RecursiveWalk(object):
    def __init__(self, first_instruction):
        self.first_instruction = first_instruction
        self.instructions_in_grid = {}
        self.todo = []
        self.expand(first_instruction, 0, 0, 0, 0)
        self.walk()
        
    def expand(self, *args, **kw):
        self.todo.append((args, kw))
        
    def _walk(self, instruction, cx, cy, px, py, 
              subtract_width=False, row = 0):
        if instruction is None: return
        if subtract_width:
            cx -= instruction.number_of_consumed_meshes
            px -= instruction.number_of_produced_meshes
        if instruction in self.instructions_in_grid: 
            i2 = self.instructions_in_grid[instruction]
            if i2.y >= cy: return
        print("{}{} at ({},{})({},{}) {}".format(
                  "  " * row, instruction, 
                  cx, cy, px, py, subtract_width
              ))
        in_grid = InstructionInGrid(instruction, cx, cy)
        self.instructions_in_grid[instruction] = in_grid
        self.expand(instruction.previous_instruction_in_row, 
                    cx, cy, px, py, subtract_width= True, row= row)
        self.expand(instruction.next_instruction_in_row, 
                    cx + instruction.number_of_consumed_meshes, cy, 
                    px + instruction.number_of_produced_meshes, py, 
                    row= row)
        for i, mesh in enumerate(instruction.produced_meshes):
            if not mesh.is_consumed(): continue
            x = px + i - mesh.mesh_index_in_consuming_instruction
            y = py + in_grid.height
            self.expand(mesh.consuming_instruction, 
                        x, y, 
                        x, y, 
                        row= row + 1)
                       
    def walk(self):
        while self.todo:
            args, kw = self.todo.pop(0)
            self._walk(*args, **kw)

    def in_grid(self, instruction):
        return self.instructions_in_grid[instruction]

        
class Connection(object):
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def is_visible(self):
        if self.start.y + 1 < self.stop.y: return True
        return False

class GridLayout(object):
    def __init__(self, pattern):
        self.pattern = pattern
        self._rows = list(sorted(self.pattern.rows))
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
                if stop_instruction is None: continue
                stop = self._walk.in_grid(stop_instruction)
                connection = Connection(start, stop)
                if connection.is_visible():
                    print("connection:", 
                          connection.start.instruction, 
                          connection.stop.instruction)
                    yield mapping(connection)