from test_convert import os, HERE, pytest
import re

IMAGES_FOLDER_NAME = "test_images"
IMAGES_FOLDER = os.path.join(HERE, IMAGES_FOLDER_NAME)
KNIT_FILE = os.path.join(IMAGES_FOLDER, "knit.svg")
PURL_FILE = os.path.join(IMAGES_FOLDER, "purl.svg")
YO_FILE = os.path.join(IMAGES_FOLDER, "yo.svg")
K2TOG_FILE = os.path.join(IMAGES_FOLDER, "k2tog.svg")
DEFAULT_FILE = os.path.join(IMAGES_FOLDER, "default.svg")


def title(content):
    """returns the title of the svg"""
    if isinstance(content, str):
        return re.findall("<title[^>]*>([^<]*)</title>", content)[-1]
    return content.title.cdata


def is_knit(content):
    return title(content) == "knit"


def is_purl(content):
    return title(content) == "purl"


def is_yo(content):
    return title(content) == "yo"


def is_k2tog(content):
    return title(content) == "k2tog"


def is_default(content):
    return title(content) == "default"


def read(path):
    with open(path) as file:
        return file.read()


file_to_test = {
        KNIT_FILE: is_knit,
        PURL_FILE: is_purl,
        YO_FILE: is_yo,
        K2TOG_FILE: is_k2tog,
        DEFAULT_FILE: is_default
    }


@pytest.mark.parametrize('path, test', list(file_to_test.items()))
def test_tests_work_on_corresponding_file(path, test):
    assert test(read(path))


@pytest.mark.parametrize('path, test', [
        (path, _test)
        for path in file_to_test
        for test_path, _test in file_to_test.items()
        if path != test_path
    ])
def test_tests_do_not_work_on_other_files(path, test):
    assert not test(read(path))


def test_default_content_has_identifier_in_place():
    assert "{instruction.type}" in read(DEFAULT_FILE)


__all__ = [
        "KNIT_FILE", "PURL_FILE", "YO_FILE", "K2TOG_FILE", "IMAGES_FOLDER",
        "IMAGES_FOLDER_NAME", "DEFAULT_FILE", "read", "title",
        "is_knit", "is_purl", "is_yo", "is_k2tog", "is_default",
    ]
