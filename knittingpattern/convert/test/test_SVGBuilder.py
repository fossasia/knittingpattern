from test_convert import fixture, parse_file, raises
from knittingpattern.convert.SVGBuilder import SVGBuilder
import io

BBOX = (-1, -2, 5, 10)


@fixture
def file():
    return io.StringIO()


@fixture
def builder():
    builder = SVGBuilder()
    builder.bounding_box = BBOX
    return builder


@fixture
def svg(builder, file):
    def svg():
        builder.write_to_file(file)
        file.seek(0)
        print(file.read())
        file.seek(0)
        return parse_file(file).svg
    return svg


@fixture
def svg1(builder, svg):
    instruction = "<instruction id=\"inst{}-id\"></instruction>"
    builder.place(0, 0, instruction.format(1), "row1")
    builder.place(1, 0, instruction.format(2), "row1")
    builder.place(2, 0, instruction.format(3), "row1")
    builder.place(0, 1, instruction.format(4), "row2")
    builder.place(1, 1, instruction.format(5), "row2")
    builder.place(2.0, 1.0, instruction.format(6), "row2")
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


def test_rendering_nothing_is_a_valid_xml(builder, file):
    builder.write_to_file(file)
    file.seek(0)
    first_line = file.readline()
    assert first_line.endswith("?>\n")
    assert first_line.startswith("<?xml")


def test_rendering_nothing_is_an_svg(builder, file):
    builder.write_to_file(file)
    file.seek(0)
    svg = parse_file(file)
    with raises(IndexError):
        svg.g


def test_translate_to_right_position(instruction1):
    assert instruction1["transform"] == "translate(0,0)"


def test_row_has_id(row1):
    assert row1["id"] == "row1"


def test_row_is_displayed_correctly_by_inkscape(row1):
    assert row1["inkscape:label"] == "row1"
    assert row1["inkscape:groupmode"] == "layer"


def test_content_is_in_group(instruction1):
    assert instruction1.g["id"] == "inst1-id"


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


def test_bounding_box(builder):
    assert builder.bounding_box == BBOX


def test_viewport_is_bounding_box(svg1):
    assert svg1["viewBox"] == "{} {} {} {}".format(*BBOX)


def test_width(svg1):
    assert svg1["width"] == "{}".format(BBOX[2] - BBOX[0])


def test_height(svg1):
    assert svg1["height"] == "{}".format(BBOX[3] - BBOX[1])
