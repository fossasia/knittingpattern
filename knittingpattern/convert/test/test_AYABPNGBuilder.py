from test import *
from knittingpattern.convert.AYABPNGBuilder import AYABPNGBuilder
from collections import namedtuple
import PIL.Image


InstructionInGrid = namedtuple("InstructionInGrid", ["x", "y", "color"])


@fixture
def file():
    return io.StringIO()


@fixture
def builder(file):
    return AYABPNGBuilder(file, -1, -1, 10, 5)


class TestColorConversion(object):
    """Convert color names to RGB colors.
    
    One could use the webcolors package for that:
      https://pypi.python.org/pypi/webcolors/
    """

    @fixture
    def convert(self):
        return AYABPNGBuilder._convert_color_to_RRGGBB

    def test_convert_24_bit(self, convert):
        assert convert("#123456") == "#123456"
    
    def test_convert_blue(self, convert):
        assert convert("blue") == "#0000ff"
        
    def test_can_convert_anything_to_color(self, convert):
        assert convert("ajsdkahsj") != convert("ajsahsj")


class TestWithStatement(object):
    """Use the with-satement with AYABPNGBuilder"""
    
    @fixture
    def patched(self, builder):
        builder.close = MagicMock()
        builder.open = MagicMock()
    
    def test_not_opened_not_closed(self, patched):
        assert not patched.open.called
        assert not patched.close.called
    
    def test_open_is_called_in_with(self, patched):
        with patched:
            assert patched.open.called
            assert not patched.close.called
    
    def test_close_is_called_at_the_end(self, patched):
        with patched:
            pass
        assert patched.close.called


class TestBounds(object):
    """Check whether points are inside and outside of the bounds."""
    
    def test_inside(self, builder):
        assert builder.is_in_bounds(0, 0)
        assert builder.is_in_bounds(-1, 0)
        assert builder.is_in_bounds(0, -1)
        assert builder.is_in_bounds(0, 4)
        assert builder.is_in_bounds(9, 4)
    
    def test_outside(self, builder):
        assert not builder.is_in_bounds(-2, -2)
        assert not builder.is_in_bounds(10, 0)
        assert not builder.is_in_bounds(5, 5)
    

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
        patched.set_instruction_in_grid(InstructionInGrid(0, 0, "#adadad"))
        set.assert_called_with(0, 0, "#adadad")
    
    def test_call_many_instructions(self, patched, set):
        patched.set_instructions_in_grid([
                InstructionInGrid(0, 0, "#000000"),
                InstructionInGrid(0, 1, "#111111"),
                InstructionInGrid(2, 0, "#222222")
            ])
        set.assert_has_calls([(0, 0, "#000000"), (0, 1, "#111111"), 
                              (2, 0, "#222222")])


class TestSavingAsPNG(object):
    
    @fixture
    def image_file(self, tmpdir):
        return tmpdir.join("test.png")
     
    @fixture
    def builder(self, image_file):
        builder = AYABPNGBuilder(image_file, -1, -1, 2, 2)
        with builder:
            builder.set_pixel(0, 0, "#000000")
            builder.set_pixel(-1, -1, "#111111")
            builder.set_pixel(1, 1, "#222222")
        return builder
        
    @fixture
    def image(self, image_file, builder):
        return PIL.Image.open(image_file.strpath)
        
    @fixture
    def default_color(self, builder):
        return builder.default_color
    
    def test_pixels_are_set(self, image):
        assert image.getpixel(1,1) == "#000000"
        assert image.getpixel(0,0) == "#111111"
        assert image.getpixel(2,2) == "#333333"
    
    def test_bbox_is_3x3(self, image):
        assert image.getbbox() == (0, 0, 3, 3)
    
    def test_other_pixels_have_default_color(self, image):
        assert image.getpixel(1,2) == "#000000"
        
    def test_default_color_is_black(self, builder):
        assert builder.default_color == "black"