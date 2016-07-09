"""The the ability to sort rows in an order so they can  be knit."""
from test_knittingpattern import pytest, HERE
from knittingpattern import load_from_relative_file, new_knitting_pattern
from knittingpattern.walk import walk


def walk_ids(pattern):
    return list(map(lambda row: row.id, walk(pattern)))


@pytest.mark.parametrize("pattern_file,expected_ids", [
    ("inheritance.json", ["colored", "inherited uncolored +instructions",
                          "inherited colored +instructions", "uncolored",
                          "inherited uncolored", "inherited colored"]),
    ("row_mapping_pattern.json", ["1.1", "2.1", "2.2", "3.2", "4.1"]),
    ("row_removal_pattern.json", [1, 2, 3]),
    ("single_instruction.json", [1, 2])])
def test_test_patterns(pattern_file, expected_ids):
    patterns = load_from_relative_file(__name__, "pattern/" + pattern_file)
    pattern = patterns.patterns.at(0)
    walked_ids = walk_ids(pattern)
    assert walked_ids == expected_ids


def construct_graph(links):
    pattern = new_knitting_pattern("constructed_graph")
    rows = pattern.rows
    for link in links:
        for row_id in link:
            if row_id not in rows:
                pattern.add_row(row_id)
    for from_id, *to_ids in links:
        from_row = rows[from_id]
        for to_id in to_ids:
            to_row = rows[to_id]
            from_row.instructions.append({})
            to_row.instructions.append({})
            from_row.last_produced_mesh.connect_to(to_row.last_consumed_mesh)
    return pattern


@pytest.mark.parametrize("links,expected_ids", [
    (((1, 2, 3), (2, 3), (4, 1)), [4, 1, 2, 3]),
    (((4, 1, 2), (2, 3, 5), (5, 6), (3, 0), (0, 6)), [4, 1, 2, 3, 0, 5, 6]),
    (((8, 6, 4, 2, 0), (6, 5), (4, 5), (2, 1), (0, 1), (1, 7), (5, 7), (7, 9)),
     [8, 6, 4, 5, 2, 0, 1, 7, 9]),
    (((3, 1, 2), (1, 1.1), (1.1, 1.2), (2, 2.1), (2.1, 2.2), (2.2, 4),
      (1.2, 4)), [3, 1, 1.1, 1.2, 2, 2.1, 2.2, 4])])
def test_graphs_are_sorted(links, expected_ids):
    pattern = construct_graph(links)
    walked_ids = walk_ids(pattern)
    assert walked_ids == expected_ids
