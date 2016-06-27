"""This module contains the rows of instructions of knitting patterns.

The :class:`rows <Row>` are part of :class:`knitting patterns
<knittingpattern.KnittingPattern.KnittingPattern>`.
They contain :class:`instructions
<knittingpattern.Instruction.InstructionInRow>` and can be connected to other
rows.
"""
from .Prototype import Prototype
from itertools import chain

ID = "id"  #: the id of the row
#: an error message
CONISTENCY_MESSAGE = "The data structure must be consistent."


class Row(Prototype):

    """This class contains the functionality for rows.

    This class is used by :class:`knitting patterns
    <knittingpattern.KnittingPattern.KnittingPattern>`.
    """

    def __init__(self, row_id, values, inheriting_from=()):
        """Create a new row.

        :param row_id: an identifier for the row
        :param values: the values from the specification
        :param list inheriting_from: a list of specifications to inherit values
          from, see :class:`knittingpattern.Prototype.Prototype`

        .. note:: Seldomly, you need to create this row on your own. You can
          load it with the :mod:`knittingpattern` or the
          :class:`knittingpattern.Parser.Parser`.
        """
        super().__init__(values, inheriting_from)
        self._id = row_id
        self._values = values
        self._instructions = []
        self._mapping_to_row = {}
        self._mapping_from_row = {}

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

    def _produce_number_of_meshes_for_row(self, start_index,
                                          stop_index, row,
                                          row_start_index):
        """Set a connection between to rows."""
        mesh_index_in_row = row_start_index
        for mesh_index in range(start_index, stop_index):
            self._set_consuming_row_and_index(mesh_index, row,
                                              mesh_index_in_row)
            mesh_index_in_row += 1

    def _get_consuming_row_and_index_for_produced_mesh_at(self, mesh_index):
        """The mesh at mesh_index is produced in this row.

        :return: the row that consumes this mesh and
          this meshes index in to array of
          consumed meshes of the returned row.
        :rtype: tuple
        """
        self._check_is_produced_mesh_index(mesh_index)
        return self._mapping_to_row.get(mesh_index)

    _get_consuming_row_and_index = \
        _get_consuming_row_and_index_for_produced_mesh_at

    def _check_is_produced_mesh_index(self, mesh_index):
        """Check if the mesh index is correct.

        :raises IndexError: if the :paramref:`mesh_index` is out of bounds
        :param int mesh_index: the index of the mesh to check the index for
        """
        if not self._is_produced_mesh_index(mesh_index):
            message = "{} only has {} produced meshes "\
                      "but you try to access mesh at index {}.".format(
                              self,
                              self.number_of_produced_meshes,
                              mesh_index
                          )
            raise IndexError(message)

    def _check_is_consumed_mesh_index(self, mesh_index):
        """Check if the mesh index is correct.

        Same as :meth:`_check_is_produced_mesh_index` but for consumed
        meshes.
        """
        if not self._is_consumed_mesh_index(mesh_index):
            message = "{} only has {} consumed meshes "\
                      "but you try to access mesh at index {}.".format(
                              self,
                              self.number_of_consumed_meshes,
                              mesh_index
                          )
            raise IndexError(message)

    def _is_produced_mesh_index(self, mesh_index):
        """Returns if the mesh index is correct.

        :return: whether the mesh_index is in bounds
        :rtype: bool

        .. seealso:: :meth:`_check_is_produced_mesh_index`,
          :meth:`_is_consumed_mesh_index`
        """
        return mesh_index >= 0 and mesh_index < self.number_of_produced_meshes

    def _is_consumed_mesh_index(self, mesh_index):
        """Returns if the mesh index is correct.

        Same as :meth:`_is_produced_mesh_index` but for consumed
        meshes.

        .. seealso:: :meth:`_check_is_consumed_mesh_index`,
          :meth:`_is_produced_mesh_index`
        """
        return mesh_index >= 0 and mesh_index < self.number_of_consumed_meshes

    def _set_consuming_row_and_index(self, mesh_index, row,
                                     mesh_index_in_row):
        """Create a connection between to rows.

        :param int mesh_index: is the index of the mesh in this row
        :param Row row: is the other row to connect to
        :param int mesh_index_in_row: is the mesh index in the :paramref:`row`
        """
        if mesh_index in self._mapping_to_row:
            self._remove_consuming_row_and_index(mesh_index)
        self._mapping_to_row[mesh_index] = (row, mesh_index_in_row)
        row._set_producing_row_and_index(mesh_index_in_row, self, mesh_index)

    def _remove_consuming_row_and_index(self, mesh_index):
        """Reverse :meth:`_set_consuming_row_and_index`."""
        row, mesh_index_in_row = self._mapping_to_row[mesh_index]
        row.__remove_producing_row_and_index_callback(mesh_index_in_row,
                                                      self, mesh_index)
        del self._mapping_to_row[mesh_index]

    def _set_producing_row_and_index(self, mesh_index, row, mesh_index_in_row):
        """Create a connection between to rows.

        :param int mesh_index: is the index of the mesh in this row
        :param Row row: is the other row to connect to
        :param int mesh_index_in_row: is the mesh index in the :paramref:`row`
        """
        if mesh_index in self._mapping_from_row:
            self._remove_producing_row_and_index(mesh_index)
        self._mapping_from_row[mesh_index] = (row, mesh_index_in_row)

    def __remove_producing_row_and_index_callback(self, mesh_index, row,
                                                  mesh_index_in_row):
        """Do not use.

        called by :meth:`_remove_producing_row_and_index` after all the
        checks have passed to reverse a call of
        :meth:`_set_producing_row_and_index`
        """
        expected_row, expected_index = self._mapping_from_row[mesh_index]
        assert expected_row == row, CONISTENCY_MESSAGE
        assert expected_index == mesh_index_in_row, CONISTENCY_MESSAGE
        del self._mapping_from_row[mesh_index]

    def _remove_producing_row_and_index(self, mesh_index):
        """Reverse the effect of :meth:`_set_producing_row_and_index`."""
        row, mesh_index_in_row = self._mapping_from_row[mesh_index]
        expected_row, expected_mesh_index = row._get_consuming_row_and_index(
                                                           mesh_index_in_row
                                                       )
        assert expected_row == self, CONISTENCY_MESSAGE
        assert expected_mesh_index == mesh_index, CONISTENCY_MESSAGE
        row._remove_consuming_row_and_index(mesh_index_in_row)

    def _get_producing_row_and_index(self, mesh_index):
        """:return: the producing row and index of the consumed mesh"""
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

    def _get_instruction_and_index_at_consumed_mesh_index(self, mesh_index):
        """Get a connection to an other row.

        :return: the instruction and its index in that instruction of
          the mesh that is consumed by this row at mesh_index
        """
        self._check_is_consumed_mesh_index(mesh_index)
        for inst in self.instructions:
            if not inst.consumes_meshes():
                continue
            mini = inst.index_of_first_consumed_mesh_in_row
            maxi = inst.index_of_last_consumed_mesh_in_row
            if mini <= mesh_index <= maxi:
                return inst, mesh_index - mini
        assert False, "Passing all instructions should never happen."

    def __repr__(self):
        """The string representation of this row.

        :return: a string representation of this row
        """
        return "<{} {}>".format(self.__class__.__qualname__, self.id)

    def __lt__(self, other):
        """``row < other_row``

        :return: whether the own id is lowre that the other id
        :rtype: bool
        """
        return self.id < other.id

__all__ = ["Row"]
