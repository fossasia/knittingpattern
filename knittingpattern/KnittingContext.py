
class KnittingContext(object):

    # TODO: create a new class that restructures this.
    #       the imports should no be avalable and if you look how this class
    #       is used: it is really only a method for parsing.

    from .Loader import JSONLoader as Loader
    from .Parser import Parser, ParsingError
    from .KnittingPatternSet import KnittingPatternSet as PatternSet
    from .IdCollection import IdCollection as PatternCollection
    from .IdCollection import IdCollection as RowCollection
    from .KnittingPattern import KnittingPattern as Pattern
    from .Row import Row
    from .InstructionLibrary import DefaultInstructions
    from .Instruction import InstructionInRow

    @property
    def load(self):
        return self.Loader(self._process_loaded_object)

    @property
    def parse(self):
        return self.Parser(self)

    def _process_loaded_object(self, obj):
        return self.parse.knitting_pattern_set(obj)

__all__ = ["KnittingContext"]
