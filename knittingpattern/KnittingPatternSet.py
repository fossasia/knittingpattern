
class KnittingPatternSet(object):

    def __init__(self, type, version, patterns):
        self._version = version
        self._type = type
        self._patterns = patterns

    @property
    def version(self):
        return self._version

    @property
    def type(self):
        return self._type

    @property
    def patterns(self):
        return self._patterns

    def to_svg(self):
        pass


__all__ = ["KnittingPatternSet"]
