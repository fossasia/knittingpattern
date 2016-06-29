

class KnittingPatternToSVG(object):
    """Converts a KnittingPattern to SVG."""

    def __init__(self, knittingpattern, layout, instruction_to_SVG, builder,
            zoom):
        """
        :param knittingpattern.KnittingPattern.KnittingPattern knittingpattern:
          a knitting pattern
        :param knittingpattern.convert.Layout.GridLayout layout:
        :param instruction_to_SVG: an Instance of
          :class:`~knittingpattern.convert.InstructionToSVG.InstructionToSVG`
          with Instructions already loaded.
        :param knittingpattern.convert.SVGBuilder.SVGBuilder builder:
        :param float zoom: the height and width of a knit instruction
        """
        self._knittingpattern = knittingpattern
        self._layout = layout
        self._instruction_to_SVG = instruction_to_SVG
        self._builder = builder
        self._zoom = zoom
        self._instruction_type_color_to_symbol = {}
        self._symbol_id_to_scale = {}

    def build_SVG_dict(self):
        """Go through the layout and build the SVG."""
        zoom = self._zoom
        layout = self._layout
        builder = self._builder
        builder.bounding_box = map(lambda f: f*zoom, layout.bounding_box)
        for x, y, instruction in self._layout.walk_instructions(
                lambda i: (i.x*zoom, i.y*zoom, i.instruction)):
            layer_id = "row-{}".format(instruction.row.id)
            symbol_id = self._instruction_to_svg_symbol(instruction)
            scale = self._symbol_id_to_scale[symbol_id]
            group = {
                    "@class": "instruction",
                    "@id": "instruction-{}".format(instruction.id),
                    "@transform": "translate({},{}),scale({})".format(
                        x, y, scale)
                }
            builder.place_svg_use(symbol_id, layer_id, group)
        builder.insert_defs(self._instruction_type_color_to_symbol.values())
        return builder.get_svg_dict()

    def _instruction_to_svg_symbol(self, instruction):
        type_ = instruction.type
        color_ = instruction.color
        to_SVG = self._instruction_to_SVG
        instruction_id = "{}:{}".format(type_, color_)
        if instruction_id not in self._instruction_type_color_to_symbol:
            svg_dict = to_SVG.instruction_to_svg_dict(instruction)
            self._compute_scale(instruction_id, svg_dict)
            symbol = self._make_symbol(svg_dict, instruction_id)
            self._instruction_type_color_to_symbol[instruction_id] = symbol
        return instruction_id

    def _make_symbol(self, svg_dict, instruction_id):
        instruction_def = svg_dict["svg"]
        symbol = {
                "@id" : instruction_id,
                "g" : instruction_def["g"],
                "title" : instruction_def["title"],
                "metadata" : instruction_def["metadata"]
            }
        return {"symbol" : symbol}

    def _compute_scale(self, instruction_id, svg_dict):
        bbox = list(map(float, svg_dict["svg"]["@viewBox"].split()))
        scale = self._zoom / (bbox[3] - bbox[1])
        self._symbol_id_to_scale[instruction_id] = scale

__all__ = ["KnittingPatternToSVG"]
