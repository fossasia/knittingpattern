"""Dump knitting patterns to PNG files compatible with the AYAB software.

"""

from ..Dumper import ContentDumper
from .Layout import GridLayout
from .AYABPNGBuilder import AYABPNGBuilder


class AYABPNGDumper(ContentDumper):
    """This class converts knitting patterns into PNG files."""

    def __init__(self, function_that_returns_a_knitting_pattern_set):
        """Initialize the Dumper with a
        :paramref:`function_that_returns_a_knitting_pattern_set`.

        :param function_that_returns_a_knitting_pattern_set: a function that
          takes no arguments but returns a
          :class:`knittinpattern.KnittingPatternSet.KnittingPatternSet`

        When a dump is requested, the
        :paramref:`function_that_returns_a_knitting_pattern_set`
        is called and the knitting pattern set is converted and saved to the
        specified location.
        """
        super().__init__(self._dump_knitting_pattern,
                         text_is_expected=False, encoding=None)
        self.__on_dump = function_that_returns_a_knitting_pattern_set

    def _dump_knitting_pattern(self, file):
        """dump a knitting pattern to a file."""
        knitting_pattern_set = self.__on_dump()
        knitting_pattern = knitting_pattern_set.patterns.at(0)
        layout = GridLayout(knitting_pattern)
        builder = AYABPNGBuilder(*layout.bounding_box)
        builder.set_colors_in_grid(layout.walk_instructions())
        builder.write_to_file(file)

    def temporary_path(self, extension=".png"):
        return super().temporary_path(extension=extension)
    temporary_path.__doc__ = ContentDumper.temporary_path.__doc__


__all__ = ["AYABPNGDumper"]
