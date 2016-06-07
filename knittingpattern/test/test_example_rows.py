from test import *
from test_examples import charlotte, cafe
from pytest import fixture, raises


@fixture
def a1(charlotte):
    return charlotte.patterns["A.1"]


@fixture
def a2(charlotte):
    return charlotte.patterns["A.2"]


def test_number_of_rows(a1):
    assert len(a1.rows) == 3
    with raises(IndexError):
        a1.rows.at(3)


def test_row_ids(a1):
    assert a1.rows.at(0).id == ("A.1", "empty", "1")
    assert a1.rows.at(2).id == ("A.1", "lace", "1")


def test_access_by_row_ids(a1):
    assert a1.rows[("A.1", "empty", "1")] == a1.rows.at(0)


def test_iterate_on_rows(a1):
    assert list(iter(a1.rows)) == [a1.rows.at(0), a1.rows.at(1), a1.rows.at(2)]
