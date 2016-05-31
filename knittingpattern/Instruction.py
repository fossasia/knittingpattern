from .Prototype import *

TYPE = "type"
KNIT_TYPE = "knit"
PURL_TYPE = "purl"
DEFAULT_TYPE = KNIT_TYPE
COLOR = "color"
NUMBER_OF_CONSUMED_MESHES = "number of consumed meshes"
DEFAULT_NUMBER_OF_CONSUMED_MESHES = 1
NUMBER_OF_PRODUCED_MESHES = "number of produced meshes"
DEFAULT_NUMBER_OF_PRODUCED_MESHES = 1


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

    from .Mesh import Mesh

    def __init__(self, row, spec):
        super().__init__(spec)
        self._row = row
        self._produced_meshes = [
                self.Mesh(self, index) 
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
        message = "Instruction {} was not found in row {}.".format(
                      self, self.row.id)
        raise InstructionNotFoundInRow(message)

    @property
    def produced_meshes(self):
        return self._produced_meshes

    @property
    def consumed_meshes(self):
        return []


class InstructionNotFoundInRow(ValueError):
    pass


__all__ = ["Instruction", "InstructionInRow", "InstructionNotFoundInRow"]
