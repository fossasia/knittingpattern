import itertools

class InstructionInGrid(object):
    def __init__(self, instruction, x, y):
        self.instruction = instruction
        self.x = x
        self.y = y
        self.width = instruction.number_of_consumed_meshes
        self.height = 1

        

class GridLayout(object):
    def __init__(self, pattern):
        self.pattern = pattern
        
    def walk_instructions(self, mapping):
        instruction_grid =  list(self.walk_rows(lambda kack: kack.instructions))
        instruction_objects = []
        for y, row_instructions in enumerate(instruction_grid):
            x = 0
            for instruction in row_instructions:
                instruction_object = InstructionInGrid(instruction, x, y)
                instruction_objects.append(instruction_object)
                x += instruction_object.width
                assert instruction_object.height == 1
        return list(map(mapping, instruction_objects))
        
    def walk_rows(self, mapping):
        return list(map(mapping, sorted(self.pattern.rows)))
        
    def walk_connections(self, mapping):
        return []