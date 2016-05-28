
class KnittingPatternSet(object):

    def __init__(self, type, version, pattern):
        self._version = version
        self._type = type
        self._pattern = pattern

    @property
    def version(self):
        return self._version

    @property
    def type(self):
        return self._type

    @property
    def pattern(self):
        return self._pattern


__all__ = ["KnittingPatternSet"]
