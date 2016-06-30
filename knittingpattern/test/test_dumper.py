from test_knittingpattern import fixture
from knittingpattern.Dumper import ContentDumper
from io import StringIO, BytesIO
import os


STRING = "asdf1234567890\u1234"
BYTES = STRING.encode("UTF-8")


@fixture
def unicode():
    def dump_to_string(file):
        file.write(STRING[:1])
        file.write(STRING[1:])
    return ContentDumper(dump_to_string)


@fixture
def binary():
    def dump_to_bytes(file):
        file.write(BYTES[:1])
        file.write(BYTES[1:])
    return ContentDumper(dump_to_bytes, text_is_expected=False)


@fixture
def no_encode_text():
    return ContentDumper(lambda file: file.write("asd"), encoding=None)


@fixture
def no_encode_binary():
    return ContentDumper(lambda file: file.write(b"asd"),
                         text_is_expected=False,
                         encoding=None)


def pytest_generate_tests(metafunc):
    if 'save_to' in metafunc.fixturenames:
        metafunc.parametrize("save_to", [binary(), unicode()])


@fixture
def temp_file(save_to):
    return save_to.temporary_file()


@fixture
def binary_temp_file(save_to):
    return save_to.temporary_binary_file()


@fixture
def stringio():
    return StringIO()


def assert_string_is_file_content(file):
    file.seek(0)
    assert file.read() == STRING


def assert_string_is_path_content(path):
    with open(path, encoding="UTF-8") as file:
        assert file.read() == STRING


def assert_string_is_binary_content(file):
    file.seek(0)
    assert file.read() == BYTES


def test_string_is_long():
    assert len(STRING) > 5


def test_dump_to_string(save_to):
    assert save_to.string() == STRING


def test_dump_to_file(save_to, stringio):
    save_to.file(stringio)
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


def test_dump_to_temporary_binary_file(binary_temp_file):
    assert_string_is_binary_content(binary_temp_file)


def test_temporary_file_is_deleted_on_default(temp_file):
    assert_temporary_file_is_deleted(temp_file)


def test_binary_temporary_file_is_deleted_on_default(binary_temp_file):
    assert_temporary_file_is_deleted(binary_temp_file)


def assert_temporary_file_is_deleted(temp_file):
    temp_file.close()
    assert not os.path.isfile(temp_file.name)


def assert_temporary_file_is_not_deleted(temp_file):
    temp_file.close()
    assert os.path.isfile(temp_file.name)


def test_temporary_file_exists(temp_file):
    assert os.path.isfile(temp_file.name)


def test_binary_temporary_file_exists(binary_temp_file):
    assert os.path.isfile(binary_temp_file.name)


def test_temporary_file_has_option_for_deletion(save_to):
    file = save_to.temporary_file(delete_when_closed=False)
    assert_temporary_file_is_not_deleted(file)


def test_binary_temporary_file_has_option_for_deletion(save_to):
    file = save_to.binary_temporary_file(delete_when_closed=False)
    assert_temporary_file_is_not_deleted(file)


def test_file_returns_new_file(save_to):
    file = save_to.file()
    assert_string_is_file_content(file)


def test_dump_is_behind_content_in_new_file(save_to, stringio):
    file = save_to.file()
    assert file.read() == ""


def test_bytes(save_to):
    assert save_to.bytes() == BYTES


def test_encoding(save_to):
    assert save_to.encoding == "UTF-8"


def test_new_binary_file(save_to):
    file = save_to.binary_file()
    file.seek(0)
    assert file.read() == BYTES


def test_binary_file(save_to):
    file = BytesIO()
    save_to.binary_file(file)
    file.seek(0)
    assert file.read() == BYTES


def test_test_binary_file_is_at_end(save_to):
    assert not save_to.binary_file().read()


def test_encoding_is_none(no_encode_binary, no_encode_text):
    assert no_encode_text.encoding is None
    assert no_encode_binary.encoding is None


def test_temporary_path_has_extension(save_to):
    assert save_to.temporary_path(extension=".png").endswith(".png")
    assert save_to.temporary_path(extension=".JPG").endswith(".JPG")


def test_string_representation(save_to):
    string = repr(save_to)
    assert string.startswith("<ContentDumper")
    assert string.endswith(">")
    assert save_to.encoding in string
