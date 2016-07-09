"""Here you can find the set of knit instructions in rows.

A :class:`knitting pattern set
<knittingpattern.KnittingPatternSet.KnittingPatternSet>`
consists of several :class:`KnittingPatterns
<knittingpattern.KnittingPattern.KnittingPattern>`.
Their functionlality can be found in this module.
"""
from .walk import walk


class KnittingPattern(object):
    """Knitting patterns contain a set of instructions that form a pattern.

    Usually you do not create instances of this but rather load a
    :class:`knitting pattern set
    <knittingpattern.KnittingPatternSet.KnittingPatternSet>`.
    """

    def __init__(self, id_, name, rows, parser):
        """Create a new instance.

        :param id_: the id of this pattern
        :param name: the human readable name of this pattern
        :param rows: a collection of rows of instructions
        :param knittingpattern.Parser.Parser parser: the parser to use to new
          content

        .. seealso:: :func:`knittingpattern.new_knitting_pattern`
        """
        self._id = id_
        self._name = name
        self._rows = rows
        self._parser = parser

    @property
    def id(self):
        """the identifier within a :class:`set of knitting patterns
        <knittingpattern.KnittingPatternSet.KnittingPatternSet>`
        """
        return self._id

    @property
    def name(self):
        """a human readable name"""
        return self._name

    @property
    def rows(self):
        """a collection of rows that this pattern is made of

        Usually this should be a
        :class:`knittingpattern.IdCollection.IdCollection` of
        :class:`knittingpattern.Row.Row`."""
        return self._rows

    def add_row(self, id_):
        """Add a new row to the pattern.

        :param id_: the id of the row
        """
        row = self._parser.new_row(id_)
        self._rows.append(row)
        return row

    def rows_in_knit_order(self):
        """Return the rows in the order that they should be knit.

        :rtype: list
        :return: the :attr:`rows` in the order that they should be knit

        .. seealso:: :mod:`knittingpattern.walk`
        """
        return walk(self)

__all__ = ["KnittingPattern"]
