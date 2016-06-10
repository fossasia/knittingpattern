from test import *
from knittingpattern.Dumper import ContentDumper
from io import StringIO
from tempfile import mktemp
import os


STRING = "asdf1234567890"


@fixture
def save_to():
    def dump_my_data_structure(file):
        file.write(STRING[:1])
        file.write(STRING[1:])
    return ContentDumper(dump_my_data_structure)


@fixture
def temp_file(save_to):
    return save_to.temporary_file()


@fixture
def stringio():
    return StringIO()


def assert_string_is_file_content(file):
    file.seek(0)
    assert file.read() == STRING


def assert_string_is_path_content(path):
    with open(path) as file:
        assert file.read() == STRING   


def test_string_is_long():
    assert len(STRING) > 5


def test_dump_to_string(save_to):
    assert save_to.string() == STRING


def test_dump_to_file(save_to, stringio):
    save_to.file(stringio)
    stringio.seek(0)
    assert_string_is_file_content(stringio)


def test_dump_is_behind_content_in_file(save_to, stringio):
    save_to.file(stringio)
    assert stringio.read() == ""
    

def test_dump_to_path(save_to, tmpdir):
    path = tmpdir.mkdir("sub").join("temp.txt").strpath
    save_to.path(path)
    assert_string_is_path_content(path)


def test_dump_to_temp_path(save_to):
    path = save_to.temporary_path()
    assert_string_is_path_content(path)


def test_dump_to_temporary_file(temp_file):
    assert_string_is_file_content(temp_file)


def test_temporary_file_is_deleted_on_default(temp_file):
    temp_file.close()
    assert not os.path.isfile(temp_file.name)


def test_temporary_file_exists(temp_file):
    assert os.path.isfile(temp_file.name)


def test_temporary_file_has_option_for_deletion(save_to):
    file = save_to.temporary_file(delete_when_closed=False)
    file.close()
    assert_string_is_path_content(file.name)
