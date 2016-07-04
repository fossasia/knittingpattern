"""Instructions have  many attributes that do not need to be specified
in each :class:`knitting pattern set
<knittingpattern.KnittingpatternSet.KnittingpatternSet>`.

This module provides the fucntionality to load default values for instructions
from various locations.
"""
from .Instruction import TYPE
from .Loader import JSONLoader
from .Instruction import Instruction


class InstructionLibrary(object):
    """This library can be used to look up default specification of
    instructions.

    The specification is searched for by the type of the instruction.
    """

    @property
    def _loader_class(self):
        """:return: the class for loading the specifications with
          :attr:`load`
        """
        return JSONLoader

    @property
    def _instruction_class(self):
        """:return: the class for the specifications
        """
        return Instruction

    def __init__(self):
        """Create a new :class:`InstructionLibrary
        <knittingpattern.InstructionLibrary.InstructionLibrary>` without
        arguments.

        Use :attr:`load` to load specifications.
        """
        self._type_to_instruction = {}

    @property
    def load(self):
        """:return: a loader that can be used to load specifications
        :rtype: knittingpattern.Loader.JSONLoader

        A file to load is a list of instructions in JSON format.

        .. code:: json

            [
                {
                    "type" : "knit",
                    "another" : "attribute"
                },
                {
                    "type" : "purl"
                }
            ]

        """
        return self._loader_class(self._process_loaded_object)

    def _process_loaded_object(self, obj):
        """add the loaded instructions from :attr:`load`
        """
        for instruction in obj:
            self.add_instruction(instruction)
        return self

    def add_instruction(self, specification):
        """Add an instruction specification

        :param specification: a specification with a key
          :data:`knittingpattern.Instruction.TYPE`

        .. seealso:: :meth:`as_instruction`
        """
        instruction = self.as_instruction(specification)
        self._type_to_instruction[instruction.type] = instruction

    def as_instruction(self, specification):
        """Convert the specification into an instruction

        :param specification: a specification with a key
          :data:`knittingpattern.Instruction.TYPE`

        The instruction is not added.

        .. seealso:: :meth:`add_instruction`
        """
        instruction = self._instruction_class(specification)
        type_ = instruction.type
        if type_ in self._type_to_instruction:
            instruction.inherit_from(self._type_to_instruction[type_])
        return instruction

    def __getitem__(self, instruction_type):
        """:return: the specification for :paramref:`instruction_type`

        .. seealso:: :meth:`as_instruction`
        """
        return self.as_instruction({TYPE: instruction_type})

    @property
    def loaded_types(self):
        """The types loaded in this library.

        :return: a list of types, preferably as :class:`string <str>`
        :rtype: list
        """
        return list(self._type_to_instruction)


class DefaultInstructions(InstructionLibrary):
    """The default specifications for instructions ported with this package
    """

    #: the folder relative to this module where the instructions are located
    INSTRUCTIONS_FOLDER = "instructions"

    def __init__(self):
        """Create the default instruction library without arguments.

        The default specifications are loaded automatically form this package.
        """
        super().__init__()
        self.load.relative_folder(__file__, self.INSTRUCTIONS_FOLDER)


def default_instructions():
    """:return: a default instruction library
    :rtype: DefaultInstructions

    .. warning:: The return value is mutable and you should not add new
      instructions to it. If you would like to add instructions to it,
      create a new
      :class:`~knittingpattern.InstructionLibrary.DefaultInstructions`
      instance.
    """
    global _default_instructions
    if _default_instructions is None:
        _default_instructions = DefaultInstructions()
    return _default_instructions


_default_instructions = None
__all__ = ["InstructionLibrary", "DefaultInstructions", "default_instructions"]
