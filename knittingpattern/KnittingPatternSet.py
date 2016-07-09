"""A set of knitting patterns that can be dumped and loaded."""

from .convert.AYABPNGDumper import AYABPNGDumper
from .Dumper import XMLDumper
from .convert.InstructionSVGCache import default_instruction_svg_cache
from .convert.Layout import GridLayout
from .convert.SVGBuilder import SVGBuilder
from .convert.KnittingPatternToSVG import KnittingPatternToSVG


class KnittingPatternSet(object):

    """This is the class for a set of knitting patterns.

    The :class:`knitting patterns
    <knittingpattern.KnittingPattern.KnittingPattern>` all have an id and can
    be accessed from here. It is possible to load this set of knitting patterns
    from various locations, see the :mod:`knittingpattern` module.
    You rarely need to create such a pattern yourself. It is easier to create
    the pattern by loading it from a file.
    """

    def __init__(self, type_, version, patterns, parser, comment=None):
        """Create a new knitting pattern set.

        This is the class for a set of :class:`knitting patterns
        <knittingpattern.KnittingPattern.KnittingPattern>`.

        :param str type: the type of the knitting pattern set, see the
          :ref:`specification <FileFormatSpecification>`.
        :param str version: the version of the knitting pattern set.
          This is not the version of the library but the version of the
          :ref:`specification <FileFormatSpecification>`.
        :param patterns: a collection of patterns. This should be a
          :class:`~knittingpattern.IdCollection.IdCollection` of
          :class:`KnittingPatterns
          <knittingpattern.KnittingPattern.KnittingPattern>`.
        :param comment: a comment about the knitting pattern
        """
        self._version = version
        self._type = type_
        self._patterns = patterns
        self._comment = comment
        self._parser = parser

    @property
    def version(self):
        """The version of the knitting pattern specification.

        :return: the version of the knitting pattern, see :meth:`__init__`
        :rtype: str

        .. seealso:: :ref:`FileFormatSpecification`
        """
        return self._version

    @property
    def type(self):

        """The type of the knitting pattern.

        :return: the type of the knitting pattern, see :meth:`__init__`
        :rtype: str

        .. seealso:: :ref:`FileFormatSpecification`
        """
        return self._type

    @property
    def patterns(self):
        """The pattern contained in this set.

        :return: the patterns of the knitting pattern, see :meth:`__init__`
        :rtype: knittingpattern.IdCollection.IdCollection

        The patterns can be accessed by their id.
        """
        return self._patterns

    @property
    def comment(self):
        """The comment about the knitting pattern.

        :return: the comment for the knitting pattern set or None,
          see :meth:`__init__`.
        """
        return self._comment

    def to_ayabpng(self):
        """Convert the knitting pattern to a png.

        :return: a dumper to save this pattern set as png for the AYAB
          software
        :rtype: knittingpattern.convert.AYABPNGDumper.AYABPNGDumper

        Example:

        .. code:: python

            >>> knitting_pattern_set.to_ayabpng().temporary_path()
            "/the/path/to/the/file.png"

        """
        return AYABPNGDumper(lambda: self)

    def to_svg(self, zoom):
        """Create an SVG from the knitting pattern set.

        :param float zoom: the height and width of a knit instruction
        :return: a dumper to save the svg to
        :rtype: knittingpattern.Dumper.XMLDumper

        Example:

        .. code:: python

            >>> knitting_pattern_set.to_svg(25).temporary_path(".svg")
            "/the/path/to/the/file.svg"
        """
        def on_dump():
            """Dump the knitting pattern to the file.

            :return: the SVG XML structure as dictionary.
            """
            knitting_pattern = self.patterns.at(0)
            layout = GridLayout(knitting_pattern)
            instruction_to_svg = default_instruction_svg_cache()
            builder = SVGBuilder()
            kp_to_svg = KnittingPatternToSVG(knitting_pattern, layout,
                                             instruction_to_svg, builder, zoom)
            return kp_to_svg.build_SVG_dict()
        return XMLDumper(on_dump)

    def add_new_pattern(self, id_, name=None):
        """Add a new, empty knitting pattern to the set.

        :param id_: the id of the pattern
        :param name: the name of the pattern to add or if :obj:`None`, the
          :paramref:`id_` is used
        :return: a new, empty knitting pattern
        :rtype: knittingpattern.KnittingPattern.KnittingPattern
        """
        if name is None:
            name = id_
        pattern = self._parser.new_pattern(id_, name)
        self._patterns.append(pattern)
        return pattern


__all__ = ["KnittingPatternSet"]
