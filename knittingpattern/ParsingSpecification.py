"""This modules specifies how to convert JSON to knitting patterns.

When parsing :class:`knitting patterns
<knittingpattern.KnittingPatternSet.KnittingPatternSet>` a lot of classes can
be used.

The :class:`ParsingSpecification` is the one place where to go to change a
class that is used throughout the whole structure loaded by e.g. a
:class:`knittingpattern.Parser.Parser`.
:func:`new_knitting_pattern_set_loader` is a convinient interface for
loading knitting patterns.

These functions should do the same:

.. code:: python

    # (1) load from module
    import knittingpattern
    kp = knittingpattern.load_from_file("my_pattern")

    # (2) load from knitting pattern
    from knittingpattern.ParsingSpecification import *
    kp = new_knitting_pattern_set_loader().file("my_pattern")

"""
from .Loader import JSONLoader
from .Parser import Parser, ParsingError
from .KnittingPatternSet import KnittingPatternSet
from .IdCollection import IdCollection
from .KnittingPattern import KnittingPattern
from .Row import Row
from .InstructionLibrary import DefaultInstructions
from .Instruction import InstructionInRow


class ParsingSpecification(object):

    """This is the specification for knitting pattern parsers.

    The :class:`<knittingpattern.Parser.Parser>` uses this specification
    to parse the knitting patterns. You can change every class in the data
    structure to add own functionality.
    """

    def __init__(self,
                 new_loader=JSONLoader,
                 new_parser=Parser,
                 new_parsing_error=ParsingError,
                 new_pattern_set=KnittingPatternSet,
                 new_pattern_collection=IdCollection,
                 new_row_collection=IdCollection,
                 new_pattern=KnittingPattern,
                 new_row=Row,
                 new_default_instructions=DefaultInstructions,
                 new_instruction_in_row=InstructionInRow):
        """Create a new parsing specification."""
        self.new_loader = new_loader
        self.new_parser = new_parser
        self.new_parsing_error = new_parsing_error
        self.new_pattern_set = new_pattern_set
        self.new_pattern_collection = new_pattern_collection
        self.new_row_collection = new_row_collection
        self.new_pattern = new_pattern
        self.new_row = new_row
        self.new_default_instructions = new_default_instructions
        self.new_instruction_in_row = new_instruction_in_row


class DefaultSpecification(ParsingSpecification):

    """This is the default specification.

    It is created like pasing no arguments to :class:`ParsingSpecification`.
    The idea is to make the default specification easy to spot and create.
    """

    def __init__(self):
        """Initialize the default specification with no arguments."""
        super().__init__()

    @classmethod
    def __repr__(cls):
        """The string representation of the object.

        :return: the string representation
        :rtype: str
        """
        return "<{}.{}>".format(cls.__module__, cls.__qualname__)


def new_knitting_pattern_set_loader(specification=DefaultSpecification()):
    """Create a loader for a knitting pattern set.

    :param specification: a :class:`specification
      <knittingpattern.ParsingSpecification.ParsingSpecification>`
      for the knitting pattern set, default
      :class:`DefaultSpecification`
    """
    parser = specification.new_parser(specification)
    loader = specification.new_loader(parser.knitting_pattern_set)
    return loader


__all__ = ["ParsingSpecification", "new_knitting_pattern_set_loader",
           "DefaultSpecification"]
