from .Prototype import *
from itertools import chain

ID = "id"
CONISTENCY_MESSAGE = "The data structure must be consistent."


class Row(Prototype):

    def __init__(self, id, values, inheriting_from=[]):
        super().__init__(values, inheriting_from)
        self._id = id
        self._values = values
        self._instructions = []
        self._mapping_to_row = {}
        self._mapping_from_row = {}

    @property
    def id(self):
        return self._id

    @property
    def instructions(self):
        return self._instructions

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

    def produce_number_of_meshes_for_row(self, start_index,
                                         stop_index, row,
                                         row_start_index):
        mesh_index_in_row = row_start_index
        for mesh_index in range(start_index, stop_index):
            self.set_consuming_row_and_index(mesh_index, row,
                                             mesh_index_in_row)
            mesh_index_in_row += 1

    def get_consuming_row_and_index(self, mesh_index):
        self._check_consuming_mesh_index(mesh_index)
        return self._mapping_to_row.get(mesh_index)

    def _check_consuming_mesh_index(self, mesh_index):
        if not self.is_consuming_mesh_index(mesh_index):
            message = "I only have {} produced meshes "\
                      "but you try to access mesh {}.".format(
                              self.number_of_produced_meshes,
                              mesh_index
                          )
            raise IndexError(message)

    def is_consuming_mesh_index(self, mesh_index):
        return mesh_index >= 0 and mesh_index < self.number_of_produced_meshes

    def set_consuming_row_and_index(self, mesh_index, row,
                                    mesh_index_in_row):
        if mesh_index in self._mapping_to_row:
            self.remove_consuming_row_and_index(mesh_index)
        self._mapping_to_row[mesh_index] = (row, mesh_index_in_row)
        row._set_producing_row_and_index(mesh_index_in_row, self, mesh_index)

    def remove_consuming_row_and_index(self, mesh_index):
        row, mesh_index_in_row = self._mapping_to_row[mesh_index]
        row._remove_producing_row_and_index(mesh_index_in_row,
                                            self, mesh_index)
        del self._mapping_to_row[mesh_index]

    def _set_producing_row_and_index(self, mesh_index, row, mesh_index_in_row):
        if mesh_index in self._mapping_from_row:
            self.remove_producing_row_and_index(mesh_index)
        self._mapping_from_row[mesh_index] = (row, mesh_index_in_row)

    def _remove_producing_row_and_index(self, mesh_index, row,
                                        mesh_index_in_row):
        expected_row, expected_index = self._mapping_from_row[mesh_index]
        assert expected_row == row, CONISTENCY_MESSAGE
        assert expected_index == mesh_index_in_row, CONISTENCY_MESSAGE
        del self._mapping_from_row[mesh_index]

    def remove_producing_row_and_index(self, mesh_index):
        row, mesh_index_in_row = self._mapping_from_row[mesh_index]
        expected_row, expected_mesh_index = row.get_consuming_row_and_index(
                                                           mesh_index_in_row
                                                       )
        assert expected_row == self, CONISTENCY_MESSAGE
        assert expected_mesh_index == mesh_index, CONISTENCY_MESSAGE
        row.remove_consuming_row_and_index(mesh_index_in_row)

    def get_producing_row_and_index(self, mesh_index):
        if mesh_index < 0 or mesh_index >= self.number_of_consumed_meshes:
            message = "I only have {} consumed meshes "\
                      "but you try to access mesh {}.".format(
                              self.number_of_consumed_meshes,
                              mesh_index
                          )
            raise IndexError(message)
        return self._mapping_from_row.get(mesh_index)

    @property
    def produced_meshes(self):
        return list(chain(*(instruction.produced_meshes
                          for instruction in self.instructions)))

    @property
    def consumed_meshes(self):
        return list(chain(*(instruction.consumed_meshes
                          for instruction in self.instructions)))

    def get_instruction_at_cosuming_mesh_index(self, mesh_index):
        self._check_consuming_mesh_index(mesh_index)
        for instruction in self.instructions:
            if mesh_index < instruction.number_of_consumed_meshes:
                return instruction
        assert False, "Passing all instructions should never happen."

    def __repr__(self):
        return "<{} {}>".format(self.__class__.__qualname__, self.id)
        
    def __lt__(self, other):
        return self.id < other.id

__all__ = ["Row"]
