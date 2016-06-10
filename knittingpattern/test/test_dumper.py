from test import *
from knittingpattern.Dumper import ContentDumper
import io
from tempfile import mktemp


STRING = "asdf1234567890"


@fixture
def string():
    def string(dump):
        dump.string(STRING[:1])
        dump.string(STRING[1:])
    return ContentDumper(string)


@fixture
def file():
    def file(dump):
        file = dump.file()
        file.write(STRING)
    return ContentDumper(file)


@fixture
def temporary_path():
    def temporary_path(dump):
        temporary_path = dump.get_path()
        with open(temporary_path, "w") as file:
            file.write(STRING)
    return ContentDumper(temporary_path)


@fixture
def path():
    def path(dump):
        path = mktemp()
        with open(temporary_path, "w") as file:
            file.write(STRING)
        dump.path(path)
    return ContentDumper(path)


def pytest_generate_tests(metafunc):
    if "dumper" in metafunc.fixturenames:
        metafunc.parametrize("dumper", [string(), file(), temporary_path(), 
                                        path()])


def test_string_is_long():
    assert len(STRING) > 5


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


def test_dump_to_temp_file(dumper):
    path = dumper.temporary_path()
    with open(path) as file:
        assert file.read() == STRING


def test_string_is_wanted():
    @ContentDumper
    def string(dump):
        assert dump.prefers_string()
        assert not dump.prefers_file()
        assert not dump.prefers_path()
        assert not dump.prefers_get_path()
    string.string()


def test_file_is_wanted():
    @ContentDumper
    def file(dump):
        assert not dump.prefers_string()
        assert dump.prefers_file()
        assert not dump.prefers_path()
        assert not dump.prefers_get_path()
    file.file()


def test_fixed_path_is_wanted(tmpdir):
    p = tmpdir.join("test.txt")
    @ContentDumper
    def path(dump):
        assert not dump.prefers_string()
        assert not dump.prefers_file()
        assert not dump.prefers_path()
        assert dump.prefers_get_path()
    path.path(p)


def test_path_is_wanted():
    @ContentDumper
    def path(dump):
        assert not dump.prefers_string()
        assert not dump.prefers_file()
        assert dump.prefers_path()
        assert dump.prefers_get_path()
    path.path()
