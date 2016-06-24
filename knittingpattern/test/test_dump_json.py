from test_knittingpattern import *
from knittingpattern.Dumper import JSONDumper
import json


@fixture
def obj():
    return ["123", 123]


@fixture
def dumper(obj):
    def dump():
        return obj
    return JSONDumper(dump)


def test_dump_object(dumper, obj):
    assert dumper.object() == obj


def test_dump_string(dumper, obj):
    assert dumper.string() == json.dumps(obj)


def test_dump_to_temporary_file(dumper, obj):
    temp_path = dumper.temporary_path()
    with open(temp_path) as file:
        obj2 = json.load(file)
    assert obj2 == obj
