"""This module contains the rows of instructions of knitting patterns.

The :class:`rows <Row>` are part of :class:`knitting patterns
<knittingpattern.KnittingPattern.KnittingPattern>`.
They contain :class:`instructions
<knittingpattern.Instruction.InstructionInRow>` and can be connected to other
rows.
"""
from .Prototype import Prototype
from itertools import chain
from. ObservableList import ObservableList

COLOR = "color"  #: the color of the row

#: an error message
CONISTENCY_MESSAGE = "The data structure must be consistent."


class Row(Prototype):

    """This class contains the functionality for rows.

    This class is used by :class:`knitting patterns
    <knittingpattern.KnittingPattern.KnittingPattern>`.
    """

    def __init__(self, row_id, values, parser):
        """Create a new row.

        :param row_id: an identifier for the row
        :param values: the values from the specification
        :param list inheriting_from: a list of specifications to inherit values
          from, see :class:`knittingpattern.Prototype.Prototype`

        .. note:: Seldomly, you need to create this row on your own. You can
          load it with the :mod:`knittingpattern` or the
          :class:`knittingpattern.Parser.Parser`.
        """
        super().__init__(values)
        self._id = row_id
        self._instructions = ObservableList()
        self._instructions.register_observer(self._instructions_changed)
        self._parser = parser

    def _instructions_changed(self, change):
        """Call when there is a change in the instructions."""
        if change.adds():
            for index, instruction in change.items():
                if isinstance(instruction, dict):
                    in_row = self._parser.instruction_in_row(self, instruction)
                    self.instructions[index] = in_row
                else:
                    instruction.transfer_to_row(self)

    @property
    def id(self):
        """The id of the row.

        :return: the id of the row
        """
        return self._id

    @property
    def instructions(self):
        """The instructions in this row.

        :return: a collection of :class:`instructions inside the row
          <knittingpattern.Instruction.InstructionInRow>`
          e.g. a :class:`knittingpattern.IdCollection.IdCollection`
        """
        return self._instructions

    @property
    def number_of_produced_meshes(self):
        """The number of meshes that this row produces.

        :return: the number of meshes that this row produces
        :rtype: int

        .. seealso::
          :meth:`Instruction.number_of_produced_meshes()
          <knittingpattern.Instruction.Instruction.number_of_produced_meshes>`,
          :meth:`number_of_consumed_meshes`
        """
        return sum(instruction.number_of_produced_meshes
                   for instruction in self.instructions)

    @property
    def number_of_consumed_meshes(self):
        """The number of meshes that this row consumes.

        :return: the number of meshes that this row consumes
        :rtype: int

        .. seealso::
          :meth:`Instruction.number_of_consumed_meshes()
          <knittingpattern.Instruction.Instruction.number_of_consumed_meshes>`,
          :meth:`number_of_produced_meshes`
        """
        return sum(instruction.number_of_consumed_meshes
                   for instruction in self.instructions)

    @property
    def produced_meshes(self):
        """The meshes that this row produces with its instructions.

        :return: a collection of :class:`meshes <knittingpattern.Mesh.Mesh>`
          that this instruction produces

        """
        return list(chain(*(instruction.produced_meshes
                          for instruction in self.instructions)))

    @property
    def consumed_meshes(self):
        """Same as :attr:`produced_meshes` but for consumed meshes."""
        return list(chain(*(instruction.consumed_meshes
                          for instruction in self.instructions)))

    def __repr__(self):
        """The string representation of this row.

        :return: a string representation of this row
        :rtype: str
        """
        return "<{} {}>".format(self.__class__.__qualname__, self.id)

    @property
    def color(self):
        """The color of the row.

        :return: the color of the row as specified or :obj:`None`
        """
        return self.get(COLOR)

    @property
    def last_produced_mesh(self):
        """The last produced mesh.

        :return: the last produced mesh
        :rtype: knittingpattern.Mesh.Mesh
        :raises IndexError: if no mesh is produced

        .. seealso:: :attr:`number_of_produced_meshes`
        """
        for instruction in reversed(self.instructions):
            if instruction.produces_meshes():
                return instruction.last_produced_mesh
        raise IndexError("{} produces no meshes".format(self))

    @property
    def last_consumed_mesh(self):
        """The last consumed mesh.

        :return: the last consumed mesh
        :rtype: knittingpattern.Mesh.Mesh
        :raises IndexError: if no mesh is consumed

        .. seealso:: :attr:`number_of_consumed_meshes`
        """
        for instruction in reversed(self.instructions):
            if instruction.consumes_meshes():
                return instruction.last_consumed_mesh
        raise IndexError("{} consumes no meshes".format(self))

    @property
    def first_produced_mesh(self):
        """The first produced mesh.

        :return: the first produced mesh
        :rtype: knittingpattern.Mesh.Mesh
        :raises IndexError: if no mesh is produced

        .. seealso:: :attr:`number_of_produced_meshes`
        """
        for instruction in self.instructions:
            if instruction.produces_meshes():
                return instruction.first_produced_mesh
        raise IndexError("{} produces no meshes".format(self))

    @property
    def first_consumed_mesh(self):
        """The first consumed mesh.

        :return: the first consumed mesh
        :rtype: knittingpattern.Mesh.Mesh
        :raises IndexError: if no mesh is consumed

        .. seealso:: :attr:`number_of_consumed_meshes`
        """
        for instruction in self.instructions:
            if instruction.consumes_meshes():
                return instruction.first_consumed_mesh
        raise IndexError("{} consumes no meshes".format(self))

    @property
    def rows_before(self):
        """The rows that produce meshes for this row.

        :rtype: list
        :return: a list of rows that produce meshes for this row. Each row
          occurs only once. They are sorted by the first occurence in the
          instructions.
        """
        rows_before = []
        for mesh in self.consumed_meshes:
            if mesh.is_produced():
                row = mesh.producing_row
                if rows_before not in rows_before:
                    rows_before.append(row)
        return rows_before

    @property
    def rows_after(self):
        """The rows that consume meshes from this row.

        :rtype: list
        :return: a list of rows that consume meshes from this row. Each row
          occurs only once. They are sorted by the first occurence in the
          instructions.
        """
        rows_after = []
        for mesh in self.produced_meshes:
            if mesh.is_consumed():
                row = mesh.consuming_row
                if rows_after not in rows_after:
                    rows_after.append(row)
        return rows_after

__all__ = ["Row", "COLOR"]
