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
    its.load.file(DEFAULT_FILE)
    return its


@fixture
def loaded_knit_to_svg(loaded, knit):
    return loaded.instruction_to_svg(knit)


@fixture
def loaded_purl_to_svg(loaded, purl):
    return loaded.instruction_to_svg(purl)


class TestHasSVGForInstruction(object):
    """This tests the `InstructionToSVG.has_instruction_to_svg` method."""

    @staticmethod    
    def test_load_from_file(its, knit):
        its.load.relative_file(__name__, IMAGES_FOLDER_NAME + "/knit.svg")
        assert its.has_svg_for_instruction(knit)

    @staticmethod
    def test_nothing_is_loaded(its, knit, purl):
        assert not its.has_svg_for_instruction(knit)
        assert not its.has_svg_for_instruction(purl)

    @staticmethod
    def test_load_from_directory(its, knit, purl):
        its.load.relative_folder(__name__, IMAGES_FOLDER_NAME)
        assert its.has_svg_for_instruction(knit)
        assert its.has_svg_for_instruction(purl)

    @staticmethod
    def test_all_images_are_loaded(loaded, knit, purl, yo):
        assert its.has_svg_for_instruction(knit)
        assert its.has_svg_for_instruction(purl)
        assert its.has_svg_for_instruction(yo)

    @staticmethod
    def test_default_returns_empty_string_if_nothing_is_loaded(its, knit):
        assert its.default_instruction_to_svg(knit) == ""


class TestDefaultInstrucionToSVG(object):
    """This tests the `InstructionToSVG.default_instruction_to_svg` method."""

    @staticmethod
    def test_instruction_type_is_replaced_in_default(default, knit):
        assert "knit" in default.instruction_to_svg(knit)
       
    @staticmethod
    def test_default_instruction_is_used(default, purl):
        default_string = default.default_instruction_to_svg(purl)
        string = default.instruction_to_svg(purl)
        assert string == default_string


class TestInstructionToSVG(object):
    
    @staticmethod
    def test_file_content_is_included(loaded_knit_to_svg, knit_content):
        assert knit_content in loaded_knit_to_svg
    
    @staticmethod
    def test_first_element_is_scaled_group(loaded_knit_to_svg, knit_content):
        parsed = parse_string(loaded_knit_to_svg)
        transform = parsed.g["transform"]
        x, y, width, height = map(float, parsed.g.svg["viewbox"])
        assert x == 0
        assert y == 0
        # TODO: test that 
        # 1. this is scaled down to a 1x1 and 
        # 2. placed in the middle 

