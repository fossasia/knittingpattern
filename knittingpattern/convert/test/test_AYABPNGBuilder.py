from test import *
from knittingpattern.convert.AYABPNGBuilder import AYABPNGBuilder

@fixture
def file():
    return io.StringIO()


@fixture
def builder(file):
    return AYABPNGBuilder(file, -1, -1, 10, 5)


class TestColorConversion(object):

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

    pass # TODO