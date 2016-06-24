"""When parsing :class:`knitting patterns
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
    """This class contains the specification for the
    :class:`parser <knittingpattern.Parser.Parser>`.
    """

    def __init__(self, Loader=JSONLoader, Parser=Parser,
                 ParsingError=ParsingError, PatternSet=KnittingPatternSet,
                 PatternCollection=IdCollection, RowCollection=IdCollection,
                 Pattern=KnittingPattern, Row=Row,
                 DefaultInstructions=DefaultInstructions,
                 InstructionInRow=InstructionInRow):
        """Create a new parsing specification.
        """
        self.Loader = Loader
        self.Parser = Parser
        self.ParsingError = ParsingError
        self.PatternSet = PatternSet
        self.PatternCollection = PatternCollection
        self.RowCollection = RowCollection
        self.Pattern = Pattern
        self.Row = Row
        self.DefaultInstructions = DefaultInstructions
        self.InstructionInRow = InstructionInRow


def new_knitting_pattern_set_loader(specification=ParsingSpecification()):
    """create a loader for the knitting pattern set specified in
    :paramref:`specification`

    :param specification: a :class:`specification
      <knittingpattern.ParsingSpecification.ParsingSpecification>`
      for the knitting pattern set
    """
    parser = specification.Parser(specification)
    loader = specification.Loader(parser.knitting_pattern_set)
    return loader


__all__ = ["ParsingSpecification", "new_knitting_pattern_set_loader"]
