from test_convert import fixture, HERE, os
from knittingpattern.convert.image_to_knittingpattern import \
    convert_image_to_knitting_pattern
from knittingpattern import convert_from_image
from PIL import Image


IMAGE_PATH = os.path.join(HERE, "pictures")


@fixture(scope="module")
def patterns(image_path, convert):
    loader = convert()
    return loader.path(image_path).knitting_pattern()


@fixture(scope="module")
def pattern(patterns):
    return patterns.patterns.at(0)


@fixture(scope="module")
def image(image_path):
    return Image.open(image_path)


def pytest_generate_tests(metafunc):
    if "image_path" in metafunc.fixturenames:
        metafunc.parametrize("image_path", [
                os.path.join(IMAGE_PATH, file)
                for file in os.listdir(IMAGE_PATH)
            ], scope="module")
    if "convert" in metafunc.fixturenames:
        metafunc.parametrize("convert", [convert_image_to_knitting_pattern,
                                         convert_from_image], scope="module")


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
