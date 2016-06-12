from test import *
from knittingpattern.Loader import ContentLoader, JSONLoader


@fixture
def result():
    return []


@fixture
def loader(result):

    def process(obj):
        result.append(obj)
        return len(result)

    def chooses_path(path):
        return "_2" in os.path.basename(path)

    return ContentLoader(process, chooses_path)


@fixture
def jsonloader(result):
    return JSONLoader(result.append)


def test_loading_object_does_nothing(loader, result):
    obj = []
    loader.string(obj)
    assert result[0] is obj


def test_processing_result_is_returned(loader):
    assert loader.string(None) == 1
    assert loader.string(None) == 2


def test_json_loader_loads_json(jsonloader, result):
    jsonloader.string("{\"x\": 1}")
    assert result == [{"x": 1}]


def test_loader_would_like_to_load_path(loader):
    assert loader.chooses_path("x_2.asd")


def test_loader_does_not_like_certain_paths(loader):
    assert not loader.chooses_path("x_1.asd")


def test_loader_can_select_paths_it_likes(loader):
    assert loader.choose_paths(["_1", "_2", "_3"]) == ["_2"]
    assert loader.choose_paths(["_123", "3_2", "4_2.as"]) == ["3_2", "4_2.as"]


def test_loading_from_directory_selects_paths(loader):
    paths_to_load = []
    loader.path = lambda path: paths_to_load.append(path)
    assert loader.relative_folder(__name__, "test_instructions")
    assert len(paths_to_load) == 1
    assert paths_to_load[0].endswith("test_instruction_2.json")
