import knittingpattern
from pytest import fixture
import json
import io

EMPTY_PATTERN = {
        "version": "0.1",
        "type": "knitting pattern"
    }


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


def test_can_import_empty_pattern_from_file_object():
    json_string = json.dumps(EMPTY_PATTERN)
    file = io.StringIO(json_string)
    pattern = knittingpattern.load_from_file(file)
    assert_is_pattern(pattern)


def test_can_import_empty_pattern_from_path(tmpdir):
    p = tmpdir.mkdir("sub").join("empty_pattern.knit")
    with open(p.strpath, "w") as f:
        json.dump(EMPTY_PATTERN, f)
    pattern = knittingpattern.load_from_path(p.strpath)
    assert_is_pattern(pattern)
