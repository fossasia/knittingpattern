from .convert import knittingpattern_to_svg as convert_knittingpattern_to_svg
from .Dumper import ContentDumper
from functools import partial


class KnittingPattern(object):

    def __init__(self, id, name, rows):
        self._id = id
        self._name = name
        self._rows = rows

    @property
    def id(self):
        """The identifier within a set of knitting patterns."""
        return self._id

    @property
    def name(self):
        """The human readable name."""
        return self._name

    @property
    def rows(self):
        """A collection of rows that this pattern is made of."""
        return self._rows

    @property
    def to_svg(self):
        """Save this object as an SVG.

        This returns a `ContentDumper` so you can do
        `to_svg.string()` or `to_svg.file()`."""
        to_svg = partial(convert_knittingpattern_to_svg, self)
        return ContentDumper(to_svg)


__all__ = ["KnittingPattern"]
