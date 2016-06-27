from abc import ABCMeta, abstractmethod


class Mesh(metaclass=ABCMeta):

    """A mesh that is either consumed or produced by an instruction.

    .. code:: python

        assert mesh.is_produced() or mesh.is_consumed()

    Since this is an abstract base class you will only get instances of
    :class:`ProducedMesh <knittingpattern.Mesh.ProducedMesh>` and
    :class:`ConsumedMesh <knittingpattern.Mesh.ConsumedMesh>`.

    """

    @abstractmethod
    def _producing_instruction_and_index(self):
        """Replace this method."""

    @abstractmethod
    def _producing_row_and_index(self):
        """Replace this method."""

    @abstractmethod
    def _consuming_instruction_and_index(self):
        """Replace this method."""

    @abstractmethod
    def _consuming_row_and_index(self):
        """Replace this method."""

    @abstractmethod
    def _is_produced(self):
        """Replace this method."""

    @abstractmethod
    def _is_consumed(self):
        """Replace this method."""

    def is_produced(self):
        """Whether the mesh has an instruction that produces it.

        :return: whether the mesh is produced by an instruction
        :rtype: bool

        If you get this mesh from
        :attr:`knittingpattern.Instruction.InstructionInRow.produced_meshes` or
        :attr:`knittingpattern.Row.Row.produced_meshes`,
        this should be :obj:`True`.

        .. warning:: Before you use any methods on how the mesh is produced,
          you should check with ``mesh.is_produced()``.
        """
        return self._is_produced()

    def is_consumed(self):
        """Whether the mesh has an instruction that consumed it.

        :return: whether the mesh is consumed by an instruction
        :rtype: bool

        If you get this mesh from
        :attr:`knittingpattern.Instruction.InstructionInRow.consumed_meshes` or
        :attr:`knittingpattern.Row.Row.consumed_meshes`,
        this should be :obj:`True`.

        .. warning:: Before you use any methods on how the mesh is consumed,
          you should check with ``mesh.is_consumed()``.
        """
        return self._is_consumed()

    @property
    def index_in_producing_instruction(self):
        """Index in instruction as a produced mesh.

        :return: the index of the mesh in the list of meshes that
          :attr:`producing_instruction` produces
        :rtype: int

        .. code:: python

            instruction = mesh.producing_instruction
            index = mesh.index_in_producing_instruction
            assert instruction.produced_meshes[index] == mesh

        .. seealso:: :attr:`producing_instruction`,
          :attr:`index_in_consuming_instruction`

        .. warning:: Check with :meth:`is_produced` before!
        """
        return self._producing_instruction_and_index()[1]

    @property
    def producing_instruction(self):
        """Instruction which produces this mesh.

        :return: the instruction that produces this mesh
        :rtype: knittingpattern.Instruction.InstructionInRow

        .. seealso:: :attr:`index_in_producing_instruction`,
          :attr:`producing_row`, :attr:`consuming_row`

        .. warning:: Check with :meth:`is_produced` before!
        """
        return self._producing_instruction_and_index()[0]

    @property
    def producing_row(self):
        """Row which produces this mesh.

        :return: the row of the instruction that produces this mesh
        :rtype: knittingpattern.Row.Row

        .. seealso:: :attr:`index_in_producing_row`,
          :attr:`producing_instruction`, :attr:`consuming_row`

        .. warning:: Check with :meth:`is_produced` before!
        """
        return self._producing_row_and_index()[0]

    @property
    def index_in_producing_row(self):
        """Index in row as produced mesh.

        :return: the index of the mesh in the :attr:`producing_row`
        :rtype: int

        .. code:: python

            row = mesh.producing_row
            index = mesh.index_in_producing_row
            assert row[index] == mesh

        .. seealso:: :attr:`producing_row`, :attr:`index_in_consuming_row`

        .. warning:: Check with :meth:`is_produced` before!
        """
        return self._producing_row_and_index()[1]

    @property
    def index_in_consuming_row(self):
        """Index in row as consumed mesh.

        :return: the index of the mesh in the list of meshes that
          :attr:`consuming_row` consumes
        :rtype: int

        .. code:: python

            row = mesh.consuming_row
            index = mesh.index_in_consuming_row
            assert row.consumed_meshes[index] == mesh

        .. seealso:: :attr:`consuming_row`, :attr:`index_in_producing_row`

        .. warning:: Check with :meth:`is_consumed` before!
        """
        return self._consuming_row_and_index()[1]

    @property
    def consuming_row(self):
        """Row which consumes this mesh.

        :return: the row that consumes this mesh
        :rtype: knittingpattern.Row.Row

        .. seealso:: :attr:`index_in_consuming_row`,
          :attr:`consuming_instruction`, :attr:`producing_row`

        .. warning:: Check with :meth:`is_consumed` before!
        """
        return self._consuming_row_and_index()[0]

    @property
    def consuming_instruction(self):
        """Instruction which consumes this mesh.

        :return: the instruction that consumes this mesh
        :rtype: knittingpattern.Instruction.InstructionInRow

        .. seealso:: :attr:`index_in_consuming_instruction`,
          :attr:`consuming_row`, :attr:`producing_instruction`

        .. warning:: Check with :meth:`is_consumed` before!
        """
        return self._consuming_instruction_and_index()[0]

    @property
    def index_in_consuming_instruction(self):
        """Index in instruction as consumed mesh.

        :return: the index of the mesh in the list of meshes that
          :attr:`consuming_instruction` consumes
        :rtype: int

        .. code:: python

            instruction = mesh.consuming_instruction
            index = mesh.index_in_consuming_instruction
            assert instruction.consumed_meshes[index] == mesh

        .. seealso:: :attr:`consuming_instruction`,
          :attr:`index_in_consuming_instruction`

        .. warning:: Check with :meth:`is_consumed` before!
        """
        return self._consuming_instruction_and_index()[1]

    def is_knit(self):
        """Whether the mesh is produced by a knit instruction.

        :return: whether the mesh is knit by an instruction
        :rtype: bool

        .. seealso:: :attr:`producing_instruction`
        """
        return self._producing_instruction_and_index()[0].does_knit()

    def __repr__(self):
        """This mesh as string.

        :return: the string representation of this mesh.
        :rtype: str

        This is useful for :func:`print` and class:`str`
        """
        if self._is_consumed():
            instruction, _ = self._consuming_instruction_and_index()
            row, row_index = self._consuming_row_and_index()
            consume_string = " for {} in {}[{}]".format(
                    instruction,
                    row,
                    row_index
                )
        else:
            consume_string = ""
        if self._is_produced():
            instruction, _ = self._producing_instruction_and_index()
            row, row_index = self._producing_row_and_index()
            produce_string = " by {} in {}[{}]".format(
                    instruction,
                    row,
                    row_index
                )
        else:
            produce_string = ""
        return "<{}{}{}>".format(
                self.__class__.__name__, produce_string, consume_string
            )


class ProducedMesh(Mesh):
    """A :class:`~knittingpattern.Mesh.Mesh` that has a producing instruction
    """

    def __init__(self, producing_instruction,
                 index_in_producing_instruction):
        """
        :param producing_instruction: the
          :class:`instruction <knittingpattern.Instruction.InstructionInRow>`
          that produces the mesh
        :param int index_in_producing_instruction: the index of the mesh
          in the list of meshes that :attr:`producing_instruction`
          produces

        .. note:: There should be no necessity to create instances of this
          directly. You should be able to use
          ``instruction.produced_meshes`` or ``instruction.consumed_meshes``
          to access the :class:`meshes <knittingpattern.Mesh.Mesh>`.

        """
        self.__producing_instruction_and_index = (
                producing_instruction,
                index_in_producing_instruction
            )

    def _producing_instruction_and_index(self):
        return self.__producing_instruction_and_index

    def _producing_row_and_index(self):
        instruction, index = self.__producing_instruction_and_index
        producing_row = instruction.row
        return (producing_row,
                index + instruction.index_of_first_produced_mesh_in_row)

    def _consuming_instruction_and_index(self):
        row_and_index = self._consuming_row_and_index()
        assert row_and_index is not None, "Use is_consumed() before."
        consuming_row, index = row_and_index
        return consuming_row._get_instruction_and_index_at_consumed_mesh_index(
                   index
               )

    def __consuming_row_and_index_or_None(self):
        producing_row, index = self._producing_row_and_index()
        return producing_row._get_consuming_row_and_index(index)

    def _consuming_row_and_index(self):
        result = self.__consuming_row_and_index_or_None()
        assert result is not None, "use is_consumed() before"
        return result

    def _is_produced(self):
        return True

    def _is_consumed(self):
        return self.__consuming_row_and_index_or_None() is not None


class ConsumedMesh(Mesh):
    """A mesh that is only consumed by an instruction"""

    def __init__(self, consuming_instruction,
                 index_in_consuming_instruction):
        """
        :param consuming_instruction: the
          :class:`instruction <knittingpattern.Instruction.InstructionInRow>`
          that consumes the mesh
        :param int index_in_consuming_instruction: the index of the mesh
          in the list of meshes that :attr:`consuming_instruction`
          consumes

        .. note:: There should be no necessity to create instances of this
          directly. You should be able to use
          ``instruction.produced_meshes`` or ``instruction.consumed_meshes``
          to access the :class:`meshes <knittingpattern.Mesh.Mesh>`.

        """
        self.__consuming_instruction_and_index = (
                consuming_instruction,
                index_in_consuming_instruction
            )

    def _producing_instruction_and_index(self):
        assert False, "use is_produced()"
    _producing_row_and_index = _producing_instruction_and_index

    def _consuming_instruction_and_index(self):
        return self.__consuming_instruction_and_index

    def _consuming_row_and_index(self):
        instruction, index = self.__consuming_instruction_and_index
        consuming_row = instruction.row
        return (
            consuming_row, index +
            instruction.index_of_first_consumed_mesh_in_row)

    def _is_produced(self):
        return False

    def _is_consumed(self):
        return True


__all__ = ["Mesh", "ProducedMesh", "ConsumedMesh"]
