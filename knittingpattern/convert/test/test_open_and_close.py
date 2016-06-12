from test import *
from knittingpattern.convert.SVGBuilder import SVGBuilder
import io


@fixture
def file():
    return io.StringIO()


@fixture
def builder(file):
    return SVGBuilder(file)


@fixture
def mock_open():
    return MagicMock()


@fixture
def mock_close():
    return MagicMock()


@fixture
def patched_builder(builder, mock_close, mock_open, monkeypatch):
    monkeypatch.setattr(builder, "open", mock_open)
    monkeypatch.setattr(builder, "close", mock_close)
    return builder


def test_open_builder(builder, file):
    builder.open()
    file.seek(0)
    assert file.read() == builder._beginning_of_file


def test_close_builder(builder, file):
    builder.open()
    builder.close()
    assert file.read() == builder._beginning_of_file + builder._end_of_file


def test_open_context(patched_builder):
    assert not patched_builder.open.called
    with patched_builder:
        assert patched_builder.open.called


def test_close_context(patched_builder):
    assert not patched_builder.close.called
    with patched_builder:
        assert not patched_builder.close.called
    assert patched_builder.close.called


def test_file_is_part_of_the_builder(builder, file):
    assert builder._file == file
