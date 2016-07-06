"""Knitting patterns consist of instructions.

The :class:`instructions <Instruction>`. that are used in the
:class:`knitting patterns <KnittingPattern>` can be foudn in this module.
They have certain attributes in common.

"""
from .Prototype import Prototype
from .Mesh import ProducedMesh, ConsumedMesh
from .convert.color import convert_color_to_rrggbb


# pattern specification

ID = "id"  #: the id key in the specification

TYPE = "type"  #: the type key in the specification

KNIT_TYPE = "knit"  #: the type of the knit instruction

PURL_TYPE = "purl"  #: the type of the purl instruction

#: the type of the instruction without a specified type
DEFAULT_TYPE = KNIT_TYPE

COLOR = "color"  #: the color key in the specification

DESCRIPTION = "description"  #: the description in the specification

#: the key for the number of meshes that a instruction consumes
NUMBER_OF_CONSUMED_MESHES = "number of consumed meshes"

#: the default number of meshes that a instruction consumes
DEFAULT_NUMBER_OF_CONSUMED_MESHES = 1

#: the key for the number of meshes that a instruction produces
NUMBER_OF_PRODUCED_MESHES = "number of produced meshes"

#: the default number of meshes that a instruction produces
DEFAULT_NUMBER_OF_PRODUCED_MESHES = 1

#: The default z-index, see :func:`get_z`.
DEFAULT_Z = 0

#: Instructions have a default specification. In this specification the key
#: in :data:`RENDER` points to configuration for rendering.
RENDER = "render"

#: The key to look for the z-index inside the :data:`render` specification.
#: .. seealso:: :func:`get_z`, :data:`DEFAULT_Z`
RENDER_Z = "z"

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
        """The id of the instruction.

        :return: the :data:`id <ID>` of the instruction or
          :obj:`None` if none is specified.
        """
        return self.get(ID)

    @property
    def type(self):
        """The type of the instruction.

        :return: the :data:`type <TYPE>` of the instruction or
          :data:`DEFAULT_TYPE` if none is specified.
        :rtype: str

        The type should be a string.
        Depending on the type, the instruction can receive additional
        attributes.

        .. seealso:: :mod:`knittingpattern.InstructionLibrary`
        """
        return self.get(TYPE, DEFAULT_TYPE)

    @property
    def color(self):
        """The color of the instruction.

        :return: the :data:`color <COLOR>` of the instruction or
          :obj:`None` if none is specified.
        """
        return self.get(COLOR)

    @property
    def description(self):
        """The description of the instruction.

        :return: the :data:`description <DESCRIPTION>` of the instruction or
          :obj:`None` if none is specified.
        """
        return self.get(DESCRIPTION)

    @property
    def number_of_consumed_meshes(self):
        """The number of meshes that this inctrucion consumes.

        :return: the :data:`number of consumed meshes
          <NUMBER_OF_CONSUMED_MESHES>` of the instruction or
          :data:`DEFAULT_NUMBER_OF_CONSUMED_MESHES` if none is specified.
        """
        return self.get(NUMBER_OF_CONSUMED_MESHES,
                        DEFAULT_NUMBER_OF_CONSUMED_MESHES)

    @property
    def number_of_produced_meshes(self):
        """The number of meshes that this instruction produces.

        :return: the :data:`number of produced meshes
          <NUMBER_OF_PRODUCED_MESHES>` of the instruction or
          :data:`DEFAULT_NUMBER_OF_PRODUCED_MESHES` if none is specified.
        """
        return self.get(NUMBER_OF_PRODUCED_MESHES,
                        DEFAULT_NUMBER_OF_PRODUCED_MESHES)

    def has_color(self):
        """Whether this instruction has a color.

        :return: whether a :data:`color <COLOR>` is specified
        :rtype: bool
        """
        return self.color is not None

    def does_knit(self):
        """Whether this instruction is a knit instruction.

        :return: whether this instruction is a knit instruction
        :rtype: bool
        """
        return self.type == KNIT_TYPE

    def does_purl(self):
        """Whether this instruction is a purl instruction.

        :return: whether this instruction is a purl instruction
        :rtype: bool
        """
        return self.type == PURL_TYPE

    def produces_meshes(self):
        """Whether this instcution produces meshes.

        :return: whether this instruction produces any meshes
        :rtype: bool

        .. seealso:: :attr:`number_of_produced_meshes`
        """
        return self.number_of_produced_meshes != 0

    def consumes_meshes(self):
        """Whether this instruction consumes meshes.

        :return: whether this instruction consumes any meshes
        :rtype: bool

        .. seealso:: :attr:`number_of_consumed_meshes`
        """
        return self.number_of_consumed_meshes != 0

    @property
    def render_z(self):
        """The z-index of the instruction when rendered.

        :return: the z-index of the instruction. Instructions with a higher
          z-index are displayed in front of instructions with lower z-index.
        :rtype: float
        """
        return self.get(RENDER, {}).get(RENDER_Z, DEFAULT_Z)

    @property
    def hex_color(self):
        """The color in "#RRGGBB" format.

        :return: the :attr:`color` in "#RRGGBB" format or none if no color is
          given
        """
        if self.has_color():
            return convert_color_to_rrggbb(self.color)
        return None


class InstructionInRow(Instruction):

    """Instructions can be placed in rows.

    Then, they have additional attributes and properties.
    """

    def __init__(self, row, spec):
        """Create a new instruction in a row with a specification.

        :param knittingpattern.Row.Row row: the row the instruction is placed
          in
        :param spec: specification of the instruction
        """
        super().__init__(spec)
        self._row = row
        self._produced_meshes = [
                self._new_produced_mesh(self, index)
                for index in range(self.number_of_produced_meshes)
            ]
        self._consumed_meshes = [
                self._new_consumed_mesh(self, index)
                for index in range(self.number_of_consumed_meshes)
            ]
        self._cached_index_in_row = None

    def transfer_to_row(self, new_row):
        """Transfer this instruction to a new row.

        :param knittingpattern.Row.Row new_row: the new row the instruction is
          in.
        """
        if new_row != self._row:
            index = self.get_index_in_row()
            if index is not None:
                self._row.instructions.pop(index)
            self._row = new_row

    @property
    def _new_produced_mesh(self):
        """:return: the class of the produced meshes."""
        return ProducedMesh

    @property
    def _new_consumed_mesh(self):
        """:return: the class of the consumed meshes."""
        return ConsumedMesh

    @property
    def row(self):
        """The row this instruction is in.

        :return: the row the instruction is placed in
        :rtype: knittingpattern.Row.Row
        """
        return self._row

    def is_in_row(self):
        """Whether the instruction can be found in its row.

        :return: whether the instruction is in its row
        :rtype: bool

        Use this to avoid raising and :class:`InstructionNotFoundInRow`.
        """
        return self.get_index_in_row() is not None

    def get_index_in_row(self):
        """Index of the instruction in the instructions of the row or None.

        :return: index in the :attr:`row`'s instructions or None, if the
          instruction is not in the row
        :rtype: int

        .. seealso:: :attr:`row_instructions`, :attr:`index_in_row`,
          :meth:`is_in_row`
        """
        expected_index = self._cached_index_in_row
        instructions = self._row.instructions
        if expected_index is not None and \
                0 <= expected_index < len(instructions) and \
                instructions[expected_index] is self:
            return expected_index
        for index, instruction_in_row in enumerate(instructions):
            if instruction_in_row is self:
                self._cached_index_in_row = index
                return index
        return None

    @property
    def index_in_row(self):
        """Index of the instruction in the instructions of the row.

        :return: index in the :attr:`row`'s instructions
        :rtype: int
        :raises knittingpattern.Instruction.InstructionNotFoundInRow:
          if the instruction is not found at the index

        .. code:: python

            index = instruction.index_in_row
            assert instruction.row.instructions[index] == instruction

        .. seealso:: :attr:`row_instructions`, :meth:`get_index_in_row`,
          :meth:`is_in_row`
        """
        index = self.get_index_in_row()
        if index is None:
            self._raise_not_found_error()
        return index

    @property
    def row_instructions(self):
        """Shortcut for ``instruction.row.instructions``.

        :return: the instructions of the :attr:`row` the instruction is in

        .. seealso:: :attr:`index_in_row`
        """
        return self.row.instructions

    @property
    def next_instruction_in_row(self):
        """The instruction after this one or None.

        :return: the instruction in :attr:`row_instructions` after this or
          :obj:`None` if this is the last
        :rtype: knittingpattern.Instruction.InstructionInRow

        This can be used to traverse the instructions.

        .. seealso:: :attr:`previous_instruction_in_row`
        """
        index = self.index_in_row + 1
        if index >= len(self.row_instructions):
            return None
        return self.row_instructions[index]

    @property
    def previous_instruction_in_row(self):
        """The instruction before this one or None.

        :return: the instruction in :attr:`row_instructions` before this or
          :obj:`None` if this is the first
        :rtype: knittingpattern.Instruction.InstructionInRow

        This can be used to traverse the instructions.

        .. seealso:: :attr:`next_instruction_in_row`
        """
        index = self.index_in_row - 1
        if index < 0:
            return None
        return self.row_instructions[index]

    @property
    def _instruction_not_found_message(self):
        """The message for the error.

        :return: an error message
        :rtype: str

        .. warning: private, do not use
        """
        return INSTRUCTION_NOT_FOUND_MESSAGE.format(
                   instruction=self, row=self.row
               )

    def _raise_not_found_error(self):
        """Raise an error that this instruction is in its row no longer.

        :raises knittingpattern.Instruction.InstructionNotFoundInRow:
          the instruction was not found

        .. warning: private, do not use
        """
        raise InstructionNotFoundInRow(self._instruction_not_found_message)

    @property
    def index_of_first_produced_mesh_in_row(self):
        """Index of the first produced mesh in the row that consumes it.

        :return: an index of the first produced mesh of rows produced meshes
        :rtype: int

        .. note:: If the instruction :meth:`produces meshes
          <Instruction.produces_meshes>`, this is the index of the first
          mesh the instruction produces in all the meshes of the row.
          If the instruction does not produce meshes, the index of the mesh is
          returned as if the instruction had produced a mesh.

        .. code::

            if instruction.produces_meshes():
                index = instruction.index_of_first_produced_mesh_in_row

        """
        index = 0
        for instruction in self.row_instructions:
            if instruction is self:
                break
            index += instruction.number_of_produced_meshes
        else:
            self._raise_not_found_error()
        return index

    @property
    def index_of_last_produced_mesh_in_row(self):
        """Index of the last mesh produced by this instruction in its row.

        :return: an index of the last produced mesh of rows produced meshes
        :rtype: int

        .. note:: If this instruction :meth:`produces meshes
          <Instruction.produces_meshes>`, this is the index of
          its last produces mesh in the row. However, if this instruction does
          not produce meshes, this is the index **before** the first mesh of
          the instruction if it produced meshes.

        .. seealso:: :attr:`index_of_first_produced_mesh_in_row`
        """
        index = self.index_of_first_produced_mesh_in_row
        return index + self.number_of_produced_meshes - 1

    @property
    def index_of_first_consumed_mesh_in_row(self):
        """The index of the first consumed mesh of this instruction in its row.

        Same as :attr:`index_of_first_produced_mesh_in_row`
        but for consumed meshes.
        """
        index = 0
        for instruction in self.row_instructions:
            if instruction is self:
                break
            index += instruction.number_of_consumed_meshes
        else:
            self._raise_not_found_error()
        return index

    @property
    def index_of_last_consumed_mesh_in_row(self):
        """The index of the last consumed mesh of this instruction in its row.

        Same as :attr:`index_of_last_produced_mesh_in_row`
        but for the last consumed mesh.
        """
        index = self.index_of_first_consumed_mesh_in_row
        return index + self.number_of_consumed_meshes - 1

    @property
    def produced_meshes(self):
        """The meshes produced by this instruction

        :return: a :class:`list` of :class:`meshes
          <knittingpattern.Mesh.Mesh>` that this instruction produces
        :rtype: list

        .. code:: python

            assert len(inst.produced_meshes) == inst.number_of_produced_meshes
            assert all(mesh.is_produced() for mesh in inst.produced_meshes)

        .. seealso:: :attr:`consumed_meshes`, :attr:`consuming_instructions`
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

        .. seealso:: :attr:`produced_meshes`, :attr:`producing_instructions`
        """
        return self._consumed_meshes

    def __repr__(self):
        """:obj:`repr(instruction) <repr>` used for :func:`print`.

        :return: the string representation of this object
        :rtype: str
        """
        index = self.get_index_in_row()
        if index is None:
            position = "not in {}".format(self.row)
        else:
            position = "in {} at {}".format(self.row, index)
        return "<{} {}\"{}\" {}>".format(
                self.__class__.__name__,
                ("{} ".format(self.id) if self.id is not None else ""),
                self.type,
                position
            )

    @property
    def producing_instructions(self):
        """Instructions that produce the meshes that this instruction consumes.

        :return: a list of :class:`instructions
          <knittingpattern.Instruction.InstructionInRow>`
        :rtype: list

        .. seealso:: :attr:`consuming_instructions`, :attr:`consumed_meshes`
        """
        return [(mesh.producing_instruction if mesh.is_produced() else None)
                for mesh in self.consumed_meshes]

    @property
    def consuming_instructions(self):
        """Instructions that consume the meshes that this instruction produces.

        :return: a list of :class:`instructions
          <knittingpattern.Instruction.InstructionInRow>`
        :rtype: list

        .. seealso:: :attr:`producing_instructions`, :attr:`produced_meshes`
        """
        return [(mesh.consuming_instruction if mesh.is_consumed() else None)
                for mesh in self.produced_meshes]

    @property
    def color(self):
        """The color of the instruction.

        :return: the :data:`color <COLOR>` of the instruction or
          :obj:`None` if none is specified.

        If no color is specified in the instruction, it is inherited form the
        row.
        """
        return self.get(COLOR, self.row.color)


class InstructionNotFoundInRow(ValueError):
    """This exception is raised if an instructin was not found in its row."""
    pass


__all__ = ["Instruction", "InstructionInRow", "InstructionNotFoundInRow",
           "ID", "TYPE", "KNIT_TYPE", "PURL_TYPE", "DEFAULT_TYPE", "COLOR",
           "NUMBER_OF_CONSUMED_MESHES", "DEFAULT_NUMBER_OF_CONSUMED_MESHES",
           "NUMBER_OF_PRODUCED_MESHES", "DEFAULT_NUMBER_OF_PRODUCED_MESHES",
           "RENDER_Z", "RENDER", "DEFAULT_Z"]
