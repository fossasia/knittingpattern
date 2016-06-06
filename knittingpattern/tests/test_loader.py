from knittingpattern.Loader import ContentLoader, JSONLoader
from pytest import fixture


@fixture
def result():
    return []


@fixture
def loader(result):
    def process(obj):
        result.append(obj)
        return len(result)
    def choose_file(path):
        filename = os.path.basename(path)
        return "_2" in filename
    return ContentLoader(process, choose_file)


@fixture
def jsonloader(result):
    return JSONLoader(result.append)


def test_loading_object_does_nothing(loader, result):
    obj = []
    loader.object(obj)
    assert result[0] is obj


def test_processing_result_is_returned(loader):
    assert loader.object(None) == 1
    assert loader.object(None) == 2


def test_json_loader_loads_json(jsonloader, result):
    jsonloader.object("{\"x\": 1}")
    assert result == [{"x": 1}]


def test_loader_would_like_to_load_file(loader):
    assert loader.chooses("x_2.asd")


def test_loader_does_not_like_certain_files(loader):
    assert not loader.chooses("x_1.asd")


def test_loader_can_select_files_it_likes(loader):
    assert loader.choose_files(["_1", "_2", "_3"]) == ["_2"]
    assert loader.choose_files(["_123", "3_2", "4_2.asd"]) == ["3_2", "4_2.asd"]


def test_loading_from_directory_selects_files(loader):
    files_to_load = []
    loader.file = lambda file: files_to_load.append(file)
    assert loader.relative_folder(__name__, "test_instructions")
    assert len(files_to_load) == 2
    assert files_to_load[0].endswith("test_instruction_2.json")
