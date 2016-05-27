import knittingpattern
from pytest import fixture, raises
import os

EXAMPLES_PATH = os.path.join(os.path.dirname(__file__), "../examples")
CAFE_PATH = os.path.join(EXAMPLES_PATH, "Cafe.json")
CHARLOTTE_PATH = os.path.join(EXAMPLES_PATH, "Charlotte.json")


@fixture
def charlotte():
    return knittingpattern.load_from_path(CHARLOTTE_PATH)


@fixture
def cafe():
    return knittingpattern.load_from_path(CAFE_PATH)


def test_number_of_pattern(charlotte):
    assert len(charlotte.pattern) == 2
    with raises(IndexError):
        charlotte.pattern[3]


def test_names(charlotte):
    assert charlotte.pattern[0].name == "A.1"
    assert charlotte.pattern[1].name == "A.2"


def test_ids(charlotte):
    assert charlotte.pattern[0].id == "A.1"
    assert charlotte.pattern[1].id == "A.2"


def test_access_with_id(charlotte):
    assert charlotte.pattern["A.1"] == charlotte.pattern[0]

def test_iterate_on_pattern(charlotte):
    pattern = charlotte.pattern
    assert list(iter(pattern)) == [pattern[0], pattern[1]]


@fixture
def a1(charlotte):
    return charlotte.pattern["A.1"]


@fixture
def a2(charlotte):
    return charlotte.pattern["A.2"]


def test_number_of_rows(a1):
    assert len(a1.rows) == 2
    with raises(IndexError):
        a1.rows[3]


def test_row_ids(a1):
    assert a1.row[0].id == ("A.1", "empty", "1")
    assert a1.row[1].id == ("A.1", "lace", "1")


def test_access_by_row_ids(a1):
    assert a1.row[("A.1", "empty", "1")] == a1.row[0]


def test_iterate_on_rows(a1):
    assert list(iter(a1.rows)) == [a1.rows[0], a1.rows[1]]


def test_next_rows(a1):
    assert a1.rows[0].next_rows == [a1.rows[1]]


def test_default_mesh(a1):
    # see Specification.md
    # https://github.com/AllYarnsAreBeautiful/knittingpattern/blob/master/Specification.md
    knit_mesh_row = a1.rows[("A.1", "empty", "1")]
    knit_mesh = knit_mesh_row[0]
    assert knit_mesh.type == "knit"
    assert len(knit_mesh.meshes_below) == 1


