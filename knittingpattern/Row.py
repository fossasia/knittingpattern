from .Prototype import *

ID = "id"


class Row(Prototype):

    def __init__(self, id, values, inheriting_from = []):
        super().__init__(values, inheriting_from)
        self._id = id
        self._values = values
        self._instructions = []
        self._mapping_to_row = {}

    @property
    def id(self):
        return self._id

    @property
    def instructions(self):
        return self._instructions

    @property
    def produced_meshes(self):
        return []
        
    @property
    def consumed_meshes(self):
        return []

    def map_mesh_index_to_row(self, mesh_index):
        pass
        
    @property
    def number_of_produced_meshes(self):
        return sum(instruction.number_of_produced_meshes
                   for instruction in self.instructions)
    
    @property
    def number_of_consumed_meshes(self):
        return sum(instruction.number_of_consumed_meshes
                   for instruction in self.instructions)
                   
    def map_number_of_meshes_to_row(self, start_index,
                                    stop_index, row,
                                    row_start_index):
        mesh_index_in_row = row_start_index
        for mesh_index in range(start_index, stop_index):
            self.map_mesh_index_to_row(mesh_index, row, mesh_index_in_row)
            mesh_index_in_row += 1
        
        
    def map_mesh_index_to_row(self, mesh_index, row = None, 
                              mesh_index_in_row = None):
        if row is None:
            if mesh_index < 0 or mesh_index >= self.number_of_produced_meshes:
                message = "I only have {} produced meshes "\
                          "but you try to access mesh {}.".format(
                                  self.number_of_produced_meshes, 
                                  mesh_index
                              )
                raise IndexError(message)
            return self._mapping_to_row.get(mesh_index)
        self._mapping_to_row[mesh_index] = (row, mesh_index_in_row)

    
__all__ = ["Row"]
