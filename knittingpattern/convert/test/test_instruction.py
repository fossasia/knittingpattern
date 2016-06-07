from test import *
from knittingpattern.convert.Instruction import Instruction


HERE = os.path.dirname(__file__)
IMAGES_FOLDER = os.path.join(HERE, "test_images")
KNIT_FILE = os.path.join(IMAGES_FOLDER, "knit.svg")
PURL_FILE = os.path.join(IMAGES_FOLDER, "purl.svg")


@fixture
def instruction1():
    return Instruction({"type": "knit"})


@fixture
def knit():
    knit = Instruction({"type": "knit"})
    knit.load_image.relative_folder(__name__, "test_images")
    return knit


@fixture
def purl():
    purl = Instruction({"type": "purl"})
    purl.load_image.relative_folder(__name__, "test_images")
    return purl


@fixture
def renderer():
    return MagicMock()

def test_load_image_from_file(instruction1):
    instruction1.load_image.relative_file(__name__, "test_images/knit.svg")
    with open(KNIT_FILE) as knit_file:
        assert instruction1.raw_image == knit_file.read()


def test_choose_image_from_folder(knit):
    assert knit.raw_image == open(KNIT_FILE).read()


def test_purl_chose_right_image(purl):
    assert purl.raw_image == open(PURL_FILE).read()



