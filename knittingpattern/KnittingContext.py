
class KnittingContext(object):

    from .Loader import Loader
    from .Parser import Parser, ParsingError
    from .KnittingPatternSet import KnittingPatternSet as PatternSet
    from .IdCollection import IdCollection as PatternCollection
    from .IdCollection import IdCollection as RowCollection
    from .KnittingPattern import KnittingPattern as Pattern
    from .Row import Row

    @property
    def load(self):
        return self.Loader(self._process_loaded_object)

    def _new_parser(self):
        return self.Parser(self)

    def _process_loaded_object(self, obj):
        parser = self._new_parser()
        return parser.parse(obj)
