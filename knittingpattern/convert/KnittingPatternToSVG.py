"""This module provides functionality to convert knitting patterns to SVG."""

from collections import OrderedDict

#: Inside the svg, the instructions are put into definitions.
#: The svg tag is renamed to the tag given in :data:`DEFINITION_HOLDER`.
DEFINITION_HOLDER = "g"

#: The default z-index, see :func:`get_z`.
DEFAULT_Z = 0

#: Instructions have a default specification. In this specification the key
#: in :data:`RENDER` points to configuration for rendering.
RENDER = "render"

#: The key to look for the z-index inside the :data:`render` specification.
#: .. seealso:: :func:`get_z`, :data:`DEFAULT_Z`
RENDER_Z = "z"


def get_z(instruction):
    """The z-index of the pattern.

    :param knittingpattern.Instruction.Instruction instruction:
      the instruction to compute the z-index from
    :return: the z-index of the instruction. Instructions with a higher z-index
      are displayed in front of instructions with lower z-index.
    :rtype: float
    """
    return instruction.get(RENDER, {}).get(RENDER_Z, DEFAULT_Z)


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
        :param instruction_to_svg: an Instance of
          :class:`~knittingpattern.convert.InstructionToSVG.InstructionToSVG`
          with Instructions already loaded.
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
        builder.bounding_box = map(lambda f: f*zoom, layout.bounding_box)
        instructions = list(layout.walk_instructions(
            lambda i: (i.x*zoom, i.y*zoom, i.instruction)))
        instructions.sort(key=lambda x_y_i: get_z(x_y_i[2]))
        for x, y, instruction in instructions:
            render_z = get_z(instruction)
            z_id = ("" if render_z == DEFAULT_Z else "-{}".format(render_z))
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

__all__ = ["KnittingPatternToSVG", "get_z", "DEFINITION_HOLDER", "RENDER_Z",
           "RENDER", "DEFAULT_Z"]
