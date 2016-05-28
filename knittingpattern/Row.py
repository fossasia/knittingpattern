from .common import *

class Row(object):

    def __init__(self, values):
        self.values = values
        self._id = to_id(values[ID])

    @property
    def id(self):
        return self._id



__all__ = ["Row"]
