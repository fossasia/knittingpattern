from test import *
from knittingpattern.Loader import ContentLoader

HERE = os.path.dirname(__file__)
IMAGES_FOLDER_NAME = "test_images"
IMAGES_FOLDER = os.path.join(HERE, IMAGES_FOLDER_NAME)
KNIT_FILE = os.path.join(IMAGES_FOLDER, "knit.svg")
PURL_FILE = os.path.join(IMAGES_FOLDER, "purl.svg")
YO_FILE = os.path.join(IMAGES_FOLDER, "yo.svg")
DEFAULT_FILE = os.path.join(IMAGES_FOLDER, "default.svg")


def read(path):
    with open(path) as file:
        return file.read()


@fixture
def knit_content():
    return read(KNIT_FILE)


@fixture
def purl_content():
    return read(PURL_FILE)


@fixture
def yo_content():
    return read(YO_FILE)


@fixture
def default_content():
    return read(DEFAULT_FILE)


def test_knit_is_in_knit_file(knit_content):
    assert "knit" in knit_content


def test_knit_is_in_knit_file(purl_content):
    assert "purl" in purl_content


def test_knit_is_in_knit_file(yo_content):
    assert "yo" in yo_content


def test_knit_is_not_in_purl_file(purl_content):
    assert "knit" not in purl_content


def test_knit_is_not_in_yo_file(yo_content):
    assert "knit" not in yo_content


def test_yo_is_not_in_purl_file(purl_content):
    assert "yo" not in purl_content


def test_purl_is_not_in_yo_file(yo_content):
    assert "purl" not in yo_content


def test_purl_is_not_in_knit_file(knit_content):
    assert "purl" not in knit_content


def test_yo_is_not_in_knit_file(knit_content):
    assert "yo" not in knit_content


def test_default_content_has_identifier_in_place(default_content):
    assert "{instruction.type}" in default_content

__all__ = [
        "KNIT_FILE", "PURL_FILE", "YO_FILE", "IMAGES_FOLDER",
        "IMAGES_FOLDER_NAME", "DEFAULT_FILE", "read", "knit_content",
        "purl_content", "yo_content", "default_content"
    ]
