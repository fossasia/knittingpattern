
ID = "id"
NAME = "name"


class KnittingPattern(object):

    def __init__(self, values):
        self.values = values

    @property
    def id(self):
        return self.values[ID]

    @property
    def name(self):
        return self.values[NAME]




__all__ = ["KnittingPattern"]
