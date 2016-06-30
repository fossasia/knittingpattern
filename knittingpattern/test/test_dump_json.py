from test_knittingpattern import fixture, MagicMock
from knittingpattern.Dumper import JSONDumper
import json
from knittingpattern.ParsingSpecification import ParsingSpecification


@fixture
def obj():
    return ["123", 123]


@fixture
def dumper(obj):
    def dump():
        return obj
    return JSONDumper(dump)


@fixture
def parser():
    return MagicMock()


def test_dump_object(dumper, obj):
    assert dumper.object() == obj


def test_dump_string(dumper, obj):
    assert dumper.string() == json.dumps(obj)


def test_dump_to_temporary_file(dumper, obj):
    temp_path = dumper.temporary_path()
    with open(temp_path) as file:
        obj2 = json.load(file)
    assert obj2 == obj


def test_dump_to_knitting_pattern(dumper, parser, obj):
    spec = ParsingSpecification(new_parser=parser)
    dumper.knitting_pattern(spec)
    parser.assert_called_with(spec)
    parser(spec).knitting_pattern_set.assert_called_with(obj)


def test_string_representation(dumper):
    string = repr(dumper)
    assert "JSONDumper" in string
