class KnittingPattern(object):

    def __init__(self, id, name, rows):
        self._id = id
        self._name = name
        self._rows = rows

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def rows(self):
        return self._rows


__all__ = ["KnittingPattern"]
