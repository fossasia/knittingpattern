"""If the knitting pattern files """
from test_knittingpattern import *


def test_load_from_example_and_create_svg():
    """:meth:`knittingpattern.load_from`"""
    import knittingpattern
    k = knittingpattern.load_from().example("Cafe.json")
    k.to_svg(25).temporary_path(".svg")
