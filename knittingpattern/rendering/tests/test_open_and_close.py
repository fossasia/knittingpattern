from knittingpattern.rendering import SVGRenderer
import io
from pytest import fixture
from unittest.mock import MagicMock


@fixture
def file():
    return io.StringIO()


@fixture
def renderer(file):
    return SVGRenderer(file)


@fixture
def mock_open():
    return MagicMock()


@fixture
def mock_close():
    return MagicMock()


@fixture
def patched_renderer(renderer, mock_close, mock_open):
    monkeypatch.setattr(renderer, "open", mock_open)
    monkeypatch.setattr(renderer, "close", mock_close)
    return renderer


def test_open_renderer(renderer, file):
    renderer.open()
    assert file.read() == renderer.beginning_of_file


def test_close_renderer(renderer, file):
    renderer.open()
    renderer.close()
    assert file.read() == renderer.beginning_of_file + renderer.end_of_file


def test_open_context(patched_renderer):
    assert not patched_renderer.open.called
    with patched_renderer:
        assert patched_renderer.open.called


def test_close_context(patched_renderer):
    assert not patched_renderer.close.called
    with patched_renderer:
        assert not patched_renderer.close.called
    assert patched_renderer.close.called


def test_file_is_part_of_the_renderer(renderer, file):
    assert renderer.file == file

