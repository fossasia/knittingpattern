from test_knittingpattern import fixture, os, raises
import knittingpattern

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


def test_number_of_patterns(charlotte):
    assert len(charlotte.patterns) == 2
    with raises(IndexError):
        charlotte.patterns.at(3)


@fixture
def pattern_0(charlotte):
    return charlotte.patterns.at(0)


@fixture
def pattern_1(charlotte):
    return charlotte.patterns.at(1)


def test_names(pattern_0, pattern_1):
    assert pattern_0.name == "A.1"
    assert pattern_1.name == "A.2"


def test_ids(pattern_0, pattern_1):
    assert pattern_0.id == "A.1"
    assert pattern_1.id == "A.2"


def test_access_with_id(charlotte):
    assert charlotte.patterns["A.1"] == charlotte.patterns.at(0)


def test_iterate_on_pattern(charlotte):
    patterns = charlotte.patterns
    assert list(iter(patterns)) == [patterns.at(0), patterns.at(1)]
