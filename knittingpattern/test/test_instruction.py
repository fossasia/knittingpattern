from test_knittingpattern import fixture
from knittingpattern.Instruction import Instruction


@fixture
def default_instruction():
    return Instruction({})


@fixture
def purl():
    return Instruction({"type": "purl"})


@fixture
def yo():
    return Instruction({"type": "yo", "number of consumed meshes": 0})


@fixture
def bindoff():
    return Instruction({"type": "bindoff", "number of produced meshes": 0})


@fixture
def colored_instruction():
    return Instruction({"type": "purl",
                        "color": "blue",
                        "custom name": "custom value",
                        "not inherited value": 1},
                       [{"color": "green",
                         "inherited value": 0,
                         "not inherited value": 2},
                        {"other inherited value": 4},
                        {"other inherited value": 0}])


def test_default_type(default_instruction):
    assert default_instruction.type == "knit"
    assert default_instruction.does_knit()
    assert not default_instruction.does_purl()


def test_default_color(default_instruction):
    assert not default_instruction.has_color()
    assert default_instruction.color is None


def test_width(default_instruction, purl):
    assert default_instruction.number_of_consumed_meshes == 1
    assert default_instruction.number_of_produced_meshes == 1
    assert purl.number_of_consumed_meshes == 1
    assert purl.number_of_produced_meshes == 1


def test_purl_is_not_knit(purl):
    assert not purl.does_knit()
    assert purl.does_purl()


def test_color(colored_instruction):
    assert colored_instruction.color == "blue"
    assert "custom name" in colored_instruction
    assert colored_instruction["custom name"] == "custom value"


def test_inheritance(colored_instruction):
    assert colored_instruction["not inherited value"] == 1
    assert colored_instruction["inherited value"] == 0
    assert colored_instruction["other inherited value"] == 4


def test_purl_produces_meshes(purl):
    assert purl.produces_meshes()


def test_purl_consumes_meshes(purl):
    assert purl.consumes_meshes()


def test_yarn_over_consumes_no_meshes(yo):
    assert yo.number_of_consumed_meshes == 0
    assert not yo.consumes_meshes()


def test_yarn_over_produces_meshes(yo):
    assert yo.number_of_produced_meshes == 1
    assert yo.produces_meshes()


def test_bindoff_consumes_meshes(bindoff):
    assert bindoff.number_of_consumed_meshes == 1
    assert bindoff.consumes_meshes()


def test_bindoff_produces_no_meshes(bindoff):
    assert bindoff.number_of_produced_meshes == 0
    assert not bindoff.produces_meshes()
