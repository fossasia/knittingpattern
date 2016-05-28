from pytest import fixture
from knittingpattern.InstructionLibrary import InstructionLibrary
from knittingpattern.KnittingContext import KnittingContext

DESCRIPTION = "here you can see how to knit: URL"

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
    
#TODO: What happens if an instruction type is defined multiple times? Error?


@fixture
def library():
    return InstructionLibrary().load.object(library_instructions)


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


def not_everyting_is_known_by_purl(purl):
    assert "asd" not in purl
    assert "inverse" in purl
    assert purl["inverse"] == "knit"


def test_custom_type(custom_knit):
    assert custom_knit["specialattribute"] == True
