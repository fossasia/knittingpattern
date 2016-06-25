"""A :class:`knitting pattern set
<knittingpattern.KnittingPatternSet.KnittingPatternSet>`
consists of several :class:`KnittingPatterns
<knittingpattern.KnittingPattern.KnittingPattern>`.
Their functionlaity can be found in this module.

"""


class KnittingPattern(object):
    """This classes instances contain a set of instructions that form a
    pattern.
    Usually you do not create instances of this but rather load a
    :class:`knitting pattern set
    <knittingpattern.KnittingPatternSet.KnittingPatternSet>`.
    """

    def __init__(self, id_, name, rows):
        """Create a new instance

        :param id_: the id of this pattern
        :param name: the human readable name of this pattern
        :param rows: a collection of rows of instructions

        """
        self._id = id_
        self._name = name
        self._rows = rows

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


__all__ = ["KnittingPattern"]
