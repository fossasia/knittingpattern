

class Mesh(object):
    
    def __init__(self, produced_by_instruction, mesh_index_in_instruction):
        self._produced_by_instruction = produced_by_instruction
        self._mesh_index_in_instruction = mesh_index_in_instruction
        
        
    @property
    def mesh_index_in_instruction(self):
        return self._mesh_index_in_instruction
        
    @property
    def produced_by_instruction(self):
        return self._produced_by_instruction
        
    @property
    def produced_in_row(self):
        return self.produced_by_instruction.row
        
    def is_produced(self):
        return True
    
    def is_consumed(self):
        return True
        
    @property
    def mesh_index_in_producing_row(self):
        index = 0
        for instruction in self.produced_in_row.instructions:
            if instruction == self.produced_by_instruction:
                break
            index += instruction.number_of_produced_meshes
        index += self.mesh_index_in_instruction
        return index