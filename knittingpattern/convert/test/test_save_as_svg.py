from test import *
from knittingpattern import load_from_relative_file
import untangle


def is_svg(path):
    svg = untangle.parse(path).svg
    assert svg.g, "there are rows"


def test_can_convert_block_to_svg():
    pattern = load_from_relative_file(__name__, "test_patterns/block4x4.json")
    # path = pattern.to_svg.temporary_path()
    # assert is_svg(path)
    # TODO
