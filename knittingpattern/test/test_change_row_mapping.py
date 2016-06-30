"""Test if the mapping of the rows is changed and how."""
from test_knittingpattern import fixture, raises
from knittingpattern import load_from_relative_file as load_relative_file


@fixture
def patterns():
    return load_relative_file(__file__, "pattern/row_removal_pattern.json")


@fixture
def line(patterns):
    return patterns.patterns["line"]


@fixture
def row1(line):
    return line.rows[1]


@fixture
def row2(line):
    return line.rows[2]


@fixture
def row3(line):
    return line.rows[3]

# produced meshes


@fixture
def mesh11p(row1):
    return row1.produced_meshes[0]


@fixture
def mesh12p(row1):
    return row1.produced_meshes[1]


@fixture
def mesh21p(row2):
    return row2.produced_meshes[0]


@fixture
def mesh31p(row3):
    return row3.produced_meshes[0]

# consumed meshes


@fixture
def mesh11c(row1):
    return row1.consumed_meshes[0]


@fixture
def mesh12c(row1):
    return row1.consumed_meshes[1]


@fixture
def mesh21c(row2):
    return row2.consumed_meshes[0]


@fixture
def mesh31c(row3):
    return row3.consumed_meshes[0]


@fixture
def connected_meshes(mesh11p, mesh21c, mesh21p, mesh31c):
    return (mesh11p, mesh21c, mesh21p, mesh31c)


@fixture
def disconnected_meshes(mesh11c, mesh12c, mesh12p, mesh31p):
    return (mesh11c, mesh12c, mesh12p, mesh31p)


@fixture
def meshes(connected_meshes, disconnected_meshes):
    return connected_meshes + disconnected_meshes


@fixture
def connections(mesh11p, mesh21c, mesh21p, mesh31c):
    return ((mesh11p, mesh21c), (mesh21p, mesh31c))


@fixture
def two_way_connections(mesh11p, mesh21c, mesh21p, mesh31c):
    return ((mesh11p, mesh21c), (mesh21c, mesh11p), (mesh21p, mesh31c),
            (mesh31c, mesh21p))


@fixture
def produced_meshes(mesh11p, mesh12p, mesh21p, mesh31p):
    return (mesh11p, mesh12p, mesh21p, mesh31p)


@fixture
def consumed_meshes(mesh11c, mesh12c, mesh21c, mesh31c):
    return (mesh11c, mesh12c, mesh21c, mesh31c)


def pytest_generate_tests(metafunc):
    if "connect" in metafunc.fixturenames:
        metafunc.parametrize("connect", [0, 1])
    if "disconnect" in metafunc.fixturenames:
        metafunc.parametrize("disconnect", [0, 1])


def connect_meshes(mesh1, mesh2, connect):
    if connect == 1:
        mesh2, mesh1 = mesh1, mesh2
    mesh1.connect_to(mesh2)


def disconnect_meshes(mesh1, mesh2, disconnect):
    mesh = (mesh1, mesh2)[disconnect]
    mesh.disconnect()


class TestLine(object):

    """Make sure the pattern is what we expect."""

    def test_consumed_meshes_of_row1(self, row1, mesh11c, mesh12c):
        for mesh in (mesh11c, mesh12c):
            assert not mesh.is_produced()
            assert mesh.is_consumed()
            assert mesh.consuming_row == row1

    def test_produced_meshes_of_row1(self, row1, mesh11p, mesh12p):
        for mesh in (mesh11p, mesh12p):
            assert mesh.is_produced()
            assert mesh.producing_row == row1
        assert mesh11p.is_consumed()
        assert not mesh12p.is_consumed()

    def test_consumed_mesh_of_row2(self, row2, mesh21c):
        assert mesh21c.is_consumed()
        assert mesh21c.is_produced()
        assert mesh21c.consuming_row == row2

    def test_produced_mesh_of_row2(self, row2, mesh21p):
        assert mesh21p.is_consumed()
        assert mesh21p.is_produced()
        assert mesh21p.producing_row == row2

    def test_consumed_mesh_of_row3(self, row3, mesh31c):
        assert mesh31c.is_consumed()
        assert mesh31c.is_produced()
        assert mesh31c.consuming_row == row3

    def test_produced_mesh_of_row3(self, row3, mesh31p):
        assert not mesh31p.is_consumed()
        assert mesh31p.is_produced()
        assert mesh31p.producing_row == row3

    def test_is_connected(self, connected_meshes):
        for mesh in connected_meshes:
            assert mesh.is_connected()

    def test_is_disconnected(self, disconnected_meshes):
        for mesh in disconnected_meshes:
            assert not mesh.is_connected()
            with raises(AssertionError):
                mesh.as_consumed_mesh()
                mesh.as_produced_mesh()

    def test_equality(self, connections):
        for produced_mesh, consumed_mesh in connections:
            assert consumed_mesh.as_produced_mesh() == produced_mesh
            assert produced_mesh.as_consumed_mesh() == consumed_mesh

    def test_is_connected_to(self, two_way_connections):
        for m1, m2 in two_way_connections:
            assert m1.is_connected_to(m2)

    def test_disconnected_from(self, connections, meshes):
        """Test all the meshes that are disconnected from eachother."""
        for m1 in meshes:
            assert m1 == m1
            for m2 in meshes:
                if m1 is m2:
                    continue
                assert m1 != m2
                assert not m1 == m2
                if (m1, m2) not in connections and (m2, m1) not in connections:
                    assert not m1.is_connected_to(m2)
                    if m1.is_connected() and m1 != m2:
                        assert m1.as_produced_mesh() != m2 or m1 == m2
                        assert m1.as_consumed_mesh() != m2 or m1 == m2

    def test_as_produced_mesh(self, produced_meshes):
        for produced_mesh in produced_meshes:
            assert produced_mesh.as_produced_mesh() == produced_mesh

    def test_as_consumed_mesh(self, consumed_meshes):
        for consumed_mesh in consumed_meshes:
            assert consumed_mesh.as_consumed_mesh() == consumed_mesh


def test_remove_a_connection(row1, row2, mesh11p, mesh21c, disconnect):
    disconnect_meshes(mesh11p, mesh21c, disconnect)
    assert mesh11p.is_produced()
    assert not mesh11p.is_consumed()
    assert mesh11p.producing_row == row1

    assert not mesh21c.is_produced()
    assert mesh21c.is_consumed()
    assert mesh21c.consuming_row == row2

    assert mesh11p != mesh21c
    with raises(Exception):
        mesh11p.as_consumed_mesh()
    with raises(Exception):
        mesh21c.as_produced_mesh()


def test_replace_a_connection(disconnect, connect, mesh21p, mesh31c, mesh12p,
                              row1, row3):
    """Remove a connection and create one with a common mesh.

    Remove a connection between mesh21p and mesh31c and create a connection
    between mesh12p and mesh31c.
    """
    disconnect_meshes(mesh21p, mesh31c, disconnect)
    connect_meshes(mesh31c, mesh12p, connect)

    assert not mesh21p.is_connected()
    assert mesh31c.is_connected()
    assert mesh12p.is_connected()

    assert mesh31c.producing_row == row1
    assert mesh12p.consuming_row == row3

    assert mesh31c.as_produced_mesh() == mesh12p
    assert mesh12p.as_consumed_mesh() == mesh31c


def test_connect_to_a_connected_location(mesh12p, mesh31c, mesh21p, connect):
    connect_meshes(mesh12p, mesh31c, connect)
    assert mesh12p.is_connected_to(mesh31c)
    assert not mesh12p.is_connected_to(mesh21p)
    assert not mesh31c.is_connected_to(mesh21p)
    assert not mesh21p.is_connected()


def test_connect_to_a_connected_location_with_connected_mesh(
        mesh11p, mesh31c, mesh21c, mesh21p, connect):
    connect_meshes(mesh11p, mesh31c, connect)
    assert mesh11p.is_connected_to(mesh31c)
    assert not mesh21c.is_connected()
    assert not mesh21p.is_connected()


def test_can_connect(connected_meshes, consumed_meshes, produced_meshes):
    for consumed_mesh in consumed_meshes:
        for produced_mesh in produced_meshes:
            can_connect = consumed_mesh not in connected_meshes and \
                produced_mesh not in connected_meshes
            assert produced_mesh.can_connect_to(consumed_mesh) == can_connect


def test_create_new_connection(mesh31p, mesh12c, connect, row1, row3):
    connect_meshes(mesh31p, mesh12c, connect)

    assert mesh31p.is_connected()
    assert mesh12c.is_connected()

    assert mesh12c.producing_row == row3
    assert mesh31p.consuming_row == row1

    assert mesh12c.as_produced_mesh() == mesh31p
    assert mesh31p.as_consumed_mesh() == mesh12c


def test_disconnect_disconnected(mesh12c):
    mesh12c.disconnect()
    assert not mesh12c.is_connected()
