"""This module provides functionality to convert knitting patterns to SVG."""

from collections import OrderedDict

#: Inside the svg, the instructions are put into definitions.
#: The svg tag is renamed to the tag given in :data:`DEFINITION_HOLDER`.
DEFINITION_HOLDER = "g"


class KnittingPatternToSVG(object):
    """Converts a KnittingPattern to SVG.

    This is inspired by the method object pattern, since building an SVG
    requires several steps.
    """

    def __init__(self, knittingpattern, layout, instruction_to_svg, builder,
                 zoom):
        """
        :param knittingpattern.KnittingPattern.KnittingPattern knittingpattern:
          a knitting pattern
        :param knittingpattern.convert.Layout.GridLayout layout:
        :param instruction_to_svg: an
          :class:`~knittingpattern.convert.InstructionToSVG.InstructionToSVG`
          :class:`
          ~knittingpattern.convert.InstructionToSVGCache.InstructionSVGCache`,
          both with instructions already loaded.
        :param knittingpattern.convert.SVGBuilder.SVGBuilder builder:
        :param float zoom: the height and width of a knit instruction
        """
        self._knittingpattern = knittingpattern
        self._layout = layout
        self._instruction_to_svg = instruction_to_svg
        self._builder = builder
        self._zoom = zoom
        self._instruction_type_color_to_symbol = OrderedDict()
        self._symbol_id_to_scale = {}

    def build_SVG_dict(self):
        """Go through the layout and build the SVG.

        :return: an xml dict that can be exported using a
          :class:`~knittingpattern.Dumper.XMLDumper`
        :rtype: dict
        """
        zoom = self._zoom
        layout = self._layout
        builder = self._builder
        bbox = list(map(lambda f: f*zoom, layout.bounding_box))
        builder.bounding_box = bbox
        flip_x = bbox[2] + bbox[0] * 2
        flip_y = bbox[3] + bbox[1] * 2
        instructions = list(layout.walk_instructions(
            lambda i: (flip_x - (i.x + i.width) * zoom,
                       flip_y - (i.y + i.height) * zoom,
                       i.instruction)))
        instructions.sort(key=lambda x_y_i: x_y_i[2].render_z)
        for x, y, instruction in instructions:
            render_z = instruction.render_z
            z_id = ("" if not render_z else "-{}".format(render_z))
            layer_id = "row-{}{}".format(instruction.row.id, z_id)
            def_id = self._register_instruction_in_defs(instruction)
            scale = self._symbol_id_to_scale[def_id]
            group = {
                    "@class": "instruction",
                    "@id": "instruction-{}".format(instruction.id),
                    "@transform": "translate({},{}),scale({})".format(
                        x, y, scale)
                }
            builder.place_svg_use(def_id, layer_id, group)
        builder.insert_defs(self._instruction_type_color_to_symbol.values())
        return builder.get_svg_dict()

    def _register_instruction_in_defs(self, instruction):
        """Create a definition for the instruction.

        :return: the id of a symbol in the defs for the specified
          :paramref:`instruction`
        :rtype: str

        If no symbol yet exists in the defs for the :paramref:`instruction` a
        symbol is created and saved using :meth:`_make_symbol`.
        """
        type_ = instruction.type
        color_ = instruction.color
        instruction_to_svg_dict = \
            self._instruction_to_svg.instruction_to_svg_dict
        instruction_id = "{}:{}".format(type_, color_)
        defs_id = instruction_id + ":defs"
        if instruction_id not in self._instruction_type_color_to_symbol:
            svg_dict = instruction_to_svg_dict(instruction)
            self._compute_scale(instruction_id, svg_dict)
            symbol = self._make_definition(svg_dict, instruction_id)
            self._instruction_type_color_to_symbol[defs_id] = \
                symbol[DEFINITION_HOLDER].pop("defs", {})
            self._instruction_type_color_to_symbol[instruction_id] = symbol
        return instruction_id

    def _make_definition(self, svg_dict, instruction_id):
        """Create a symbol out of the supplied :paramref:`svg_dict`.

        :param dict svg_dict: dictionary containing the SVG for the
          instruction currently processed
        :param str instruction_id: id that will be assigned to the symbol
        """
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
        """Compute the scale of an instruction svg.

        Compute the scale using the bounding box stored in the
        :paramref:`svg_dict`. The scale is saved in a dictionary using
        :paramref:`instruction_id` as key.

        :param str instruction_id: id identifying a symbol in the defs
        :param dict svg_dict: dictionary containing the SVG for the
          instruction currently processed
        """
        bbox = list(map(float, svg_dict["svg"]["@viewBox"].split()))
        scale = self._zoom / (bbox[3] - bbox[1])
        self._symbol_id_to_scale[instruction_id] = scale

__all__ = ["KnittingPatternToSVG", "DEFINITION_HOLDER"]
