from test import *
from knittingpattern import load_from_relative_file
import untangle


@fixture(scope="module")
def patterns():
    return load_from_relative_file(__name__, "test_patterns/block4x4.json")


@fixture(scope="module")
def path(patterns):
    return patterns.to_svg.temporary_path()
    

@fixture(scope="module")
def svg(path):
    return untangle.parse(path).svg


def test_svg_contains_four_rows(svg):
    assert len(svg.g) == 4

