from .common import *

class KnittingPattern(object):

    def __init__(self, values, rows):
        self.values = values
        self._id = to_id(values[ID])
        self.rows = rows

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self.values[NAME]




__all__ = ["KnittingPattern"]
