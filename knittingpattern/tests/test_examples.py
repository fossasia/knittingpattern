import knittingpattern
from pytest import fixture, raises
import os

EXAMPLES_PATH = os.path.join(os.path.dirname(__file__), "../examples")
CAFE_PATH = os.path.join(EXAMPLES_PATH, "Cafe.json")
CHARLOTTE_PATH = os.path.join(EXAMPLES_PATH, "Charlotte.json")
CAFE_STRING = open(CAFE_PATH).read()
CHARLOTTE_STRING = open(CHARLOTTE_PATH).read()


@fixture
def charlotte():
    return knittingpattern.load_from_string(CHARLOTTE_STRING)


@fixture
def cafe():
    return knittingpattern.load_from_string(CAFE_STRING)


def test_number_of_pattern(charlotte):
    assert len(charlotte.pattern) == 2
    with raises(IndexError):
        charlotte.pattern.at(3)


def test_names(charlotte):
    assert charlotte.pattern.at(0).name == "A.1"
    assert charlotte.pattern.at(1).name == "A.2"


def test_ids(charlotte):
    assert charlotte.pattern.at(0).id == "A.1"
    assert charlotte.pattern.at(1).id == "A.2"


def test_access_with_id(charlotte):
    assert charlotte.pattern["A.1"] == charlotte.pattern.at(0)


def test_iterate_on_pattern(charlotte):
    pattern = charlotte.pattern
    assert list(iter(pattern)) == [pattern.at(0), pattern.at(1)]
