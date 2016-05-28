from .common import *

class Row(object):

    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id



__all__ = ["Row"]
