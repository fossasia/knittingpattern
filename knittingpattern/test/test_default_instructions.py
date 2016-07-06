from test_knittingpattern import fixture, pytest
from knittingpattern.InstructionLibrary import DefaultInstructions, \
                                               default_instructions


DEFAULT_INSTRUCTIONS = {
            "knit": (1, 1),
            "purl": (1, 1),
            "skp": (2, 1),
            "yo": (0, 1),
            "yo twisted": (0, 1),
            "k2tog": (2, 1),
            "bo": (1, 0),
            "cdd": (3, 1),
            "co": (0, 1)
        }


@fixture
def default():
    return DefaultInstructions()


@pytest.mark.parametrize("type_,value", DEFAULT_INSTRUCTIONS.items())
def test_mesh_consumption(default, type_, value):
    assert default[type_].number_of_consumed_meshes == value[0]


@pytest.mark.parametrize("type_,value", DEFAULT_INSTRUCTIONS.items())
def test_mesh_production(default, type_, value):
    assert default[type_].number_of_produced_meshes == value[1]


@pytest.mark.parametrize("type_", DEFAULT_INSTRUCTIONS.keys())
def test_description_present(default, type_):
    assert default[type_].description

UNTEDTED_MESSAGE = "No default instructions shall be untested."


def test_all_default_instructions_are_tested(default):
    untested_instructions = \
        set(default.loaded_types) - set(DEFAULT_INSTRUCTIONS)
    assert not untested_instructions, UNTEDTED_MESSAGE


def test_default_instructions_is_a_singleton():
    assert default_instructions() is default_instructions()


def test_default_instructions_are_an_instance_of_the_class():
    assert isinstance(default_instructions(), DefaultInstructions)
