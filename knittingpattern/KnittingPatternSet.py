from .convert.AYABPNGDumper import AYABPNGDumper
from .Dumper import ContentDumper
from .convert.InstructionToSVG import default_instructions_to_SVG
from .convert.Layout import GridLayout
from .convert.SVGBuilder import SVGBuilder


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

    @property
    def comment(self):
        """Returns the comment for the knitting pattern set or None."""
        return self._comment

    def to_ayabpng(self):
        """Returns a Dumper to save this pattern set as png for AYAB."""
        return AYABPNGDumper(lambda: self)

    def to_svg(self, zoom):
        def on_dump(file):
            knitting_pattern = self.patterns.at(0)
            layout = GridLayout(knitting_pattern)
            instruction_to_SVG = default_instructions_to_SVG()
            builder = SVGBuilder()
            builder.bounding_box = map(lambda f: f*zoom, layout.bounding_box)
            for x, y, instruction in layout.walk_instructions(
                    lambda i: (i.x*zoom, i.y*zoom, i.instruction)):
                layer_id = "row-{}".format(instruction.row.id)
                svg = instruction_to_SVG.instruction_to_svg_dict(instruction)
                min_x, min_y, max_x, max_y = \
                    map(float, svg["svg"]["@viewBox"].split())
                scale = zoom/(max_y-min_y)
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
