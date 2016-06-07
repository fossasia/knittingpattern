from test import *
from knittingpattern.convert import SVGRenderer
import io
import untangle # http://docs.python-guide.org/en/latest/scenarios/xml/


@fixture
def file():
    return io.StringIO()


@fixture
def renderer():
    return SVGRenderer(file)


@fixture
def svg(renderer):
    def svg():
        return untangle.parse(file).svg
    return svg
    

@fixture
def svg1(renderer, svg):
    with renderer:
        renderer.render_at(0, 0, "<instruction id=\"inst1-id\"></instruction>", "row1")
        renderer.render_at(1, 0, "<instruction id=\"inst2-id\"></instruction>", "row1")
        renderer.render_at(2, 0, "<instruction id=\"inst3-id\"></instruction>", "row1")
        renderer.render_at(0, 1, "<instruction id=\"inst4-id\"></instruction>", "row2")
        renderer.render_at(1, 1, "<instruction id=\"inst5-id\"></instruction>", "row2")
        renderer.render_at(2.0, 1.0, "<instruction id=\"inst6-id\"></instruction>", "row2")
    return svg()


@fixture
def row1(svg1):
    return svg1.g[0]


@fixture
def row2(svg1):
    return svg1.g[1]


@fixture
def instruction1(row1):
    return row1.g[0]


@fixture
def instruction2(row1):
    return row1.g[1]


@fixture
def instruction3(row1):
    return row1.g[2]


@fixture
def instruction21(row2):
    return row2.g[0]


@fixture
def instruction22(row2):
    return row2.g[1]


@fixture
def instruction23(row2):
    return row2.g[2]


def test_rendering_nothing_is_a_valid_xml(renderer, file):
    with renderer:
        pass
    first_line = file.readline()
    assert first_line.endswith("?>")
    assert first_line.startswith("<?xml")


def test_rendering_nothing_is_an_svg(renderer, file):
    with renderer:
        pass
    grafics = untangle.parse(file)
    assert grafics.elements[0].name == "svg"


def test_translate_to_right_position(instruction1):
    assert instruction1["transform"] == "translate(0,0)"


def test_row_has_id(row1):
    assert row1["id"] == "row1"
    

def test_row_is_displayed_correctly_by_inkscape(row1):
     assert row1["inkscape:label"] == "row1"
     assert row1["inkscape:groupmode"] == "layer"


def test_content_is_in_group(instruction1):
    assert instruction1.instruction["id"] == "inst1-id"


def test_row_contains_several_instructions(row1, row2):
    assert len(row1.g) == 3
    assert len(row2.g) == 3


def test_instruction2_is_translated(instruction2):
    assert instruction2["transform"] == "translate(1,0)"


def test_instruction3_is_translated(instruction3):
    assert instruction3["transform"] == "translate(2,0)"


def test_instruction21_is_translated(instruction21):
    assert instruction21["transform"] == "translate(0,1)"


def test_instruction22_is_translated(instruction22):
    assert instruction22["transform"] == "translate(1,1)"


def test_instruction23_is_translated(instruction23):
    assert instruction23["transform"] == "translate(2.0,1.0)"
































