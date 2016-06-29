from collections import OrderedDict


DEFINITION_HOLDER = "g"
DEFAULT_Z = 0
RENDER = "render"
RENDER_Z = "z"


def get_z(instruction):
    return instruction.get(RENDER, {}).get(RENDER_Z, DEFAULT_Z)


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
        self._instruction_type_color_to_symbol = OrderedDict()
        self._symbol_id_to_scale = {}

    def build_SVG_dict(self):
        """Go through the layout and build the SVG."""
        zoom = self._zoom
        layout = self._layout
        builder = self._builder
        builder.bounding_box = map(lambda f: f*zoom, layout.bounding_box)
        instructions = layout.walk_instructions(lambda i: (i.x*zoom, i.y*zoom,
                                                           i.instruction))
        instructions.sort(lambda x_y_i: get_z(x_y_i[2]))
        for x, y, instruction in instructions:
            render_z = get_z(instruction)
            z_id = ("" if render_z == DEFAULT_Z else "-{}".format(render_z))
            layer_id = "row-{}{}".format(instruction.row.id, z_id)
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
        """:return: the id of a symbol in the defs for the specified
        :paramref:`instruction`.
        
        :rtype: str
        If no symbol yet exists in the defs for the :paramref:`instruction` a
        symbol is created and saved using :meth:`_make_symbol`.
        """
        type_ = instruction.type
        color_ = instruction.color
        to_SVG = self._instruction_to_SVG
        instruction_id = "{}:{}".format(type_, color_)
        defs_id = instruction_id + ":defs"
        if instruction_id not in self._instruction_type_color_to_symbol:
            svg_dict = to_SVG.instruction_to_svg_dict(instruction)
            self._compute_scale(instruction_id, svg_dict)
            symbol = self._make_symbol(svg_dict, instruction_id)
            self._instruction_type_color_to_symbol[defs_id] = \
                symbol[DEFINITION_HOLDER].pop("defs", {})
            self._instruction_type_color_to_symbol[instruction_id] = symbol
        return instruction_id

    def _make_symbol(self, svg_dict, instruction_id):
        """Create a symbol out of the supplied :paramref:`svg_dict`.

        :param dict svg_dict: dictionary containing the SVG for the
          instruction currently processed
        :param str instruction_id: id that will be assigned to the symbol"""
        instruction_def = svg_dict["svg"]
        blacklisted_elements = ["sodipodi:namedview", "metadata"]
        whitelisted_attributes = ["@sodipodi:docname"]
        symbol = OrderedDict({"@id": instruction_id})
        for content, value in instruction_def.items():
            if content.startswith('@'):
                if content in whitelisted_attributes:
                    symbol[content] = value
            elif content not in blacklisted_elements:
                symbol[content] = value
        return {DEFINITION_HOLDER: symbol}

    def _compute_scale(self, instruction_id, svg_dict):
        """compute the scale using the bounding box stored in the
        :paramref:`svg_dict`. 
        
        The scale is saved in a dictionary using :paramref:`instruction_id` as 
        key.
        :param str instruction_id: id identifying a symbol in the defs
        :param dict svg_dict: dictionary containing the SVG for the
          instruction currently processed"""
        bbox = list(map(float, svg_dict["svg"]["@viewBox"].split()))
        scale = self._zoom / (bbox[3] - bbox[1])
        self._symbol_id_to_scale[instruction_id] = scale

__all__ = ["KnittingPatternToSVG"]
