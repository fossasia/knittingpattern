from test_knittingpattern import fixture, raises
import knittingpattern
import json

EMPTY_PATTERN = {
        "version": "0.1",
        "type": "knitting pattern"
    }


@fixture
def temp_empty_pattern_path(tmpdir):
    p = tmpdir.mkdir("sub").join("empty_pattern.knit")
    with open(p.strpath, "w") as f:
        json.dump(EMPTY_PATTERN, f)
    return p.strpath


def assert_is_pattern(pattern):
    assert pattern.type == "knitting pattern"
    assert pattern.version == "0.1"


def test_can_import_empty_pattern_from_object():
    pattern = knittingpattern.load_from_object(EMPTY_PATTERN)
    assert_is_pattern(pattern)


def test_can_import_empty_pattern_from_string():
    json_string = json.dumps(EMPTY_PATTERN)
    pattern = knittingpattern.load_from_string(json_string)
    assert_is_pattern(pattern)


def test_can_import_empty_pattern_from_file_object(temp_empty_pattern_path):
    with open(temp_empty_pattern_path) as file:
        pattern = knittingpattern.load_from_file(file)
    assert_is_pattern(pattern)


def test_can_import_empty_pattern_from_path(temp_empty_pattern_path):
    pattern = knittingpattern.load_from_path(temp_empty_pattern_path)
    assert_is_pattern(pattern)


def test_knitting_pattern_type_is_present():
    with raises(ValueError):
        knittingpattern.load_from_object({})


def test_knitting_pattern_type_is_correct():
    with raises(ValueError):
        knittingpattern.load_from_object({"type": "knitting pattern2"})


def test_load_from_url(temp_empty_pattern_path):
    url = "file:///" + temp_empty_pattern_path
    pattern = knittingpattern.load_from_url(url)
    assert_is_pattern(pattern)
