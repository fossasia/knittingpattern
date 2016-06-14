
class KnittingPatternSet(object):

    def __init__(self, type, version, patterns, comment=None):
        self._version = version
        self._type = type
        self._patterns = patterns
        self._comment = comment

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

    @property
    def comment(self):
        """Returns the comment for the knitting pattern set or None."""
        return self._comment


__all__ = ["KnittingPatternSet"]
