from .Prototype import *

# pattern specification

TYPE = "type"
KNIT_TYPE = "knit"
PURL_TYPE = "purl"
DEFAULT_TYPE = KNIT_TYPE
COLOR = "color"
NUMBER_OF_CONSUMED_MESHES = "number of consumed meshes"
DEFAULT_NUMBER_OF_CONSUMED_MESHES = 1
NUMBER_OF_PRODUCED_MESHES = "number of produced meshes"
DEFAULT_NUMBER_OF_PRODUCED_MESHES = 1

# error messages

INSTRUCTION_NOT_FOUND_MESSAGE = "Instruction {instruction} was not found in row {row}."

class Instruction(Prototype):

    @property
    def type(self):
        return self.get(TYPE, DEFAULT_TYPE)

    @property
    def color(self):
        return self.get(COLOR, None)

    @property
    def number_of_consumed_meshes(self):
        return self.get(NUMBER_OF_CONSUMED_MESHES, DEFAULT_NUMBER_OF_CONSUMED_MESHES)

    @property
    def number_of_produced_meshes(self):
        return self.get(NUMBER_OF_PRODUCED_MESHES, DEFAULT_NUMBER_OF_PRODUCED_MESHES)

    def has_color(self):
        return self.color is not None

    def does_knit(self):
        return self.type == KNIT_TYPE

    def does_purl(self):
        return self.type == PURL_TYPE


class InstructionInRow(Instruction):

    from .Mesh import ProducedMesh, ConsumedMesh

    def __init__(self, row, spec):
        super().__init__(spec)
        self._row = row
        self._produced_meshes = [
                self.ProducedMesh(self, index)
                for index in range(self.number_of_produced_meshes)
            ]
        
    @property
    def row(self):
        return self._row

    @property
    def index_in_row_instructions(self):
        for index, instruction_in_row in enumerate(self.row.instructions):
            if instruction_in_row is self:
                return index
        self._raise_not_found_error()
    
    @property
    def _instruction_not_found_message(self):
        return INSTRUCTION_NOT_FOUND_MESSAGE.format(
                   instruction = self, row = self.row
               )
    
    def _raise_not_found_error(self):
        raise InstructionNotFoundInRow(self._instruction_not_found_message)
    
    @property
    def index_of_first_produced_mesh_in_rows_produced_meshes(self):
        index = 0
        for instruction in self.row.instructions:
            if instruction is self:
                break
            index += instruction.number_of_produced_meshes
        else:
            self._raise_not_found_error()
        return index
    
    @property
    def index_of_first_consumed_mesh_in_rows_consumed_meshes(self):
        index = 0
        for instruction in self.row.instructions:
            if instruction is self:
                break
            index += instruction.number_of_consumed_meshes
        else:
            self._raise_not_found_error()
        return index

    @property
    def produced_meshes(self):
        return self._produced_meshes

    @property
    def consumed_meshes(self):
        return [self._consumed_mesh(index)
                for index in range(self.number_of_consumed_meshes)]

    def _consumed_mesh(self, mesh_index_in_instruction):
        consuming_row= self.row
        index_in_consuming_row = self.index_of_first_consumed_mesh_in_rows_consumed_meshes + \
                                 mesh_index_in_instruction
        origin = consuming_row.get_producing_row_and_index(index_in_consuming_row)
        if origin is None:
            return self.ConsumedMesh(self, mesh_index_in_instruction)
        producing_row, mesh_index_in_producing_row = origin
        return producing_row.produced_meshes[mesh_index_in_producing_row]
        
    def __repr__(self):
        return "<{} \"{}\" in {} at {}>".format(
                self.__class__.__name__,
                self.type,
                self.row, 
                self.index_in_row_instructions
            )

class InstructionNotFoundInRow(ValueError):
    pass


__all__ = ["Instruction", "InstructionInRow", "InstructionNotFoundInRow"]
