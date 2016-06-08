from .Prototype import *

# pattern specification

ID = "id"
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

INSTRUCTION_NOT_FOUND_MESSAGE = \
    "Instruction {instruction} was not found in row {row}."


class Instruction(Prototype):

    @property
    def id(self):
        return self.get(ID)

    @property
    def type(self):
        return self.get(TYPE, DEFAULT_TYPE)

    @property
    def color(self):
        return self.get(COLOR, None)

    @property
    def number_of_consumed_meshes(self):
        return self.get(NUMBER_OF_CONSUMED_MESHES,
                        DEFAULT_NUMBER_OF_CONSUMED_MESHES)

    @property
    def number_of_produced_meshes(self):
        return self.get(NUMBER_OF_PRODUCED_MESHES,
                        DEFAULT_NUMBER_OF_PRODUCED_MESHES)

    def has_color(self):
        return self.color is not None

    def does_knit(self):
        return self.type == KNIT_TYPE

    def does_purl(self):
        return self.type == PURL_TYPE

    def produces_meshes(self):
        return self.number_of_produced_meshes != 0

    def consumes_meshes(self):
        return self.number_of_consumed_meshes != 0


class InstructionInRow(Instruction):

    from .Mesh import ProducedMesh, ConsumedMesh

    def __init__(self, row, spec):
        super().__init__(spec)
        self._row = row
        self._produced_meshes = [
                self.ProducedMesh(self, index)
                for index in range(self.number_of_produced_meshes)
            ]
        self._cached_index_in_row_instructions = None

    @property
    def row(self):
        return self._row

    @property
    def index_in_row_instructions(self):
        expected_index = self._cached_index_in_row_instructions
        instructions = self.row_instructions
        if expected_index is not None and \
                0 <= expected_index < len(instructions) and \
                instructions[expected_index] is self:
            return expected_index
        for index, instruction_in_row in enumerate(instructions):
            if instruction_in_row is self:
                self._cached_index_in_row_instructions = index
                return index
        self._raise_not_found_error()

    @property
    def row_instructions(self):
        return self.row.instructions

    @property
    def next_instruction_in_row(self):
        index = self.index_in_row_instructions + 1
        if index < 0:
            return None
        if index >= len(self.row_instructions):
            return None
        return self.row_instructions[index]

    @property
    def previous_instruction_in_row(self):
        index = self.index_in_row_instructions - 1
        if index < 0:
            return None
        if index >= len(self.row_instructions):
            return None
        return self.row_instructions[index]

    @property
    def _instruction_not_found_message(self):
        return INSTRUCTION_NOT_FOUND_MESSAGE.format(
                   instruction=self, row=self.row
               )

    def _raise_not_found_error(self):
        raise InstructionNotFoundInRow(self._instruction_not_found_message)

    @property
    def index_of_first_produced_mesh_in_rows_produced_meshes(self):
        assert self.produces_meshes()
        index = 0
        for instruction in self.row_instructions:
            if instruction is self:
                break
            index += instruction.number_of_produced_meshes
        else:
            self._raise_not_found_error()
        return index

    @property
    def index_of_last_produced_mesh_in_rows_produced_meshes(self):
        assert self.produces_meshes()
        return self.index_of_first_produced_mesh_in_rows_produced_meshes + \
            self.number_of_produced_meshes - 1

    @property
    def index_of_first_consumed_mesh_in_rows_consumed_meshes(self):
        assert self.consumes_meshes()
        index = 0
        for instruction in self.row_instructions:
            if instruction is self:
                break
            index += instruction.number_of_consumed_meshes
        else:
            self._raise_not_found_error()
        return index

    @property
    def index_of_last_consumed_mesh_in_rows_consumed_meshes(self):
        assert self.consumes_meshes()
        return self.index_of_first_consumed_mesh_in_rows_consumed_meshes + \
            self.number_of_consumed_meshes - 1

    @property
    def produced_meshes(self):
        return self._produced_meshes

    @property
    def consumed_meshes(self):
        return [
                self.consumed_meshes_at(index)
                for index in range(self.number_of_consumed_meshes)
            ]

    def consumed_meshes_at(self, mesh_index):
        consuming_row = self.row
        index_in_consuming_row = \
            self.index_of_first_consumed_mesh_in_rows_consumed_meshes + \
            mesh_index
        origin = consuming_row.get_producing_row_and_index(
                index_in_consuming_row
            )
        if origin is None:
            return self.ConsumedMesh(self, mesh_index)
        producing_row, mesh_index_in_producing_row = origin
        return producing_row.produced_meshes[mesh_index_in_producing_row]

    def produced_meshes_at(self, mesh_index):
        return self.produced_meshes[mesh_index]

    def __repr__(self):
        return "<{} {}\"{}\" in {} at {}>".format(
                self.__class__.__name__,
                ("{} ".format(self.id) if self.id is not None else ""),
                self.type,
                self.row,
                self.index_in_row_instructions
            )

    @property
    def producing_instructions(self):
        return [(mesh.producing_instruction if mesh.is_produced() else None)
                for mesh in self.consumed_meshes]

    @property
    def consuming_instructions(self):
        return [(mesh.consuming_instruction if mesh.is_consumed() else None)
                for mesh in self.produced_meshes]


class InstructionNotFoundInRow(ValueError):
    pass


__all__ = ["Instruction", "InstructionInRow", "InstructionNotFoundInRow"]
