from test import *
from knittingpattern.convert.image_to_knittingpattern import *
from knittingpattern import load_from_object
from PIL import Image


IMAGE_PATH = os.path.join(HERE, "pictures")


@fixture(scope="module")
def patterns(image_path):
    object = convert_image_to_knitting_pattern.path(image_path).object()
    patterns = load_from_object(object)
    return patterns


@fixture(scope="module")
def pattern(patterns):
    return patterns.patterns.at(0)


@fixture(scope="module")
def image(image_path):
    return Image.open(image_path)


def pytest_generate_tests(metafunc):
    if 'image_path' in metafunc.fixturenames:
        metafunc.parametrize("image_path", [
                os.path.join(IMAGE_PATH, file)
                for file in os.listdir(IMAGE_PATH)
            ], scope="module")


def test_convert_image_to_knittingpattern(patterns, image_path):
    assert patterns.comment["source"] == image_path


def test_row_length_is_image_length(pattern, image):
    min_x, min_y, max_x, max_y = image.getbbox()
    assert len(pattern.rows.at(0).instructions) == max_x - min_x


def test_first_color_is_white(pattern):
    assert pattern.rows[0].instructions[0].color == "white"


def test_other_color_is_white(pattern):
    assert pattern.rows[1].instructions[1].color == "white"


def test_black_exists(pattern):
    assert pattern.rows[20].instructions[64].color == "black"
