"""Test properties of rows."""
from test_knittingpattern import fixture, raises
from test_examples import charlotte as _charlotte


@fixture
def charlotte():
    return _charlotte()


@fixture
def a1(charlotte):
    """:return: the pattern ``"A.1"`` in charlotte"""
    return charlotte.patterns["A.1"]


@fixture
def a2(charlotte):
    """:return: the pattern ``"A.2"`` in charlotte"""
    return charlotte.patterns["A.2"]


def test_number_of_rows(a1):
    """``"A.1"`` should have three rows that can be accessed"""
    assert len(a1.rows) == 3
    with raises(IndexError):
        a1.rows.at(3)


def test_row_ids(a1):
    """Rows in ``"A.1"`` have ids."""
    assert a1.rows.at(0).id == ("A.1", "empty", "1")
    assert a1.rows.at(2).id == ("A.1", "lace", "1")


def test_access_by_row_ids(a1):
    """Rows in ``"A.1"`` can be accessed by their ids."""
    assert a1.rows[("A.1", "empty", "1")] == a1.rows.at(0)


def test_iterate_on_rows(a1):
    """For convinience one can iterate over the rows."""
    assert list(iter(a1.rows)) == [a1.rows.at(0), a1.rows.at(1), a1.rows.at(2)]
