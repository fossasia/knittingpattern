from .Prototype import *

ID = "id"


class Row(Prototype):

    def __init__(self, id, values, inheriting_from = []):
        self._id = id
        self._values = values
        super().__init__(values, inheriting_from)

    @property
    def id(self):
        return self._id

    @property
    def instructions(self):
        return []

    @property
    def produced_meshes(self):
        return []
        
    @property
    def consumed_meshes(self):
        return []
        
__all__ = ["Row"]
