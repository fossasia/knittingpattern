from test import *
from knittingpattern.convert.SVGConverter import SVGConverter
import io
import untangle  # http://docs.python-guide.org/en/latest/scenarios/xml/


def parse_file(file):
    parser = untangle.make_parser()
    sax_handler = untangle.Handler()
    parser.setContentHandler(sax_handler)
    parser.parse(file)
    return sax_handler.root


@fixture
def file():
    return io.StringIO()


@fixture
def converter(file):
    return SVGConverter(file)


@fixture
def svg(converter, file):
    def svg():
        return parse_file(file).svg
    return svg


@fixture
def svg1(converter, svg):
    instruction = "<instruction id=\"inst{}-id\"></instruction>"
    with converter:
        converter.render_at(0, 0, instruction.format(1), "row1")
        converter.render_at(1, 0, instruction.format(2), "row1")
        converter.render_at(2, 0, instruction.format(3), "row1")
        converter.render_at(0, 1, instruction.format(4), "row2")
        converter.render_at(1, 1, instruction.format(5), "row2")
        converter.render_at(2.0, 1.0, instruction.format(6), "row2")
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


def test_rendering_nothing_is_a_valid_xml(converter, file):
    with converter:
        pass
    first_line = file.readline()
    assert first_line.endswith("?>\n")
    assert first_line.startswith("<?xml")


def test_rendering_nothing_is_an_svg(converter, file):
    with converter:
        pass
    grafics = parse_file(file)
    assert grafics.svg["width"] == "0"
    assert grafics.svg["height"] == "0"


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


def test_exit_handler_raises_exception(converter):
    with raises(ValueError):
        with converter:
            raise ValueError("test!")
