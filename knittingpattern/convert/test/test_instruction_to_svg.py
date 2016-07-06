from test_images import IMAGES_FOLDER, DEFAULT_FILE,\
    IMAGES_FOLDER_NAME, is_knit, is_purl
from test_convert import fixture, parse_string
from knittingpattern.convert.InstructionToSVG import InstructionToSVG
from collections import namedtuple

Instruction = namedtuple("TestInstruction", ["type", "hex_color"])
XML_START = '<?xml version="1.0" encoding="utf-8"?>\n<svg></svg>'


@fixture
def knit():
    return Instruction("knit", "green")


@fixture
def purl():
    return Instruction("purl", "red")


@fixture
def yo():
    return Instruction("yo", "brown")


@fixture
def its():
    return InstructionToSVG()


@fixture
def loaded(its):
    its.load.folder(IMAGES_FOLDER)
    return its


@fixture
def default(its):
    its.load.path(DEFAULT_FILE)
    return its


class TestHasSVGForInstruction(object):
    """This tests the `InstructionToSVG.has_instruction_to_svg` method."""

    def test_load_from_file(self, its, knit):
        its.load.relative_file(__name__, IMAGES_FOLDER_NAME + "/knit.svg")
        assert its.has_svg_for_instruction(knit)

    def test_nothing_is_loaded(self, its, knit, purl):
        assert not its.has_svg_for_instruction(knit)
        assert not its.has_svg_for_instruction(purl)

    def test_load_from_directory(self, its, knit, purl):
        its.load.relative_folder(__name__, IMAGES_FOLDER_NAME)
        assert its.has_svg_for_instruction(knit)
        assert its.has_svg_for_instruction(purl)

    def test_all_images_are_loaded(self, loaded, knit, purl, yo):
        assert loaded.has_svg_for_instruction(knit)
        assert loaded.has_svg_for_instruction(purl)
        assert loaded.has_svg_for_instruction(yo)

    def test_default_returns_empty_string_if_nothing_is_loaded(self, its,
                                                               knit):
        assert its.default_instruction_to_svg(knit) == XML_START


class TestDefaultInstrucionToSVG(object):
    """This tests the `InstructionToSVG.default_instruction_to_svg` method."""

    def test_instruction_type_is_replaced_in_default(self, default, knit):
        assert "knit" in default.instruction_to_svg(knit)

    def test_default_instruction_is_used(self, default, purl):
        default_string = default.default_instruction_to_svg(purl)
        string = default.instruction_to_svg(purl)
        assert string == default_string


def is_color_layer(layer):
    layer_has_label_color = layer["inkscape:label"] == "color"
    layer_is_of_mode_layer = layer["inkscape:groupmode"] == "layer"
    return layer_has_label_color and layer_is_of_mode_layer


def color_layers(svg):
    return [layer for layer in svg.g if is_color_layer(layer)]


def assert_has_one_colored_layer(svg):
    assert len(color_layers(svg)) == 1


def assert_fill_has_color_of(svg, instruction):
    colored_layer = color_layers(svg)[0]
    element = (colored_layer.rect
               if "rect" in dir(colored_layer)
               else colored_layer.circle)
    style = element["style"]
    assert "fill:" + instruction.hex_color in style


class TestInstructionToSVG(object):

    @fixture
    def knit_svg(self, loaded, knit):
        return parse_string(loaded.instruction_to_svg(knit)).svg

    @fixture
    def purl_svg(self, loaded, purl):
        return parse_string(loaded.instruction_to_svg(purl)).svg

    def test_file_content_is_included(self, knit_svg):
        assert is_knit(knit_svg)

    def test_file_content_is_purl(self, purl_svg):
        assert is_purl(purl_svg)

    def test_returned_object_is_svg_with_viewbox(self, knit_svg):
        assert len(knit_svg["viewBox"].split()) == 4

    def test_there_is_one_color_layer(self, knit_svg):
        assert_has_one_colored_layer(knit_svg)

    def test_purl_has_one_color_layer(self, purl_svg):
        assert_has_one_colored_layer(purl_svg)

    def test_fill_in_colored_layer_is_replaced_by_color(self, knit_svg, knit):
        assert_fill_has_color_of(knit_svg, knit)

    def test_purl_is_colored(self, purl_svg, purl):
        assert_fill_has_color_of(purl_svg, purl)

    # TODO: test colored layer so it does everything as specified
