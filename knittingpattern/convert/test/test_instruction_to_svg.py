from test_images import *
from test import *
from knittingpattern.convert.InstructionToSVG import InstructionToSVG
import re


@fixture
def knit():
    knit = MagicMock()
    knit.type = "knit"
    return knit


@fixture
def purl():
    purl = MagicMock()
    purl.type = "purl"
    return purl


@fixture
def yo():
    yo = MagicMock()
    yo.type = "yo"
    return yo


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


@fixture
def loaded_knit_to_svg(loaded, knit):
    return loaded.instruction_to_svg(knit)


@fixture
def loaded_purl_to_svg(loaded, purl):
    return loaded.instruction_to_svg(purl)


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
        assert its.default_instruction_to_svg(knit) == ""


class TestDefaultInstrucionToSVG(object):
    """This tests the `InstructionToSVG.default_instruction_to_svg` method."""

    def test_instruction_type_is_replaced_in_default(self, default, knit):
        assert "knit" in default.instruction_to_svg(knit)

    def test_default_instruction_is_used(self, default, purl):
        default_string = default.default_instruction_to_svg(purl)
        string = default.instruction_to_svg(purl)
        assert string == default_string


class TestInstructionToSVG(object):

    def test_file_content_is_included(self, loaded_knit_to_svg, knit_content):
        assert knit_content in loaded_knit_to_svg

    def test_first_element_is_scaled_group(self, loaded_knit_to_svg,
                                           knit_content):
        parsed = parse_string(loaded_knit_to_svg)
        # transform = parsed.g["transform"]
        # x, y, width, height = map(float, parsed.g.svg["viewbox"])
        # assert x == 0
        # assert y == 0
        # TODO: test that
        # 1. this is scaled down to a 1x1 and
        # 2. placed in the middle
