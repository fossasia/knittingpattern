"""Test creating png files from knitting patterns.

Each pixel is an instruction."""
from test_convert import fixture, pytest, MagicMock, call
from knittingpattern.convert.AYABPNGBuilder import AYABPNGBuilder
from collections import namedtuple
import PIL.Image
import tempfile


ColorInGrid = namedtuple("ColorInGrid", ["x", "y", "color"])


@fixture
def builder():
    return AYABPNGBuilder(-1, -1, 10, 5)


class TestColorConversion(object):
    """Convert color names to RGB colors.

    One could use the webcolors package for that:
      https://pypi.python.org/pypi/webcolors/
    """

    @fixture
    def convert(self):
        return AYABPNGBuilder._convert_color_to_rrggbb

    def test_convert_24_bit(self, convert):
        assert convert("#123456") == "#123456"

    def test_convert_blue(self, convert):
        assert convert("blue") == "#0000ff"

    def test_can_convert_anything_to_color(self, convert):
        assert convert("ajsdkahsj") != convert("ajsahsj")


class TestBounds(object):
    """Check whether points are inside and outside of the bounds."""
    @pytest.mark.parametrize('x, y', [(0, 0), (-1, 0), (0, -1), (0, 4),
                                      (9, 4)])
    def test_inside(self, builder, x, y):
        assert builder.is_in_bounds(x, y)

    @pytest.mark.parametrize('x, y', [(-2, -2), (10, 0), (5, 5), (30, 30),
                                      (12, 12)])
    def test_outside(self, builder, x, y):
        assert not builder.is_in_bounds(x, y)


class TestSetPixel(object):

    @fixture
    def set(self):
        return MagicMock()

    @fixture
    def patched(self, builder, set):
        builder._set_pixel = set
        return builder

    def test_set_pixel(self, patched, set):
        patched.set_pixel(1, 2, "#aaaaaa")
        set.assert_called_with(1, 2, "#aaaaaa")

    def test_set_pixel_converts_color(self, patched, set):
        patched.set_pixel(2, 3, "black")
        set.assert_called_with(2, 3, "#000000")

    def test_set_with_instruction(self, patched, set):
        patched.set_color_in_grid(ColorInGrid(0, 0, "#adadad"))
        set.assert_called_with(0, 0, "#adadad")

    def test_call_many_instructions(self, patched, set):
        patched.set_colors_in_grid([
                ColorInGrid(0, 0, "#000000"),
                ColorInGrid(0, 1, "#111111"),
                ColorInGrid(2, 0, "#222222")
            ])
        set.assert_has_calls([call(0, 0, "#000000"),
                              call(0, 1, "#111111"),
                              call(2, 0, "#222222")])

    def test_setiing_color_none_does_nothing(self, patched, set):
        patched.set_pixel(2, 2, None)
        patched.set_color_in_grid(ColorInGrid(0, 0, None))
        patched.set_colors_in_grid([
                ColorInGrid(0, 0, None),
                ColorInGrid(0, 1, None),
                ColorInGrid(2, 0, None)
            ])
        assert not set.called


class TestSavingAsPNG(object):

    @fixture(scope="class")
    def image_path(self):
        return tempfile.mktemp()

    @fixture(scope="class")
    def builder(self, image_path):
        builder = AYABPNGBuilder(-1, -1, 2, 2)
        # set pixels inside
        builder.set_pixel(0, 0, "#000000")
        builder.set_pixel(-1, -1, "#111111")
        builder.set_pixel(1, 1, "#222222")
        # set out of bounds pixels
        builder.set_colors_in_grid([ColorInGrid(12, 12, "red")])
        builder.set_color_in_grid(ColorInGrid(-3, -3, "#adadad"))
        builder.set_pixel(-3, 4, "#adadad")
        builder.write_to_file(image_path)
        return builder

    @fixture(scope="class")
    def image(self, image_path, builder):
        return PIL.Image.open(image_path)

    def test_pixels_are_set(self, image):
        assert image.getpixel((1, 1)) == (0, 0, 0)
        assert image.getpixel((0, 0)) == (0x11, 0x11, 0x11)
        assert image.getpixel((2, 2)) == (0x22, 0x22, 0x22)

    def test_bbox_is_3x3(self, image):
        assert image.getbbox() == (0, 0, 3, 3)

    def test_other_pixels_have_default_color(self, image):
        assert image.getpixel((1, 2)) == (255, 255, 255)


class TestDefaultColor(object):

    @fixture
    def default_color(self, builder):
        return builder.default_color

    def test_can_change_default_color(self):
        builder = AYABPNGBuilder(-1, -1, 2, 2, "black")
        assert builder.default_color == "black"

    def test_default_color_is_white(self, default_color):
        assert default_color == "white"
