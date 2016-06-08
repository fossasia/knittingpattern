

class ProducedMesh(object):

    def __init__(self, producing_instruction,
                 mesh_index_in_producing_instruction):
        self._producing_instruction = producing_instruction
        self._mesh_index_in_producing_instruction = \
            mesh_index_in_producing_instruction

    @property
    def mesh_index_in_producing_instruction(self):
        return self._mesh_index_in_producing_instruction

    @property
    def producing_instruction(self):
        return self._producing_instruction

    @property
    def producing_row(self):
        return self.producing_instruction.row

    def is_produced(self):
        return True

    def is_consumed(self):
        return self.consuming_row_and_index is not None

    @property
    def mesh_index_in_producing_row(self):
        instruction = self.producing_instruction
        i = instruction.index_of_first_produced_mesh_in_rows_produced_meshes
        return i + self.mesh_index_in_producing_instruction

    @property
    def mesh_index_in_consuming_row(self):
        return self.consuming_row_and_index[1]

    @property
    def consuming_row_and_index(self):
        return self.producing_row.get_consuming_row_and_index(
                       self.mesh_index_in_producing_row
                   )

    def is_knit(self):
        return self.producing_instruction.does_knit()

    @property
    def consuming_instruction(self):
        return self.consuming_instruction_and_index[0]

    @property
    def mesh_index_in_consuming_instruction(self):
        return self.consuming_instruction_and_index[1]

    @property
    def consuming_instruction_and_index(self):
        """Returns the instruction that consumes this mesh and
           the index of this mesh in this instruction."""
        row_and_index = self.consuming_row_and_index
        assert row_and_index is not None, "Use is_consumed() before."
        consuming_row, index = row_and_index
        return consuming_row.get_instruction_and_index_at_consumed_mesh_index(
                   index
               )

    @property
    def consuming_row(self):
        return self.consuming_row_and_index[0]

    def __repr__(self):
        return "<{} by {} at {} in {} at {}>".format(
                self.__class__.__name__,
                self.producing_instruction,
                self.mesh_index_in_producing_instruction,
                self.producing_row,
                self.mesh_index_in_producing_row
            )


class ConsumedMesh(object):

    def __init__(self, consuming_instruction,
                 mesh_index_in_consuming_instruction):
        self._consuming_instruction = consuming_instruction
        self._mesh_index_in_consuming_instruction = \
            mesh_index_in_consuming_instruction

    def is_produced(self):
        return False
