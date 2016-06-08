from itertools import chain

class InstructionInGrid(object):
    def __init__(self, instruction, x, y, subtract_width=False):
        self.instruction = instruction
        self.x = x
        self.y = y
        self.width = instruction.number_of_consumed_meshes
        self.height = 1
        if subtract_width:
            self.x -= self.width

def identity(object):
    return object
    

class RecursiveWalk(object):
    def __init__(self, first_instruction):
        self.first_instruction = first_instruction
        self.instructions_in_grid = {}
        self.todo = []
        self.expand(first_instruction, 0, 0)
        self.walk()
        
    def expand(self, *args, **kw):
        self.todo.append((args, kw))
        
    def _walk(self, instruction, x, y, subtract_width=False, row = 0):
        if instruction is None: return
        if instruction in self.instructions_in_grid: return
        print("{}{} at {},{} {}".format("  " * row, instruction, x, y, subtract_width))
        in_grid = InstructionInGrid(instruction, x, y, subtract_width=subtract_width)
        self.instructions_in_grid[instruction] = in_grid
        self.expand(instruction.previous_instruction_in_row, x, y, subtract_width= True, row= row)
        self.expand(instruction.next_instruction_in_row, x + in_grid.width, y, row= row)
        for mesh in instruction.produced_meshes:
            if not mesh.is_consumed(): continue
            self.expand(mesh.consuming_instruction, x, y + in_grid.height, row= row + 1)
                       
    def walk(self):
        while self.todo:
            args, kw = self.todo.pop(0)
            self._walk(*args, **kw)

    def in_grid(self, instruction):
        return self.instructions_in_grid[instruction]
        

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
        return []