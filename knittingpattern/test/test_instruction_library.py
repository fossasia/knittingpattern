from test_knittingpattern import fixture
from knittingpattern.InstructionLibrary import InstructionLibrary

DESCRIPTION = "here you can see how to knit: URL"
DESCRIPTION_2 = "well, this is kinda a different description"

library_instructions = [
        {
            "type": "knit",
            "description": DESCRIPTION
        },
        {
            "type": "purl",
            "inverse": "knit"
        },
        {
            "type": "extravagant knit",
            "color": "green",
            "specialattribute": True
        }
    ]

# TODO: What happens if an instruction type is defined multiple times? Error?


@fixture
def library():
    return InstructionLibrary().load.object(library_instructions)


@fixture
def library2(library):
    spec = [
            {"type": "added", "a": 1},
            {"type": "knit", "description": DESCRIPTION_2}
        ]
    library.load.object(spec)
    return library


@fixture
def knit(library):
    return library.as_instruction({"type": "knit"})


@fixture
def purl(library):
    return library.as_instruction({"type": "purl", "color": "white"})


@fixture
def custom_knit(library):
    return library.as_instruction({"type": "extravagant knit"})


def test_knit_type_attributes(knit):
    assert knit.type == "knit"
    assert knit["description"] == DESCRIPTION
    assert knit["type"] == knit.type


def test_knit_has_no_color(knit):
    assert "color" not in knit
    assert "type" in knit


def test_purl_has_color(purl):
    assert purl.color == "white"
    assert "color" in purl


def test_not_everyting_is_known_by_purl(purl):
    assert "asd" not in purl
    assert "inverse" in purl
    assert purl["inverse"] == "knit"


def test_custom_type(custom_knit):
    assert custom_knit["specialattribute"]


def test_default_instruction_is_knit(library):
    assert library.as_instruction({})["type"] == "knit"


def test_library_does_not_forget_old_values(library2):
    assert library2.as_instruction({"knit"})


def test_library_can_load_multiple_times(library2):
    assert library2.as_instruction({"type": "added"})["a"] == 1


def test_library_handles_loading_several_instructions_with_same_type(library2):
    assert library2.as_instruction({})["description"] == DESCRIPTION_2


def test_access_via_type(library):
    assert library["knit"]["type"] == "knit"
