from .Prototype import *

TYPE = "type"
KNIT_TYPE = "knit"
PURL_TYPE = "purl"
DEFAULT_TYPE = KNIT_TYPE
COLOR = "color"
CONSUMED_MESHES = "number_of_consumed_meshes"
PRODUCED_MESHES = "number_of_produced_meshes"


class Instruction(Prototype):

    @property
    def type(self):
        return self.get(TYPE, DEFAULT_TYPE)

    @property
    def color(self):
        return self.get(COLOR, None)

    @property
    def number_of_consumed_meshes(self):
        return self.get(CONSUMED_MESHES, 1)

    @property
    def number_of_produced_meshes(self):
        return self.get(PRODUCED_MESHES, 1)

    def has_color(self):
        return self.color is not None

    def does_knit(self):
        return self.type == KNIT_TYPE

    def does_purl(self):
        return self.type == PURL_TYPE


__all__ = ["Instruction"]
