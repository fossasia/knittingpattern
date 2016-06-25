from test_knittingpattern import fixture, raises
from knittingpattern.IdCollection import IdCollection
from collections import namedtuple


I = namedtuple("Item", ["id"])


@fixture
def c():
    return IdCollection()


def test_no_object(c):
    assert not c
    assert not list(c)


def test_add_object(c):
    c.append(I("123"))
    c.append(I("122"))
    assert c.at(0).id == "123"
    assert c.at(1).id == "122"
    assert c["123"].id == "123"
    assert c["122"].id == "122"


def test_length(c):
    assert len(c) == 0
    c.append(I(1))
    assert len(c) == 1
    c.append(I(""))
    assert len(c) == 2


def test_at_raises_keyerror(c):
    with raises(KeyError):
        c["unknown-id"]
