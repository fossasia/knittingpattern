"""Walk the knitting pattern."""


def walk(knitting_pattern):
    """Walk the knitting pattern in a right-to-left fashion.

    :return: an iterable to walk the rows
    :rtype: list
    :param knittingpattern.KnittingPattern.KnittingPattern knitting_pattern: a
      knitting pattern to take the rows from
    """
    rows_before = {}  # key consumes from values
    free_rows = []
    walk = []
    for row in knitting_pattern.rows:
        rows_before_ = row.rows_before[:]
        if rows_before_:
            rows_before[row] = rows_before_
        else:
            free_rows.append(row)
    assert free_rows
    while free_rows:
        print("free rows:", free_rows)
        row = free_rows.pop(0)
        walk.append(row)
        assert row not in rows_before
        for freed_row in reversed(row.rows_after):
            todo = rows_before[freed_row]
            print("  freed:", freed_row, todo)
            todo.remove(row)
            if not todo:
                del rows_before[freed_row]
                free_rows.insert(0, freed_row)
    assert not rows_before, "everything is walked"
    return walk


__all__ = ["walk"]
