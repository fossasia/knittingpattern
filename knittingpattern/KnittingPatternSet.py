"""A set of knitting patterns that can be written to JSON and from JSON.

"""

from .convert.AYABPNGDumper import AYABPNGDumper
from .Dumper import ContentDumper
from .convert.InstructionToSVG import default_instructions_to_SVG
from .convert.Layout import GridLayout
from .convert.SVGBuilder import SVGBuilder


class KnittingPatternSet(object):
    """This is the class for a set of :class:`knitting patterns
    <knittingpattern.KnittingPattern.KnittingPattern>`.
    """

    def __init__(self, type_, version, patterns, comment=None):
        """create a new knitting pattern set

        :param str type: the type of the knitting pattern set, see the
          :ref:`specification <FileFormatSpecification>`.
        :param str version: the version of the knitting pattern set.
          This is not the version of the library but the version of the
          :ref:`specification <FileFormatSpecification>`.
        :param patterns: a collection of patterns. This should be a
          :class:`~knittingpattern.IdCollection.IdCollection` of
          :class:`KnittingPatterns
          <knittingpattern.KnittingPattern.KnittingPattern>`.
        """
        self._version = version
        self._type = type_
        self._patterns = patterns
        self._comment = comment

    @property
    def version(self):
        """:return: the version of the knitting pattern, see :meth:`__init__`
        """
        return self._version

    @property
    def type(self):
        """:return: the type of the knitting pattern, see :meth:`__init__`
        """
        return self._type

    @property
    def patterns(self):
        """:return: the patterns of the knitting pattern, see :meth:`__init__`
        :rtype: knittingpattern.IdCollection.IdCollection
        """
        return self._patterns

    @property
    def comment(self):
        """
        :return: the comment for the knitting pattern set or None,
          see :meth:`__init__`
        """
        return self._comment

    def to_ayabpng(self):
        """:return: a dumper to save this pattern set as png for the AYAB
          software
        :rtype: knittingpattern.convert.AYABPNGDumper.AYABPNGDumper

        Example:

        .. code:: python

            >>> knitting_pattern_set.to_ayabpng().temporary_path()
            "/the/path/to/the/file.png"

        """
        return AYABPNGDumper(lambda: self)

    def to_svg(self, zoom):
        """
        :param float zoom: the height and width of a knit instruction
        :return: a dumper to save the svg to
        :rtype: knittingpattern.Dumper.ContentDumper

        Example:

        .. code:: python

            >>> knitting_pattern_set.to_svg().temporary_path()
            "/the/path/to/the/file.svg"
        """
        def on_dump(file):
            """dumps the knitting pattern to the file"""
            knitting_pattern = self.patterns.at(0)
            layout = GridLayout(knitting_pattern)
            instruction_to_SVG = default_instructions_to_SVG()
            builder = SVGBuilder()
            builder.bounding_box = map(lambda f: f*zoom, layout.bounding_box)
            for x, y, instruction in layout.walk_instructions(
                    lambda i: (i.x*zoom, i.y*zoom, i.instruction)):
                layer_id = "row-{}".format(instruction.row.id)
                svg = instruction_to_SVG.instruction_to_svg_dict(instruction)
                bbox = list(map(float, svg["svg"]["@viewBox"].split()))
                scale = zoom / (bbox[3] - bbox[1])
                group = {
                        "@class": "instruction",
                        "@id": "instruction-{}".format(instruction.id),
                        "@transform": "translate({},{}),scale({})".format(
                            x, y, scale)
                    }
                builder.place_svg_dict(x, y, svg, layer_id, group)
            builder.write_to_file(file)
        return ContentDumper(on_dump)


__all__ = ["KnittingPatternSet"]
