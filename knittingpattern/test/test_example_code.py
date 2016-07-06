"""The files contain example code that should work."""
import test_knittingpattern


def test_load_from_example_and_create_svg():
    """Test :meth:`knittingpattern.load_from`."""
    import knittingpattern
    k = knittingpattern.load_from().example("Cafe.json")
    k.to_svg(25).temporary_path(".svg")
