from test import *
from knittingpattern.convert.image_to_knittingpattern import *
from knittingpattern import load_from_path
from PIL import Image


IMAGE_NAME = "conversion.bmp"
IMAGE_PATH = os.path.join("pictures", IMAGE_NAME)


@fixture
def patterns():
    path = convert_image_to_knitting_pattern.relative_file(
        __name__, IMAGE_PATH).temporary_path()
    patterns = load_from_path(path)
    return patterns

@fixture
def pattern(patterns):
    return patterns.patterns.at(0)

@fixture
def image():
    return Image.open(os.path.join(HERE, IMAGE_PATH))


def test_convert_image_to_knittingpattern(patterns):
    assert patterns.comment["source"].endswith(IMAGE_NAME)


def test_row_length_is_image_length(pattern, image):
    min_x, min_y, max_x, max_y = image.getbbox()
    assert len(pattern.rows.at(0).instructions) == max_x - min_x
