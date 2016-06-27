from test_convert import fixture, pytest
from knittingpattern import load_from_relative_file
import PIL.Image


@fixture(scope="module")
def block4x4():
    return load_from_relative_file(__name__, "test_patterns/block4x4.json")


@fixture(scope="module")
def path(block4x4):
    return block4x4.to_ayabpng().temporary_path()


@fixture(scope="module")
def image(path):
    return PIL.Image.open(path)


@pytest.mark.parametrize('xy', [(i, i) for i in range(4)])
def test_there_is_a_green_line(image, xy):
    assert image.getpixel(xy) == (0, 128, 0)


def test_path_ends_with_png(path):
    assert path.endswith(".png")
