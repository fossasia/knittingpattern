from test import *


def test_import():
    import knittingpattern
    print(knittingpattern.__file__)
    assert knittingpattern.__version__
