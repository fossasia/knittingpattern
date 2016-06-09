from test import *
from knittingpattern.Dumper import ContentDumper
import io


STRING = "asdf"


@fixture
def string():
    @ContentDumper
    def string(dump):
        dump.string(STRING)
    return string


@fixture
def file():
    @ContentDumper
    def file(dump):
        file = dump.file()
        file.write(STRING)
    return file


def pytest_generate_tests(metafunc):
    if "dumper" in metafunc.fixturenames:
        metafunc.parametrize("dumper", [string(), file()])
    
    
def test_dump_to_string(dumper):
    assert dumper.string() == STRING


def test_dump_to_file(dumper):
    file = io.StringIO()
    dumper.file(file)
    file.seek(0)
    assert file.read() == STRING


def test_dump_to_path(dumper, tmpdir):
    path = tmpdir.mkdir("sub").join("temp.txt").strpath
    dumper.path(path)
    with open(path) as f:
        assert f.read() == STRING

def test_string_is_wanted():
    @ContentDumper
    def string(dump):
        assert dump.prefers_string()
        assert not dump.prefers_file()
    string.string()
    
def test_file_is_wanted():
    @ContentDumper
    def file(dump):
        assert not dump.prefers_string()
        assert dump.prefers_file()
    file.file()
    

        