

class Mesh(object):
    
    def __init__(self, instruction_produced_by, mesh_index_in_instruction):
        self._instruction_produced_by = instruction_produced_by
        self._mesh_index_in_instruction = mesh_index_in_instruction
        
        
    @property
    def mesh_index_in_instruction(self):
        return self._mesh_index_in_instruction
        
    @property
    def instruction_produced_by(self):
        return self._instruction_produced_by
        
    @property
    def produced_in_row(self):
        return self.instruction_produced_by.row
        
    def is_produced(self):
        return True
    
    def is_consumed(self):
        return True
        
    @property
    def mesh_index_in_producing_row(self):
        index = 0
        for instruction in self.produced_in_row.instructions:
            if instruction == self.instruction_produced_by:
                break
            index += instruction.number_of_produced_meshes
        index += self.mesh_index_in_instruction
        return index
        
    def is_knit(self):
        return self.instruction_produced_by.does_knit()