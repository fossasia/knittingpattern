""":class:`knitting patterns <KnittingPattern>` consist of
:class:`instructions <Instruction>`.

These instructions have certain attributes in common.
In this module you can find the functinality of these instructions.

"""
from .Prototype import Prototype

# pattern specification

ID = "id"  #: the id key in the specification
TYPE = "type"  #: the type key in the specification
KNIT_TYPE = "knit"  #: the type of the knit instruction
PURL_TYPE = "purl"  #: the type of the purl instruction
#: the type of the instruction without a specified type
DEFAULT_TYPE = KNIT_TYPE
COLOR = "color"  #: the color key in the specification
#: the key for the number of meshes that a instruction consumes
NUMBER_OF_CONSUMED_MESHES = "number of consumed meshes"
#: the default number of meshes that a instruction consumes
DEFAULT_NUMBER_OF_CONSUMED_MESHES = 1
#: the key for the number of meshes that a instruction produces
NUMBER_OF_PRODUCED_MESHES = "number of produced meshes"
#: the default number of meshes that a instruction produces
DEFAULT_NUMBER_OF_PRODUCED_MESHES = 1

# error messages

INSTRUCTION_NOT_FOUND_MESSAGE = \
    "Instruction {instruction} was not found in row {row}."


class Instruction(Prototype):
    """Instructions specify what should be done during knitting.
    This class represents the basic interface for instructions.

    It is based on the
    :class:`Prototype <knittingpattern.Prototype.Prototype>`
    which allows creating instructions based on other instructions so
    they can inherit their attributes.

    You can create new instructions by passing a specification to them which
    can consist of a :class:`dictionary <dict>` or an other
    :class:`prototype <knittingpattern.Prototype.Prototype>`.
    For such specifications see the
    :mod:`InstructionLibrary <knittingpattern.InstructionLibrary>`.
    """

    @property
    def id(self):
        """
        :return: the :data:`id <ID>` of the instruction or
          :obj:`None` if none is specified.
        """
        return self.get(ID)

    @property
    def type(self):
        """
        :return: the :data:`type <TYPE>` of the instruction or
          :data:`DEFAULT_TYPE` if none is specified.
        """
        return self.get(TYPE, DEFAULT_TYPE)

    @property
    def color(self):
        """
        :return: the :data:`color <COLOR>` of the instruction or
          :obj:`None` if none is specified.
        """
        return self.get(COLOR, None)

    @property
    def number_of_consumed_meshes(self):
        """
        :return: the :data:`number of consumed meshes
          <NUMBER_OF_CONSUMED_MESHES>` of the instruction or
          :data:`DEFAULT_NUMBER_OF_CONSUMED_MESHES` if none is specified.
        """
        return self.get(NUMBER_OF_CONSUMED_MESHES,
                        DEFAULT_NUMBER_OF_CONSUMED_MESHES)

    @property
    def number_of_produced_meshes(self):
        """
        :return: the :data:`number of produced meshes
          <NUMBER_OF_PRODUCED_MESHES>` of the instruction or
          :data:`DEFAULT_NUMBER_OF_PRODUCED_MESHES` if none is specified.
        """
        return self.get(NUMBER_OF_PRODUCED_MESHES,
                        DEFAULT_NUMBER_OF_PRODUCED_MESHES)

    def has_color(self):
        """determines if a color is specified

        :return: whether a :data:`color <COLOR>` is specified
        :rtype: bool
        """
        return COLOR in self

    def does_knit(self):
        """
        :return: whether this instruction is a knit instruction
        :rtype: bool
        """
        return self.type == KNIT_TYPE

    def does_purl(self):
        """
        :return: whether this instruction is a purl instruction
        :rtype: bool
        """
        return self.type == PURL_TYPE

    def produces_meshes(self):
        """
        :return: whether this instruction produces any meshes
        :rtype: bool
        """
        return self.number_of_produced_meshes != 0

    def consumes_meshes(self):
        """
        :return: whether this instruction consumes any meshes
        :rtype: bool
        """
        return self.number_of_consumed_meshes != 0


class InstructionInRow(Instruction):
    """Instructions can be placed in rows.
    Then they have addisional attributes and properties.
    """

    #: The meshes consumed and produced by the instruction
    from .Mesh import ProducedMesh, ConsumedMesh

    def __init__(self, row, spec):
        """
        Create a new instruction in a :paramref:`row` with a :paramref:`spec`.

        :param knittingpattern.Row.Row row: the row the instruction is placed
          in
        :param spec: specification of the instruction
        """
        super().__init__(spec)
        self._row = row
        self._produced_meshes = [
                self.ProducedMesh(self, index)
                for index in range(self.number_of_produced_meshes)
            ]
        self._cached_index_in_row_instructions = None

    @property
    def row(self):
        """:return: the row the instruction is placed in
        :rtype: knittingpattern.Row.Row
        """
        return self._row

    @property
    def index_in_row_instructions(self):
        """
        :return: index in the :attr:`row`'s instructions
        :rtype: int
        :raises knittingpattern.Instruction.InstructionNotFoundInRow:
          if the instruction is not found at the index

        .. code:: python

            index = instruction.index_in_row_instructions
            assert instruction.row.instructions[index] == instruction

        .. seealso:: :meth:`row_instructions`
        """
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
        """shortcut for ``instruction.row.instructions``

        :return: the instructions of the :attr:`row` the instruction is in

        .. seealso:: :meth:`index_in_row_instructions`
        """
        return self.row.instructions

    @property
    def next_instruction_in_row(self):
        """
        :return: the instruction in :attr:`row_instructions` after this or
          :obj:`None` if this is the last
        :rtype: knittingpattern.Instruction.InstructionInRow

        This can be used to traverse the instructions.

        .. seealso:: :meth:`previous_instruction_in_row`
        """
        index = self.index_in_row_instructions + 1
        if index < 0:
            return None
        if index >= len(self.row_instructions):
            return None
        return self.row_instructions[index]

    @property
    def previous_instruction_in_row(self):
        """
        :return: the instruction in :attr:`row_instructions` before this or
          :obj:`None` if this is the first
        :rtype: knittingpattern.Instruction.InstructionInRow

        This can be used to traverse the instructions.

        .. seealso:: :meth:`next_instruction_in_row`
        """
        index = self.index_in_row_instructions - 1
        if index < 0:
            return None
        if index >= len(self.row_instructions):
            return None
        return self.row_instructions[index]

    @property
    def _instruction_not_found_message(self):
        """:return: an error message
        :rtype: str

        .. warning: private, do not use
        """
        return INSTRUCTION_NOT_FOUND_MESSAGE.format(
                   instruction=self, row=self.row
               )

    def _raise_not_found_error(self):
        """
        :raises knittingpattern.Instruction.InstructionNotFoundInRow:
          the instruction was not found

        .. warning: private, do not use
        """
        raise InstructionNotFoundInRow(self._instruction_not_found_message)

    @property
    def _index_of_first_produced_mesh_in_rows_produced_meshes(self):
        """
        :return: an index of the first produced mesh of rows produced meshes
        :rtype: int

        .. note::
          If you really need to use this, check if the instruction
          produces meshes before with
          :meth:`produces_meshes() <Instruction.produces_meshes>`

        .. code::

            if instruction.produces_meshes():
                index = instruction.index_of_fi...duced_meshes

        """
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
    def _index_of_last_produced_mesh_in_rows_produced_meshes(self):
        """
        Same as :meth:`_index_of_first_produced_mesh_in_rows_produced_meshes`
        but for the last mesh procduced.
        """
        assert self.produces_meshes()
        return self._index_of_first_produced_mesh_in_rows_produced_meshes + \
            self.number_of_produced_meshes - 1

    @property
    def _index_of_first_consumed_mesh_in_rows_consumed_meshes(self):
        """
        Same as :meth:`_index_of_first_produced_mesh_in_rows_produced_meshes`
        but for consumed meshes.
        """
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
    def _index_of_last_consumed_mesh_in_rows_consumed_meshes(self):
        """
        Same as :meth:`_index_of_first_consumed_mesh_in_rows_consumed_meshes`
        but for the last consumed mesh.
        """
        assert self.consumes_meshes()
        return self._index_of_first_consumed_mesh_in_rows_consumed_meshes + \
            self.number_of_consumed_meshes - 1

    @property
    def produced_meshes(self):
        """The meshes produced by this instruction

        :return: a :class:`list` of :class:`meshes
          <knittingpattern.Mesh.Mesh>` that this instruction produces
        :rtype: list

        .. code:: python

            assert len(inst.produced_meshes) == inst.number_of_produced_meshes
            assert all(mesh.is_produced() for mesh in inst.produced_meshes)

        .. seealso:: :meth:`consumed_meshes`, :meth:`consuming_instructions`
        """
        return self._produced_meshes

    @property
    def consumed_meshes(self):
        """The meshes consumed by this instruction

        :return: a :class:`list` of :class:`meshes
          <knittingpattern.Mesh.Mesh>` that this instruction consumes
        :rtype: list

        .. code:: python

            assert len(inst.consumed_meshes) == inst.number_of_consumed_meshes
            assert all(mesh.is_consumed() for mesh in inst.consumed_meshes)

        .. seealso:: :meth:`produced_meshes`, :meth:`producing_instructions`
        """
        return [
                self._consumed_meshes_at(index)
                for index in range(self.number_of_consumed_meshes)
            ]

    def _consumed_meshes_at(self, mesh_index):
        """
        :param int mesh_index: the index of the consumed mesh
        :return: a :class:`mesh <knittingpattern.Mesh.Mesh>` that is consumed
          at the :paramref:`mesh_index`
        :rtype: knittingpattern.Mesh.Mesh
        """
        consuming_row = self.row
        index_in_consuming_row = \
            self._index_of_first_consumed_mesh_in_rows_consumed_meshes + \
            mesh_index
        origin = consuming_row._get_producing_row_and_index(
                index_in_consuming_row
            )
        if origin is None:
            return self.ConsumedMesh(self, mesh_index)
        producing_row, mesh_index_in_producing_row = origin
        return producing_row.produced_meshes[mesh_index_in_producing_row]

    def _produced_meshes_at(self, mesh_index):
        """
        Same as :meth:`_consumed_meshes_at` but for consumed meshes
        """
        return self.produced_meshes[mesh_index]

    def __repr__(self):
        """ ``repr(instruction)`` used for :func:`print`

        :return: the string representation of this object
        :rtype: str
        """
        return "<{} {}\"{}\" in {} at {}>".format(
                self.__class__.__name__,
                ("{} ".format(self.id) if self.id is not None else ""),
                self.type,
                self.row,
                self.index_in_row_instructions
            )

    @property
    def producing_instructions(self):
        """Shortcut for all the instructions that produce the meshes that
        this instruction consumes.

        :return: a list of :class:`instructions
          <knittingpattern.Instruction.InstructionInRow>`
        :rtype: list

        .. seealso:: :meth:`consuming_instructions`, :meth:`consumed_meshes`
        """
        return [(mesh.producing_instruction if mesh.is_produced() else None)
                for mesh in self.consumed_meshes]

    @property
    def consuming_instructions(self):
        """
        Same as :attr:`consuming_instructions` but for consuming instructions

        .. seealso:: :meth:`producing_instructions`, :meth:`produced_meshes`
        """
        return [(mesh.consuming_instruction if mesh.is_consumed() else None)
                for mesh in self.produced_meshes]


class InstructionNotFoundInRow(ValueError):
    """This exception is raised if an instructin was not found in its row."""
    pass


__all__ = ["Instruction", "InstructionInRow", "InstructionNotFoundInRow",
           "ID", "TYPE", "KNIT_TYPE", "PURL_TYPE", "DEFAULT_TYPE", "COLOR",
           "NUMBER_OF_CONSUMED_MESHES", "DEFAULT_NUMBER_OF_CONSUMED_MESHES",
           "NUMBER_OF_PRODUCED_MESHES", "DEFAULT_NUMBER_OF_PRODUCED_MESHES"]
